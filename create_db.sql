CREATE DATABASE amazon_review_intelligence;
USE amazon_review_intelligence;

CREATE TABLE Customer (
    customer_id VARCHAR(100) PRIMARY KEY,
    full_name VARCHAR(300) NOT NULL,
    email VARCHAR(200),
    phone VARCHAR(20),
    created_at DATE
);

CREATE TABLE Product (
    product_id VARCHAR(100) PRIMARY KEY,
    product_name VARCHAR(300) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT
);

CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(200) NOT NULL
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(100),
    order_date DATE NOT NULL,
    status VARCHAR(100),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Payment (
    payment_id INT PRIMARY KEY,
    order_id INT UNIQUE,
    payment_method VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Review (
    review_id VARCHAR(100) PRIMARY KEY,
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    rating INT NOT NULL,
    review_text VARCHAR(1000),
    review_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE Order_Item (
    order_id INT,
    product_id VARCHAR(100),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE Product_Category (
    product_id VARCHAR(100),
    category_id INT,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);