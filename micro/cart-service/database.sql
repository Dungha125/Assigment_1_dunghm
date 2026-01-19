-- Database creation script for Cart Service
CREATE DATABASE IF NOT EXISTS bookstore_cart;
USE bookstore_cart;

-- Carts table
CREATE TABLE IF NOT EXISTS carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer_id (customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Cart items table
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    book_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    UNIQUE KEY unique_cart_book (cart_id, book_id),
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    INDEX idx_cart_id (cart_id),
    INDEX idx_book_id (book_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
