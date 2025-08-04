USE LMS;

START TRANSACTION;

INSERT INTO library (name, campus_location, contact_email, phone_number) VALUES
                    ('Central Library', 'Main Campus', 'East@library.com', '1234567890'),
                    ('Science Library', 'North Wing', 'North@library.com', '2468013579'),
                    ('Arts Library', 'South Wing', 'South@library.com', '3216549870');

INSERT INTO Author (first_name, last_name, birth_date, nationality, biography) VALUES
                   ('George', 'Orwell', '1903-06-25', 'British', 'George Orwell was an English novelist and essayist, known for works like 1984 and Animal Farm.'),
                   ('Jane', 'Austen', '1775-12-16', 'British', 'Jane Austen was an English novelist known for her six major novels, including Pride and Prejudice.'),
                   ('Joanne', 'Rowling', '1965-07-31', 'British', 'J.K. Rowling is the author of the Harry Potter fantasy series.'),
                   ('Stephen', 'Hawking', '1942-01-08', 'British', 'Stephen Hawking was a theoretical physicist known for his work on black holes and relativity.'),
                   ('Isaac', 'Asimov', '1920-01-02', 'American', 'Isaac Asimov was a science fiction writer and biochemist, best known for the Foundation series.'),
                   ('Agatha', 'Christie', '1890-09-15', 'British', 'Agatha Christie is the best-selling mystery writer of all time, known for characters like Hercule Poirot.'),
                   ('Mark', 'Twain', '1835-11-30', 'American', 'Mark Twain was an American writer and humorist, author of Tom Sawyer and Huckleberry Finn.'),
                   ('Ernest', 'Hemingway', '1899-07-21', 'American', 'Ernest Hemingway was an American novelist and short-story writer, known for The Old Man and the Sea.');

COMMIT;

START TRANSACTION;

INSERT INTO Category (Name, Description) VALUES
                     ('Fiction', 'Literary works invented by the imagination, such as novels or short stories.'),
                     ('Science', 'Books related to scientific topics, discoveries, and theories.'),
                     ('Mystery', 'Fiction dealing with the solution of a crime or the unraveling of secrets.'),
                     ('History', 'Books about historical events, people, and places.'),
                     ('Fantasy', 'Fiction with magical or supernatural elements set in imaginary worlds.');

COMMIT;

START TRANSACTION;

INSERT INTO book (title, isbn, publication_date, total_copies, available_copies, library_id) VALUES
                 ('1984', '9780451524935', '1949-06-08', 10, 6, 1),
                 ('Pride and Prejudice', '9780141439518', '1813-01-28', 8, 5, 1),
                 ('Harry Potter and the Sorcerer\'s Stone', '9780590353427', '1997-06-26', 12, 7, 1),
                 ('A Brief History of Time', '9780553380163', '1988-04-01', 6, 3, 2),
                 ('Foundation', '9780553293357', '1951-06-01', 9, 6, 2),
                 ('Murder on the Orient Express', '9780062073495', '1934-01-01', 7, 4, 2),
                 ('The Adventures of Tom Sawyer', '9780143039563', '1876-06-01', 5, 2, 3),
                 ('The Old Man and the Sea', '9780684801223', '1952-09-01', 5, 3, 3),
                 ('Emma', '9780141439587', '1815-12-23', 6, 4, 1),
                 ('Harry Potter and the Chamber of Secrets', '9780439064873', '1998-07-02', 10, 8, 1),
                 ('The Universe in a Nutshell', '9780553802023', '2001-11-06', 4, 2, 2),
                 ('I, Robot', '9780553294385', '1950-12-02', 6, 4, 2),
                 ('And Then There Were None', '9780062073488', '1939-11-06', 8, 5, 2),
                 ('Adventures of Huckleberry Finn', '9780143107323', '1884-12-10', 7, 3, 3),
                 ('The Sun Also Rises', '9780743297332', '1926-10-22', 5, 1, 3);

COMMIT;

START TRANSACTION;

