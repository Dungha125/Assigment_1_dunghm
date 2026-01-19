-- Database creation script for Clean Architecture Bookstore
CREATE DATABASE IF NOT EXISTS bookstore_clean;
USE bookstore_clean;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    INDEX idx_title (title),
    INDEX idx_author (author)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
    INDEX idx_cart_id (cart_id),
    INDEX idx_book_id (book_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
