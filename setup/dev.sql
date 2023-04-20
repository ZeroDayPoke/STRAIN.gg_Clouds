-- Creates Strain DB and User
CREATE DATABASE IF NOT EXISTS strain_db;
CREATE USER IF NOT EXISTS 'strainadmin'@'localhost'
IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON strain_db.*
TO 'strainadmin'@'localhost';
FLUSH PRIVILEGES;
