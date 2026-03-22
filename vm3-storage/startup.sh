#!/bin/bash
set -e

# Setup rsync daemon configuration
mkdir -p /etc/rsyncd
echo 'app_user:rsyncpassword123' > /etc/rsyncd/rsyncd.secrets
chmod 600 /etc/rsyncd/rsyncd.secrets

cat > /etc/rsyncd/rsyncd.conf << 'EOF'
uid = root
gid = root
use chroot = false
max connections = 4
pid file = /var/run/rsyncd.pid
log file = /var/log/rsyncd.log

[ai_books]
    path = /ai_books
    comment = AI Books
    read only = true
    auth users = app_user
    secrets file = /etc/rsyncd/rsyncd.secrets
EOF

# Clean up existing pid file if present
rm -f /var/run/rsyncd.pid

# Start rsync daemon in background
/usr/bin/rsync --daemon --config=/etc/rsyncd/rsyncd.conf &

# Start MySQL server using the original entrypoint (which handles initialization)
exec /usr/local/bin/docker-entrypoint.sh mysqld