-- Create Database
CREATE DATABASE IF NOT EXISTS billing_system;

USE billing_system;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT,
    expiry DATE
);

-- Bills table
CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    total DECIMAL(10,2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bill Items table
CREATE TABLE IF NOT EXISTS bill_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert default admin user (username: admin, password: admin123)
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');
