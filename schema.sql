CREATE DATABASE LMS;
USE LMS;

-- Create Library Table
CREATE TABLE Library (
    library_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    campus_location VARCHAR(100),
    contact_email VARCHAR(100),
    phone_number CHAR(10)
);

-- Create Category Table
CREATE TABLE Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Create Author Table
CREATE TABLE Author (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    bio TEXT
);

-- Create Book Table
CREATE TABLE Book (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    isbn CHAR(13) UNIQUE NOT NULL,
    published_year YEAR,
    total_copies INT DEFAULT 0,
    available_copies INT DEFAULT 0,
    category_id INT,
    library_id INT,
    CONSTRAINT chk_copies CHECK (available_copies <= total_copies),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (library_id) REFERENCES Library(library_id)
);

-- Create Member Table
CREATE TABLE Member (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone_number CHAR(10),
    member_type ENUM('Student', 'Faculty') NOT NULL
);

-- Create Book_Author Mapping Table
CREATE TABLE Book_Author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

-- Create Borrowing Table
CREATE TABLE Borrowing (
    borrowing_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    member_id INT,
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    CONSTRAINT chk_due_after_borrow CHECK (due_date > borrow_date),
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Create Review Table
CREATE TABLE Review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    member_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);


