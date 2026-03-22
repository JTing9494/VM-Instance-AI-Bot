#!/bin/bash
set -e

# Create rsync configuration directory
mkdir -p /etc/rsyncd

# Create rsync daemon configuration
cat > /etc/rsyncd/rsyncd.conf << EOF
uid = root
gid = root
use chroot = false
max connections = 4
syslog facility = local5
pid file = /var/run/rsyncd.pid
lock file = /var/run/rsyncd.lock
log file = /var/log/rsyncd.log

[company_data]
    path = /rsync_data
    comment = Company data for Gemini file search
    read only = true
    list = true
    auth users = app_user
    secrets file = /etc/rsyncd/rsyncd.secrets

[ai_books]
    path = /ai_books
    comment = AI Books collection for Gemini
    read only = true
    list = true
    auth users = app_user
    secrets file = /etc/rsyncd/rsyncd.secrets
