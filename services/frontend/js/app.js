const GOOGLE_CLIENT_ID = window.APP_CONFIG?.GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com";
const API_BASE_URL = window.APP_CONFIG?.API_BASE_URL || "http://localhost:8000";

// Setup Toastify helper (Global scope)
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

// Global Translation Helper
const t = (key) => {
    const i18n = window.Alpine?.I18n || window.AlpineI18n;
    if (i18n && typeof i18n.t === 'function') {
        return i18n.t(key);
    }
    return key;
};

document.addEventListener('alpine:init', () => {
    // 1. Initialize I18n
    const i18n = window.Alpine.I18n || window.AlpineI18n;
    if (i18n && window.messages) {
        i18n.create(window.messages);
    } else {
        console.error("I18n plugin or messages not loaded! Shimming $t to prevent crash.");
        Alpine.magic('t', () => (key) => key);
    }

    // 2. Define Stores

    // UI Store (Theme, Language, Active Tab)
    Alpine.store('ui', {
        theme: Alpine.$persist('system').as('app_theme'),
        lang: Alpine.$persist('en').as('app_lang'),
        activeTab: 'products', // products, orders

        init() {
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

    // Auth Store
    Alpine.store('auth', {
        token: Alpine.$persist('').as('auth_token'),
        user: Alpine.$persist(null).as('auth_user'),
        view: 'login', // login, register

        init() {
            // Check for token in URL hash (Redirect Mode Callback)
            this.handleHashToken();

            // Watch for view changes to render Google button
            Alpine.effect(() => {
                if (!this.isAuthenticated && this.view === 'login') {
                    // Give Alpine a moment to render the view
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
                    // Clear hash without refreshing
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
                
                // Fetch user info
                await this.fetchMe();

                toast(t('login_success'), 'success');
            } catch (e) {
                toast(t('login_failed') + ": " + e.message, 'error');
            }
        },

        async loginWithGoogle(idToken) {
            try {
                const res = await fetch(`${API_BASE_URL}/api/v1/user/auth/login/google`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_token: idToken })
                });

                if (!res.ok) throw new Error('Google login failed');

                const data = await res.json();
                this.token = data.access_token;
                
                await this.fetchMe();
                toast(t('login_success'), 'success');
            } catch (e) {
                toast(t('login_failed') + ": " + e.message, 'error');
            }
        },

        async register(userData) {
            try {
                const res = await fetch(`${API_BASE_URL}/api/v1/user/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });

                if (!res.ok) {
                    const error = await res.json();
                    throw new Error(error.detail || 'Registration failed');
                }

                toast(t('register_success'), 'success');
                this.view = 'login';
            } catch (e) {
                toast(t('register_failed') + ": " + e.message, 'error');
            }
        },

        async fetchMe() {
            try {
                const res = await fetch(`${API_BASE_URL}/api/v1/user/users/me`, {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                });
                if (res.ok) {
                    this.user = await res.json();
                } else {
                    this.logout();
                }
            } catch (e) {
                console.error("Fetch me error", e);
            }
        },

        logout() {
            this.token = '';
            this.user = null;
            toast(t('logged_out'), 'info');
        }
    });

    // Cart Store
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

                const res = await fetch(`${API_BASE_URL}/api/v1/order/orders/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${auth.token}`
                    },
                    body: JSON.stringify(orderData)
                });

                if (!res.ok) {
                    const error = await res.json();
                    throw new Error(error.detail || 'Checkout failed');
                }

                toast(t('checkout_success'), 'success');
                this.clear();
                // Switch to orders tab
                Alpine.store('ui').activeTab = 'orders';
            } catch (e) {
                toast(t('checkout_failed') + ": " + e.message, 'error');
            } finally {
                this.loading = false;
            }
        }
    });

    // Products Data Component
    Alpine.data('products', () => ({
        list: [],
        filteredList: [],
        search: '',
        loading: false,

        async init() {
            if (window.autoAnimate && this.$refs.productList) {
                window.autoAnimate(this.$refs.productList);
            }

            const auth = Alpine.store('auth');
            if (auth && auth.isAuthenticated) {
                await this.fetch();
            }

            this.$watch('$store.auth.token', (val) => {
                if (val) this.fetch();
                else {
                    this.list = [];
                    this.filteredList = [];
                }
            });

            this.$watch('search', () => {
                this.filter();
            });
        },

        async fetch() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                if (!auth || !auth.token) return;

                const res = await fetch(`${API_BASE_URL}/api/v1/product/products/`, {
                    headers: { 'Authorization': `Bearer ${auth.token}` }
                });

                if (res.ok) {
                    this.list = await res.json();
                    this.filter();
                } else if (res.status === 401) {
                    auth.logout();
                }
            } catch (e) {
                console.error("Fetch products error", e);
            } finally {
                this.loading = false;
            }
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

    // Orders Data Component
    Alpine.data('orders', () => ({
        list: [],
        loading: false,

        async init() {
            this.$watch('$store.ui.activeTab', (val) => {
                if (val === 'orders') this.fetch();
            });
        },

        async fetch() {
            this.loading = true;
            try {
                const auth = Alpine.store('auth');
                if (!auth || !auth.token || !auth.user) return;

                const res = await fetch(`${API_BASE_URL}/api/v1/order/orders/user/${auth.user.id}`, {
                    headers: { 'Authorization': `Bearer ${auth.token}` }
                });

                if (res.ok) {
                    this.list = await res.json();
                }
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
            const colors = {
                'PENDING': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
                'PAID': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
                'SHIPPED': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
                'DELIVERED': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
                'CANCELLED': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
                'FAILED': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
            };
            return colors[status] || 'bg-gray-100 text-gray-800';
        }
    }));
});
