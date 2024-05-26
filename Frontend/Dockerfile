# Use the official Nginx image as the base image
FROM nginx

# Copy the Nginx configuration file to the appropriate location
COPY app.conf /etc/nginx/conf.d/default.conf

# Copy the HTML file to the Nginx web server directory
COPY labcom.html /var/www/templates/

# Copy the static files to the Nginx web server directory
COPY static /usr/share/nginx/www/static
