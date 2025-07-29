CREATE DATABASE LMS;
USE LMS;

CREATE TABLE Library (
     library_id INT PRIMARY KEY AUTO INCREMENT,
     name VARCHAR(50),
     campus_location VARCHAR(50),
     contact_email VARCHAR(50) UNIQUE,
     phone_number CHAR(10)
);
     
CREATE TABLE book (
     book_id INT PRIMARY KEY AUTO INCREMENT,
     title VARCHAR(50),
     isbn CHAR(13) UNIQUE,
     publication_date DATE,
     total_copies INT,
     available_copies INT,
     CHECK (available_copies <= total_copies)
);

DROP TABLE IF EXISTS Author;

CREATE TABLE Author (
     author_id INT PRIMARY KEY,
     first_name VARCHAR(50),
     last_name VARCHAR(50),
     birth_date DATE,
     nationality VARCHAR(50),
     biography TEXT
);
     
CREATE TABLE BookAuthor (
     book_id INT,
     author_id INT,
     PRIMARY KEY (book_id, author_id),
     FOREIGN KEY (book_id) REFERENCES Book (book_id),
     FOREIGN KEY (author_id) REFERENCES Author (author_id)
);


CREATE TABLE Category (
     category_id INT PRIMARY KEY AUTO INCREMENT,
     name VARCHAR(50),
     description TEXT 
);

CREATE TABLE BookCategory (
     book_id INT,
     category_id INT,
     PRIMARY KEY (book_id, category_id),
     FOREIGN KEY (book_id) REFERENCES Book (book_id),
     FOREIGN KEY (category_id) REFERENCES Category (category_id)
);

CREATE TABLE Member (
     member_id INT PRIMARY KEY AUTO INCREMENT,
     first_name VARCHAR(50),
     last_name VARCHAR(50),
     email VARCHAR(50) UNIQUE,
     phone_number CHAR(10),
     member_type VARCHAR(20),
     registration_date DATE 
);

CREATE TABLE Borrowing (
     borrowing_id INT PRIMARY KEY AUTO INCREMENT,
     member_id INT,
     book_id INT,
     borrow_date DATE,
     due_date DATE,
     return_date DATE,
     late_fee DECIMAL(6,2),
     CHECK (due_date > borrow_date),
     FOREIGN KEY (member_id) REFERENCES Member (member_id),
     FOREIGN KEY (book_id) REFERENCES Book (book_id)
);

CREATE TABLE Review(
     review_id INT PRIMARY KEY AUTO INCREMENT,
     member_id INT,
     book_id INT,
     rating INT CHECK (rating BETWEEN 1 AND 5),
     comment TEXT,
     review_date DATE,
     UNIQUE KEY (member_id, book_id),
     FOREIGN KEY (member_id) REFERENCES Member (member_id),
     FOREIGN KEY (book_id) REFERENCES Book (book_id)
);
