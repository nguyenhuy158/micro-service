FROM nginx:alpine

# Copy all frontend files to the Nginx document root
COPY . /usr/share/nginx/html

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 80
EXPOSE 80

# Use entrypoint to generate config and start nginx
ENTRYPOINT ["/entrypoint.sh"]
