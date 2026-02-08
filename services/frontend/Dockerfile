FROM nginx:alpine

# Copy all frontend files to the Nginx document root
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
