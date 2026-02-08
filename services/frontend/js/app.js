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

document.addEventListener('alpine:init', () => {
    // 1. Initialize I18n
    // Ensure messages are loaded from window.messages
    if (window.Alpine.I18n && window.messages) {
        window.Alpine.I18n.create(window.messages);
    } else {
        console.error("I18n plugin or messages not loaded!");
    }

    // 2. Define Stores
    
    // UI Store (Theme, Language)
    Alpine.store('ui', {
        theme: Alpine.$persist('system').as('app_theme'),
        lang: Alpine.$persist('en').as('app_lang'),

        init() {
            this.applyTheme();
            this.applyLang();
            
            // Watchers
            this.$watch('theme', () => this.applyTheme());
            this.$watch('lang', (val) => {
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
            if (window.Alpine.I18n) {
                window.Alpine.I18n.locale = this.lang;
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
        
        get isAuthenticated() {
            return !!this.token;
        },

        async login(username, password) {
            try {
                const params = new URLSearchParams();
                params.append('username', username);
                params.append('password', password);

                const res = await fetch('http://localhost:8000/api/v1/login/access-token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: params
                });

                if (!res.ok) throw new Error('Login failed');

                const data = await res.json();
                this.token = data.access_token;
                this.user = { username }; 
                
                toast(window.Alpine.I18n.t('login_success'), 'success');
            } catch (e) {
                toast(window.Alpine.I18n.t('login_failed') + ": " + e.message, 'error');
            }
        },

        logout() {
            this.token = '';
            this.user = null;
            toast(window.Alpine.I18n.t('logged_out'), 'info');
        }
    });

    // Cart Store
    Alpine.store('cart', {
        items: Alpine.$persist([]).as('cart_items'),

        get total() {
            return this.items.reduce((acc, item) => acc + item.price, 0);
        },

        add(product) {
            this.items.push(product);
            toast(`${window.Alpine.I18n.t('added_to_cart')}: ${product.name}`, 'success');
        },

        clear() {
            this.items = [];
        },
        
        checkout() {
             toast(window.Alpine.I18n.t('checkout_msg'), 'warning');
             this.clear();
        }
    });

    // Products Data Component
    Alpine.data('products', () => ({
        list: [],
        loading: false,

        async init() {
            // Apply AutoAnimate if available globally
            // Note: autoAnimate (formkit) might not be globally exposed via simple script tag easily without a shim,
            // but if window.autoAnimate exists (from some CDNs), use it.
            // For now, removing explicit autoAnimate call to fix module error unless we confirm the global.
            // If the user insists on AutoAnimate, we'd need a proper import map or global build.
            // Assuming for now we skip or check existence to avoid crash.
            if (window.autoAnimate && this.$refs.productList) {
                window.autoAnimate(this.$refs.productList);
            }

            if (Alpine.store('auth').isAuthenticated) {
                await this.fetch();
            }

            this.$watch('$store.auth.token', (val) => {
                if (val) this.fetch();
                else this.list = [];
            });
        },

        async fetch() {
            this.loading = true;
            try {
                const res = await fetch('http://localhost:8000/api/v1/products', {
                    headers: { 
                        'Authorization': `Bearer ${Alpine.store('auth').token}` 
                    }
                });
                if (res.ok) {
                    this.list = await res.json();
                } else if (res.status === 401) {
                    Alpine.store('auth').logout();
                }
            } catch (e) {
                console.error("Fetch error", e);
                toast(window.Alpine.I18n.t('no_products'), 'error');
            } finally {
                this.loading = false;
            }
        }
    }));
});
