CREATE DATABASE smart_library;
USE smart_library;

CREATE TABLE users(
user_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
phone_number VARCHAR(20) NOT NULL,
email VARCHAR(150) NOT NULL,
role VARCHAR(30) NOT NULL
);
CREATE TABLE books(
book_id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(100) NOT NULL,
author VARCHAR(100) NOT NULL,
category VARCHAR(100) NOT NULL,
total_quantity INT NOT NULL,
available_quantity INT NOT NULL,
borrowed_quantity INT NOT NULL,
borrow_price NUMERIC(10,2) NOT NULL,
purchase_price NUMERIC(10,2) NOT NULL
);

CREATE TABLE borrows(
borrow_id INT AUTO_INCREMENT PRIMARY KEY,
book_id INT NOT NULL,
user_id INT NOT NULL,
quantity INT NOT NULL,
remaining_quantity INT NOT NULL,
borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
due_date TIMESTAMP NOT NULL,
return_date TIMESTAMP DEFAULT NULL,
FOREIGN KEY(book_id) REFERENCES books(book_id)
ON DELETE RESTRICT ON UPDATE CASCADE,
FOREIGN KEY(user_id) REFERENCES users(user_id)
ON DELETE RESTRICT ON UPDATE CASCADE
);

-- يسجل كل مرة تشتري فيها المكتبة نسخًا جديدة من الكتب.
CREATE TABLE purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL, -- تكلفة الكتاب الواحد
    total_cost DECIMAL(10,2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    admin_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
	ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES users(user_id)
	ON DELETE RESTRICT ON UPDATE CASCADE
);

-- يسجل كل عملية شراء يقوم بها أحد الزبائن.
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL, -- سعر الكتاب الواحد عند بيعه للعميل
    total_amount DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
	ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
	ON DELETE RESTRICT ON UPDATE CASCADE
);