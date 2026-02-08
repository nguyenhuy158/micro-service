#!/bin/sh

# Generate config.js from environment variables
cat <<EOF > /usr/share/nginx/html/js/config.js
window.APP_CONFIG = {
    GOOGLE_CLIENT_ID: "${GOOGLE_CLIENT_ID}",
    API_BASE_URL: "${API_BASE_URL}"
};
EOF

# Start nginx
exec nginx -g "daemon off;"
