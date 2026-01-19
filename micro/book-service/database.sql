-- Database creation script for Book Service
CREATE DATABASE IF NOT EXISTS bookstore_book;
USE bookstore_book;

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
