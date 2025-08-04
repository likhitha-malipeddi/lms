SELECT * FROM Library
SELECT * FROM Author
SELECT * FROM Category
SELECT * FROM book
SELECT * FROM Member
SELECT * FROM Borrowing
SELECT * FROM Review

-- Books with their authors and categories
SELECT 
    b.title,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name)) AS author,
    GROUP_CONCAT(DISTINCT c.name) AS category
FROM Book b
LEFT JOIN BookAuthor ba ON b.book_id = ba.book_id
LEFT JOIN Author a ON ba.author_id = a.author_id
LEFT JOIN BookCategory bc ON b.book_id = bc.book_id
LEFT JOIN Category c ON bc.category_id = c.category_id
GROUP BY b.book_id;

-- Most borrowed books in the last 30 days
SELECT book_id, COUNT(*) AS borrow_count
FROM Borrowing
WHERE borrow_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY book_id
ORDER BY borrow_count DESC
LIMIT 5;

-- Members with overdue books and calculated late fees
SELECT 
    m.first_name,
    m.last_name,
    b.title,
    br.due_date,
    br.return_date,
    br.late_fee
FROM Borrowing br
JOIN Member m ON br.member_id = m.member_id
JOIN Book b ON br.book_id = b.book_id
WHERE br.return_date > br.due_date;

-- Average rating per book with author information
SELECT 
    b.title,
    ROUND(AVG(r.rating), 2) AS average_rating,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name)) AS authors
FROM Review r
JOIN Book b ON r.book_id = b.book_id
LEFT JOIN BookAuthor ba ON b.book_id = ba.book_id
LEFT JOIN Author a ON ba.author_id = a.author_id
GROUP BY b.book_id;

-- Books available in each library with stock levels
SELECT 
    L.name AS Library_name,
    b.title,
    b.total_copies,
    b.available_copies
FROM Book b
JOIN Library L ON b.Library_id = L.Library_id
ORDER BY L.name, b.title;

-- count
SELECT 
    member_type,
    COUNT(*) AS total_members
FROM Member
GROUP BY member_type;

-- avg
SELECT 
    b.title,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM Review r
JOIN Book b ON r.book_id = b.book_id
GROUP BY b.book_id;

-- sum
SELECT 
    m.first_name,
    m.last_name,
    SUM(b.late_fee) AS total_late_fee
FROM Borrowing b
JOIN Member m ON b.member_id = m.member_id
GROUP BY b.member_id;

-- subquery
SELECT 
    b.title,
    r.rating
FROM Review r
JOIN Book b ON r.book_id = b.book_id
WHERE r.rating > (
    SELECT AVG(rating)
    FROM Review
);


-- CTE: Top 3 most reviewed books
WITH ReviewCount AS (
    SELECT 
        book_id, 
        COUNT(*) AS review_count
    FROM Review
    GROUP BY book_id
)
SELECT 
    b.title,
    rc.review_count
FROM ReviewCount rc
JOIN Book b ON b.book_id = rc.book_id
ORDER BY rc.review_count DESC
LIMIT 3;

-- Window Function: Late fee ranking per member
SELECT 
    member_id,
    book_id,
    late_fee,
    RANK() OVER (PARTITION BY member_id ORDER BY late_fee DESC) AS late_fee_rank
FROM Borrowing
WHERE late_fee > 2;

-- Start a transaction to borrow a book and update available copies
START TRANSACTION;

INSERT INTO Borrowing(
     member_id, 
     book_id, 
     borrow_date, 
     due_date, 
     return_date
)
VALUES (
    3, 
    5, 
    CURDATE(), 
    DATE_ADD(CURDATE(), INTERVAL 14 DAY), 
    NULL
);

UPDATE Book
SET available_copies = available_copies - 1
WHERE book_id = 5 AND available_copies > 0;

COMMIT;



     