INSERT INTO Member (first_name, last_name, email, phone, member_type, registration_date) VALUES
                   ('Alice', 'Smith', 'alice.smith@example.edu', '5551001', 'Student', '2024-09-01'),
                   ('Bob', 'Johnson', 'bob.johnson@example.edu', '5551002', 'Faculty', '2022-01-15'),
                   ('Charlie', 'Rose', 'charlie.rose@example.edu', '5551003', 'Student', '2024-10-10'),
                   ('Dana', 'Lee', 'dana.lee@example.edu', '5551004', 'Faculty', '2021-08-25'),
                   ('Evan', 'Kim', 'evan.kim@example.edu', '5551005', 'Student', '2024-09-12'),
                   ('Fiona', 'Zhang', 'fiona.zhang@example.edu', '5551006', 'Faculty', '2023-03-05'),
                   ('George', 'White', 'george.white@example.edu', '5551007', 'Student', '2023-11-18'),
                   ('Helen', 'Black', 'helen.black@example.edu', '5551008', 'Faculty', '2022-05-30'),
                   ('Ian', 'Brown', 'ian.brown@example.edu', '5551009', 'Student', '2024-01-07'),
                   ('Jane', 'Green', 'jane.green@example.edu', '5551010', 'Faculty', '2020-09-14'),
                   ('Kyle', 'Blue', 'kyle.blue@example.edu', '5551011', 'Student', '2024-09-15'),
                   ('Laura', 'Red', 'laura.red@example.edu', '5551012', 'Faculty', '2023-02-10'),
                   ('Mike', 'Orange', 'mike.orange@example.edu', '5551013', 'Student', '2024-08-20'),
                   ('Nina', 'Purple', 'nina.purple@example.edu', '5551014', 'Faculty', '2022-03-12'),
                   ('Oscar', 'Cyan', 'oscar.cyan@example.edu', '5551015', 'Student', '2023-10-01'),
                   ('Paula', 'Grey', 'paula.grey@example.edu', '5551016', 'Faculty', '2021-12-22'),
                   ('Quincy', 'Silver', 'quincy.silver@example.edu', '5551017', 'Student', '2024-04-04'),
                   ('Rachel', 'Gold', 'rachel.gold@example.edu', '5551018', 'Faculty', '2022-07-07'),
                   ('Steve', 'Copper', 'steve.copper@example.edu', '5551019', 'Student', '2024-05-10'),
                   ('Tina', 'Bronze', 'tina.bronze@example.edu', '5551020', 'Faculty', '2023-06-28');

COMMIT;

START TRANSACTION;

INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee) VALUES
                      (1, 3, '2025-06-01', '2025-06-15', '2025-06-14', 0.00),
                      (2, 4, '2025-06-02', '2025-06-16', '2025-06-18', 1.00),
                      (3, 5, '2025-06-03', '2025-06-17', NULL, 0.00),
                      (4, 6, '2025-06-04', '2025-06-18', '2025-06-20', 2.00),
                      (5, 7, '2025-06-05', '2025-06-19', NULL, 0.00),
                      (6, 1, '2025-06-06', '2025-06-20', '2025-06-20', 0.00),
                      (7, 2, '2025-06-07', '2025-06-21', NULL, 0.00),
                      (8, 8, '2025-06-08', '2025-06-22', '2025-06-25', 3.00),
                      (9, 9, '2025-06-09', '2025-06-23', '2025-06-23', 0.00),
                      (10, 10, '2025-06-10', '2025-06-24', NULL, 0.00),
                      (11, 11, '2025-06-11', '2025-06-25', NULL, 0.00),
                      (12, 12, '2025-06-12', '2025-06-26', NULL, 0.00),
                      (13, 13, '2025-06-13', '2025-06-27', NULL, 0.00),
                      (14, 14, '2025-06-14', '2025-06-28', NULL, 0.00),
                      (15, 15, '2025-06-15', '2025-06-29', NULL, 0.00),
                      (16, 3, '2025-06-16', '2025-06-30', NULL, 0.00),
                      (17, 4, '2025-06-17', '2025-07-01', NULL, 0.00),
                      (18, 5, '2025-06-18', '2025-07-02', NULL, 0.00),
                      (19, 6, '2025-06-19', '2025-07-03', NULL, 0.00),
                      (20, 7, '2025-06-20', '2025-07-04', NULL, 0.00),
                      (21, 1, '2025-06-21', '2025-07-05', NULL, 0.00),
                      (2, 2, '2025-06-22', '2025-07-06', NULL, 0.00),
                      (3, 3, '2025-06-23', '2025-07-07', NULL, 0.00),
                      (4, 4, '2025-06-24', '2025-07-08', NULL, 0.00),
                      (5, 5, '2025-06-25', '2025-07-09', NULL, 0.00);
COMMIT;

START TRANSACTION;

INSERT INTO Review (member_id, book_id, rating, comment, review_date) VALUES
                   (1, 3, 5, 'Amazing book, very insightful!', '2025-07-01'),
                   (2, 4, 4, 'Great read, but a bit lengthy.', '2025-07-02'),
                   (3, 5, 3, 'Interesting concepts but hard to follow.', '2025-07-03'),
                   (4, 6, 5, 'Excellent reference material.', '2025-07-04'),
                   (5, 7, 4, 'Well written and informative.', '2025-07-05'),
                   (6, 1, 2, 'Not what I expected, somewhat boring.', '2025-07-06'),
                   (7, 2, 5, 'Loved it! Highly recommend.', '2025-07-07'),
                   (8, 8, 3, 'Average, some parts were slow.', '2025-07-08'),
                   (9, 9, 4, 'Good explanations and examples.', '2025-07-09'),
                   (10, 10, 5, 'Fantastic book, very useful.', '2025-07-10'),
                   (11, 11, 1, 'Did not like the writing style.', '2025-07-11'),
                   (12, 12, 4, 'Helpful and well structured.', '2025-07-12');
COMMIT;


