const GOOGLE_CLIENT_ID = window.APP_CONFIG?.GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com";
const API_BASE_URL = window.APP_CONFIG?.API_BASE_URL || "http://localhost:8000";

const toast = (text, type = 'info') => {
    let bg = "linear-gradient(to right, #00b09b, #96c93d)";
    if (type === 'error') bg = "linear-gradient(to right, #ff5f6d, #ffc371)";
    if (type === 'warning') bg = "linear-gradient(to right, #f7b733, #fc4a1a)";

    Toastify({
        text: text,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: { background: bg },
    }).showToast();
};

const t = (key) => {
    const i18n = window.Alpine?.I18n || window.AlpineI18n;
    if (i18n && typeof i18n.t === 'function') {
        return i18n.t(key);
    }
    return key;
};

document.addEventListener('alpine:init', () => {
    const i18n = window.AlpineI18n;
    if (i18n && window.messages) {
        const savedLang = JSON.parse(localStorage.getItem('app_lang')) || 'en';
        i18n.create(savedLang, window.messages);
    } else {
        console.error("I18n plugin or messages not loaded! Shimming $t to prevent crash.", {
            plugin: !!i18n,
            messages: !!window.messages
        });
        Alpine.magic('t', () => (key) => key);
    }

    registerRouter();

    Alpine.store('ui', {
        theme: Alpine.$persist('system').as('app_theme'),
        lang: Alpine.$persist('en').as('app_lang'),
        cartOpen: false,
        searchExpanded: false,

        init() {
            if (!['en', 'vi'].includes(this.lang)) {
                this.lang = 'en';
            }

            this.applyTheme();
            this.applyLang();

            Alpine.effect(() => {
                this.theme;
                this.applyTheme();
            });

            Alpine.effect(() => {
                this.lang;
                this.applyLang();
            });
        },

        toggleTheme() {
            if (this.theme === 'light') this.theme = 'dark';
            else if (this.theme === 'dark') this.theme = 'system';
            else this.theme = 'light';
        },

        toggleLang() {
            this.lang = this.lang === 'en' ? 'vi' : 'en';
        },

        applyTheme() {
            const isDark = this.theme === 'dark' ||
                (this.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

            if (isDark) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        },

        applyLang() {
            const i18n = window.Alpine?.I18n || window.AlpineI18n;
            if (i18n) {
                i18n.locale = this.lang;
            }
            if (window.dayjs) {
                window.dayjs.locale(this.lang);
            }
        }
    });

    Alpine.store('auth', {
        token: Alpine.$persist('').as('auth_token'),
        user: Alpine.$persist(null).as('auth_user'),
        view: 'login',

        init() {
            this.handleHashToken();

            Alpine.effect(() => {
                if (!this.isAuthenticated && this.view === 'login') {
                    setTimeout(() => this.initGoogleAuth(), 100);
                }
            });
        },

        handleHashToken() {
            const hash = window.location.hash;
            if (hash && hash.startsWith('#token=')) {
                const token = hash.split('=')[1];
                if (token) {
                    this.token = token;
                    window.history.replaceState(null, null, window.location.pathname);
                    this.fetchMe().then(() => {
                        toast(t('login_success'), 'success');
                    });
                }
            }
        },

        initGoogleAuth() {
            if (typeof google === 'undefined') return;

            google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                ux_mode: 'redirect',
                login_uri: `${API_BASE_URL}/api/v1/user/auth/login/google/callback`,
            });

            const btnParent = document.getElementById('google-login-btn');
            if (btnParent) {
                google.accounts.id.renderButton(
                    btnParent,
                    { theme: "outline", size: "large", width: btnParent.offsetWidth }
                );
            }
        },

        get isAuthenticated() {
            return !!this.token;
        },

        async login(username, password) {
            try {
                const params = new URLSearchParams();
                params.append('username', username);
                params.append('password', password);

                const res = await fetch(`${API_BASE_URL}/api/v1/user/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: params
                });

                if (!res.ok) throw new Error('Login failed');

                const data = await res.json();
                this.token = data.access_token;

                await this.fetchMe();

                toast(t('login_success'), 'success');
            } catch (e) {
                toast(t('login_failed') + ": " + e.message, 'error');
            }
        },

        async loginWithGoogle(idToken) {
            try {
                const data = await api.post('/api/v1/user/auth/login/google', { id_token: idToken });
                this.token = data.access_token;

                await this.fetchMe();
                toast(t('login_success'), 'success');
            } catch (e) {
                toast(t('login_failed') + ": " + e.message, 'error');
            }
        },

        async register(userData) {
            try {
                await api.post('/api/v1/user/auth/register', userData);
                toast(t('register_success'), 'success');
                this.view = 'login';
            } catch (e) {
                toast(t('register_failed') + ": " + e.message, 'error');
            }
        },

        async fetchMe() {
            try {
                const data = await api.get('/api/v1/user/users/me');
                this.user = data;
            } catch (e) {
                if (e.message === 'Unauthorized') {
                    this.logout();
                } else {
                    console.error("Fetch me error", e);
                }
            }
        },

        logout() {
            this.token = '';
            this.user = null;
            toast(t('logged_out'), 'info');
        }
    });

    Alpine.store('cart', {
        items: Alpine.$persist([]).as('cart_items'),
        loading: false,

        get total() {
            return this.items.reduce((acc, item) => acc + item.price, 0);
        },

        add(product) {
            this.items.push(product);
            toast(`${t('added_to_cart')}: ${product.name}`, 'success');
        },

        remove(index) {
            this.items.splice(index, 1);
        },

        clear() {
            this.items = [];
        },

        async checkout() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                if (!auth || !auth.token || !auth.user) throw new Error('Not authenticated');

                const orderData = {
                    user_id: auth.user.id,
                    items: this.items.map(item => ({
                        product_id: item.id,
                        quantity: 1,
                        price: item.price
                    })),
                    total_amount: this.total
                };

                await api.post('/api/v1/order/orders/', orderData);

                toast(t('checkout_success'), 'success');
                this.clear();
                Alpine.store('router').navigate('orders');
            } catch (e) {
                toast(t('checkout_failed') + ": " + e.message, 'error');
            } finally {
                this.loading = false;
            }
        }
    });

    Alpine.store('profile', {
        loading: false,
        totpSetup: null,

        async updateInfo(full_name, email) {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                await api.patch('/api/v1/user/users/me', { full_name, email });

                await auth.fetchMe();
                toast(t('profile_updated'), 'success');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async changePassword(old_password, new_password) {
            this.loading = true;
            try {
                await api.post('/api/v1/user/users/me/password', { old_password, new_password });
                toast(t('password_changed'), 'success');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async uploadAvatar(file) {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                const formData = new FormData();
                formData.append('file', file);

                await api.post('/api/v1/user/users/me/avatar', formData);

                await auth.fetchMe();
                toast(t('avatar_uploaded'), 'success');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async setupTOTP() {
            this.loading = true;
            try {
                this.totpSetup = await api.post('/api/v1/user/users/me/totp/setup');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async enableTOTP(code) {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                await api.post('/api/v1/user/users/me/totp/enable', { code, secret: this.totpSetup.secret });

                this.totpSetup = null;
                await auth.fetchMe();
                toast(t('totp_enable_success') || 'MFA Enabled', 'success');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async disableTOTP() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                await api.post('/api/v1/user/users/me/totp/disable');

                await auth.fetchMe();
                toast(t('totp_disable_success') || 'MFA Disabled', 'info');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        }
    });

    Alpine.store('apiKeys', {
        keys: [],
        loading: false,

        async fetch() {
            this.loading = true;
            try {
                this.keys = await api.get('/api/v1/inventory/keys/me');
            } catch (e) {
                console.error("Fetch API keys error", e);
            } finally {
                this.loading = false;
            }
        },

        copyKey(key) {
            navigator.clipboard.writeText(key).then(() => {
                toast('API key copied to clipboard', 'success');
            }).catch(() => {
                toast('Failed to copy key', 'error');
            });
        }
    });

    Alpine.store('admin', {
        products: [],
        productsLoading: false,
        categories: [],

        inventory: [],
        inventoryLoading: false,

        orders: [],
        ordersLoading: false,

        async fetchProducts() {
            this.productsLoading = true;
            try {
                this.products = await api.get('/api/v1/product/products/');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.productsLoading = false;
            }
        },

        async createProduct(data) {
            try {
                await api.post('/api/v1/product/products', data);
                toast('Product created', 'success');
                await this.fetchProducts();
            } catch (e) {
                toast(e.message, 'error');
            }
        },

        async fetchCategories() {
            try {
                this.categories = await api.get('/api/v1/product/categories');
            } catch (e) {
                console.error("Fetch categories error", e);
            }
        },

        async createCategory(data) {
            try {
                await api.post('/api/v1/product/categories', data);
                toast('Category created', 'success');
                await this.fetchCategories();
            } catch (e) {
                toast(e.message, 'error');
            }
        },

        async fetchInventory() {
            this.inventoryLoading = true;
            try {
                this.inventory = await api.get('/api/v1/inventory/all');
            } catch (e) {
                toast(e.message, 'error');
            } finally {
                this.inventoryLoading = false;
            }
        },

        async createInventory(data) {
            try {
                await api.post('/api/v1/inventory/', data);
                toast('Inventory created', 'success');
                await this.fetchInventory();
            } catch (e) {
                toast(e.message, 'error');
            }
        },

        async fetchOrders() {
            this.ordersLoading = true;
            try {
                toast('Admin order listing is not yet available', 'warning');
            } finally {
                this.ordersLoading = false;
            }
        },

        async updateOrderStatus(orderId, status) {
            try {
                await api.patch(`/api/v1/order/orders/${orderId}`, { status });
                toast('Order status updated', 'success');
            } catch (e) {
                toast(e.message, 'error');
            }
        }
    });

    Alpine.data('products', () => ({
        list: [],
        filteredList: [],
        search: '',
        loading: false,
        selectedProduct: null,
        selectedCategory: '',
        sortBy: 'newest',
        page: 1,
        pageSize: 12,
        hasMore: true,
        categories: [],

        async init() {
            if (window.autoAnimate && this.$refs.productList) {
                window.autoAnimate(this.$refs.productList);
            }

            const auth = Alpine.store('auth');
            if (auth && auth.isAuthenticated) {
                await this.fetchCategories();
                await this.fetch();
            }

            this.$watch('$store.auth.token', (val) => {
                if (val) {
                    this.fetchCategories();
                    this.fetch();
                } else {
                    this.list = [];
                    this.filteredList = [];
                }
            });

            this.$watch('search', () => {
                this.filter();
            });

            this.$watch('selectedCategory', () => {
                this.page = 1;
                this.list = [];
                this.fetch();
            });

            this.$watch('sortBy', () => {
                this.page = 1;
                this.list = [];
                this.fetch();
            });
        },

        async fetchCategories() {
            try {
                this.categories = await api.get('/api/v1/product/categories');
            } catch (e) {
                console.error("Fetch categories error", e);
            }
        },

        async fetch() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                if (!auth || !auth.token) return;

                const skip = (this.page - 1) * this.pageSize;
                let url = `/api/v1/product/products/?skip=${skip}&limit=${this.pageSize}`;
                if (this.selectedCategory) {
                    url += `&category_id=${this.selectedCategory}`;
                }
                if (this.sortBy) {
                    url += `&sort_by=${this.sortBy}`;
                }

                const data = await api.get(url);
                if (this.page === 1) {
                    this.list = data;
                } else {
                    this.list = [...this.list, ...data];
                }
                this.hasMore = data.length === this.pageSize;
                this.filter();
            } catch (e) {
                if (e.message === 'Unauthorized') {
                    Alpine.store('auth').logout();
                } else {
                    console.error("Fetch products error", e);
                }
            } finally {
                this.loading = false;
            }
        },

        loadMore() {
            if (!this.hasMore || this.loading) return;
            this.page++;
            this.fetch();
        },

        filter() {
            if (!this.search) {
                this.filteredList = this.list;
                return;
            }
            const q = this.search.toLowerCase();
            this.filteredList = this.list.filter(p =>
                p.name.toLowerCase().includes(q) ||
                p.description.toLowerCase().includes(q)
            );
        }
    }));

    Alpine.data('orders', () => ({
        list: [],
        loading: false,

        async init() {
            this.$watch('$store.router.currentRoute', (val) => {
                if (val === 'orders') this.fetch();
            });
        },

        async fetch() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                if (!auth || !auth.token || !auth.user) return;

                const data = await api.get(`/api/v1/order/orders/user/${auth.user.id}`);
                this.list = data.map(o => ({ ...o, _expanded: false }));
            } catch (e) {
                console.error("Fetch orders error", e);
            } finally {
                this.loading = false;
            }
        },

        formatDate(dateStr) {
            return dayjs(dateStr).format('YYYY-MM-DD HH:mm');
        },

        getStatusColor(status) {
            const s = (status || '').toLowerCase();
            const colors = {
                'pending': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
                'paid': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
                'shipped': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
                'delivered': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
                'cancelled': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
                'failed': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
            };
            return colors[s] || 'bg-gray-100 text-gray-800';
        }
    }));

    Alpine.data('orderDetail', () => ({
        order: null,
        loading: false,
        keys: [],

        async init() {
            this.$watch('$store.router.currentRoute', (val) => {
                if (val === 'order-detail') {
                    const params = Alpine.store('router').params;
                    if (params.id) {
                        this.fetch(params.id);
                        this.fetchKeys(params.id);
                    }
                }
            });

            this.$watch('$store.router.params', (params) => {
                if (Alpine.store('router').currentRoute === 'order-detail' && params.id) {
                    this.fetch(params.id);
                    this.fetchKeys(params.id);
                }
            });

            if (Alpine.store('router').currentRoute === 'order-detail') {
                const params = Alpine.store('router').params;
                if (params.id) {
                    await this.fetch(params.id);
                    await this.fetchKeys(params.id);
                }
            }
        },

        async fetch(orderId) {
            this.loading = true;
            try {
                this.order = await api.get(`/api/v1/order/orders/${orderId}`);
            } catch (e) {
                console.error("Fetch order detail error", e);
            } finally {
                this.loading = false;
            }
        },

        async fetchKeys(orderId) {
            try {
                this.keys = await api.get(`/api/v1/inventory/keys/order/${orderId}`);
            } catch (e) {
                console.error("Fetch order keys error", e);
            }
        },

        formatDate(dateStr) {
            return dayjs(dateStr).format('YYYY-MM-DD HH:mm');
        },

        getStatusColor(status) {
            const s = (status || '').toLowerCase();
            const colors = {
                'pending': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
                'paid': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
                'shipped': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
                'delivered': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
                'cancelled': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
                'failed': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
            };
            return colors[s] || 'bg-gray-100 text-gray-800';
        }
    }));
});
