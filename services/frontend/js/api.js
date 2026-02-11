const api = (() => {
    const baseURL = () => window.APP_CONFIG?.API_BASE_URL || "http://localhost:8000";

    const getHeaders = (body) => {
        const headers = {};
        const token = Alpine.store('auth')?.token;
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        if (body && !(body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }
        return headers;
    };

    const handleResponse = async (res) => {
        if (res.status === 401) {
            Alpine.store('auth')?.logout();
            throw new Error('Unauthorized');
        }
        if (!res.ok) {
            const error = await res.json().catch(() => ({}));
            throw new Error(error.detail || `Request failed (${res.status})`);
        }
        if (res.status === 204) return null;
        return res.json();
    };

    const request = async (method, path, body) => {
        const options = {
            method,
            headers: getHeaders(body),
        };
        if (body !== undefined) {
            options.body = body instanceof FormData ? body : JSON.stringify(body);
        }
        const res = await fetch(`${baseURL()}${path}`, options);
        return handleResponse(res);
    };

    return {
        get: (path) => request('GET', path),
        post: (path, body) => request('POST', path, body),
        patch: (path, body) => request('PATCH', path, body),
        delete: (path) => request('DELETE', path),
    };
})();
