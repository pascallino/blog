CREATE DATABASE IF NOT EXISTS MyBlogtex;
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON `MyBlogtex`.* TO 'root'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
