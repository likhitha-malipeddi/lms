CREATE DATABASE LMS;
USE LMS;

CREATE TABLE Librar (
     library_id INT PRIMARY KEY,
     name VARCHAR(50),
     campus_location VARCHAR(50),
     contact_email VARCHAR(50) UNIQUE,
     phone_number VARCHAR(20)
);
     
CREATE TABLE book (
     book_id INT PRIMARY KEY,
     title VARCHAR(50),
     isbn VARCHAR(50) UNIQUE,
     publication_date DATE,
     total_copies INT,
     available_copies INT,
     library_id INT,
     FOREIGN KEY(library_id) REFERENCES librar(library_id)
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
     FOREIGN KEY (book_id) REFERENCES book (book_id),
     FOREIGN KEY (author_id) REFERENCES author (author_id)
);


CREATE TABLE Category (
     category_id INT PRIMARY KEY,
     name VARCHAR(50),
     description TEXT, 
);

CREATE TABLE BookCategory (
     book_id INT,
     category_id INT,
     PRIMARY KEY (book_id, category_id),
     FOREIGN KEY (book_id) REFERENCES book (book_id),
     FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE Member (
     member_id INT PRIMARY KEY,
     first_name VARCHAR(50),
     last_name VARCHAR(50),
     email VARCHAR(50) UNIQUE,
     phone VARCHAR(20),
     member_type VARCHAR(20),
     registration_date DATE, 
);

CREATE TABLE Borrowing (
     borrowing_id INT PRIMARY KEY,
     member_id INT,
     book_id INT,
     borrow_date DATE,
     due_date DATE,
     return_date DATE,
     late_fee DECIMAL(6,2),
     FOREIGN KEY (member_id) REFERENCES member (member_id),
     FOREIGN KEY (book_id) REFERENCES book (book_id)
);

CREATE TABLE Review(
     review_id INT PRIMARY KEY,
     member_id INT,
     book_id INT,
     rating INT CHECK (rating BETWEEN 1 AND 5),
     comment TEXT,
     review_date DATE,
     UNIQUE KEY (member_id, book_id),
     FOREIGN KEY (member_id) REFERENCES member (member_id),
     FOREIGN KEY (book_id) REFERENCES book (book_id)
);
