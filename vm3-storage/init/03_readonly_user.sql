-- Create read-only user for VM-2 to connect
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT SELECT ON company_data.* TO 'app_user'@'%';
GRANT SELECT ON companies.* TO 'app_user'@'%';
GRANT SELECT ON users.* TO 'app_user'@'%';
FLUSH PRIVILEGES;