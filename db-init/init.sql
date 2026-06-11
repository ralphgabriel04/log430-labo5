-- Create database 
CREATE DATABASE IF NOT EXISTS labo05_db;
USE labo05_db;

-- Users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    sku VARCHAR(64) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    payment_link VARCHAR(100),
    is_paid BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Order items
DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Product stocks 
DROP TABLE IF EXISTS stocks;
CREATE TABLE stocks (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Mock data: users
INSERT INTO users (name, email) VALUES
('Ada Lovelace', 'alovelace@example.com'),
('Adele Goldberg', 'agoldberg@example.com'),
('Alan Turing', 'aturing@example.com');

-- Mock data: products
INSERT INTO products (name, sku, price) VALUES
('Laptop ABC', 'LP12567', 1999.99),
('Keyboard DEF', 'KB67890', 59.50),
('Gadget XYZ', 'GG12345', 5.75),
('27-inch Screen WYZ', 'SC27289', 299.75);

-- Mock data: product stocks
INSERT INTO stocks (product_id, quantity) VALUES
(1, 1000),
(2, 500),
(3, 2),
(4, 90);

-- Indexes
CREATE INDEX idx_stocks_product_id ON stocks (product_id);
CREATE INDEX idx_order_items_product_id ON order_items (product_id);