--  Demonstration Queries for Book Tracker Database


-- 1. Relational Mapping (The "Master View")
-- Capability: Joining multiple tables (1:M and M:M) to turn raw IDs into a human-readable report.
SELECT 
    b.title, 
    CONCAT(a.first_name, ' ', a.last_name) AS author,
    p.name AS publisher,
    b.depth_level
FROM book b
JOIN book_author ba ON b.book_id = ba.book_id
JOIN author a ON ba.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
ORDER BY b.title ASC;

-- 2. Navigating Many-to-Many Relationships
-- Capability: Filtering data based on a junction table. Finds all books belonging to 'Psychology'.
SELECT b.title, c.name AS category_name
FROM book b
JOIN book_category bc ON b.book_id = bc.book_id
JOIN category c ON bc.category_id = c.category_id
WHERE c.name = 'Psychology';

-- 3. Business Intelligence (Aggregation)
-- Capability: Summarizing data (counts and averages) grouped by a specific entity.
SELECT 
    p.name AS publisher, 
    COUNT(b.book_id) AS book_count, 
    ROUND(AVG(b.approval_rating), 2) AS avg_rating
FROM publisher p
JOIN book b ON p.publisher_id = b.publisher_id
GROUP BY p.name
HAVING book_count > 0;

-- 4. Computed Metrics (Calculated Columns)
-- Capability: Performing math on the fly (Words per Hour) to help users choose intensity.
SELECT 
    title, 
    word_count, 
    read_time_hours,
    (word_count / read_time_hours) AS words_per_hour
FROM book
WHERE word_count IS NOT NULL AND read_time_hours > 0
ORDER BY words_per_hour DESC;

-- 5. Advanced List Aggregation (GROUP_CONCAT)
-- Capability: Flattening multiple rows into one comma-separated string for easy viewing.
SELECT 
    b.title, 
    GROUP_CONCAT(c.name SEPARATOR ', ') AS categories
FROM book b
JOIN book_category bc ON b.book_id = bc.book_id
JOIN category c ON bc.category_id = c.category_id
GROUP BY b.book_id;

-- 6. Search & Pattern Matching
-- Capability: Unstructured data retrieval using wildcards.
SELECT first_name, last_name, field_of_expertise, bio
FROM author
WHERE bio LIKE '%research%' OR field_of_expertise LIKE '%Psychology%';

-- 7. Data Integrity Validation (Null Handling)
-- Capability: Identifying rows with missing critical data (orphans).
SELECT title, publisher_id, page_count
FROM book
WHERE publisher_id IS NULL OR page_count IS NULL;

-- 8. Cross-Reference Analysis
-- Capability: Complex logic checking for topical authority (Expertise matches Category).
SELECT 
    b.title, 
    CONCAT(a.first_name, ' ', a.last_name) AS author,
    a.field_of_expertise,
    c.name AS book_category
FROM book b
JOIN book_author ba ON b.book_id = ba.book_id
JOIN author a ON ba.author_id = a.author_id
JOIN book_category bc ON b.book_id = bc.book_id
JOIN category c ON bc.category_id = c.category_id
WHERE a.field_of_expertise = c.name;
