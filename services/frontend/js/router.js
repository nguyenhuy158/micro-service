function registerRouter() {
    const routes = [
        { pattern: /^#\/orders\/([^/]+)$/, name: 'order-detail', paramNames: ['id'] },
        { pattern: /^#\/orders$/, name: 'orders', paramNames: [] },
        { pattern: /^#\/products$/, name: 'products', paramNames: [] },
        { pattern: /^#\/keys$/, name: 'api-keys', paramNames: [] },
        { pattern: /^#\/profile$/, name: 'profile', paramNames: [] },
        { pattern: /^#\/admin\/products$/, name: 'admin-products', paramNames: [] },
        { pattern: /^#\/admin\/orders$/, name: 'admin-orders', paramNames: [] },
        { pattern: /^#\/admin\/inventory$/, name: 'admin-inventory', paramNames: [] },
    ];

    function parseHash(hash) {
        if (!hash || hash.startsWith('#token=')) {
            return { route: 'products', params: {} };
        }

        for (const r of routes) {
            const match = hash.match(r.pattern);
            if (match) {
                const params = {};
                r.paramNames.forEach((name, i) => {
                    params[name] = match[i + 1];
                });
                return { route: r.name, params };
            }
        }

        return { route: 'products', params: {} };
    }

    Alpine.store('router', {
        currentRoute: 'products',
        params: {},

        navigate(route, params = {}) {
            const reverseMap = {
                'products': '#/products',
                'orders': '#/orders',
                'order-detail': (p) => `#/orders/${p.id}`,
                'api-keys': '#/keys',
                'profile': '#/profile',
                'admin-products': '#/admin/products',
                'admin-orders': '#/admin/orders',
                'admin-inventory': '#/admin/inventory',
            };

            const entry = reverseMap[route];
            if (entry) {
                window.location.hash = typeof entry === 'function' ? entry(params) : entry;
            }
        },

        init() {
            const apply = () => {
                const { route, params } = parseHash(window.location.hash);
                this.currentRoute = route;
                this.params = params;
            };

            apply();
            window.addEventListener('hashchange', () => apply());
        },
    });
}
