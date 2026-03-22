FROM mysql:5.7

# Install rsync
RUN yum install -y rsync && rm -rf /var/cache/yum

# Copy initialization scripts
COPY init/ /docker-entrypoint-initdb.d/

# Create rsync daemon configuration directory
RUN mkdir -p /etc/rsyncd /ai_books

# Copy rsync setup script
COPY rsync_setup.sh /usr/local/bin/rsync_setup.sh
RUN chmod +x /usr/local/bin/rsync_setup.sh

# Expose MySQL and rsync ports
EXPOSE 3306
EXPOSE 873

# Copy custom startup script
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Startup script will run both rsync and MySQL
CMD ["/startup.sh"]