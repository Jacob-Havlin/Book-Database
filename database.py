import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Establishes a connection to the MySQL database running inside Docker.
    Returns the connection object if successful, otherwise returns None.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",   # Host machine address (Docker maps this to the container)
            user="root",
            password="password",
            database="book_tracker"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: Could not connect to database. {e}")
        return None

# --- CREATE OPERATIONS ---

def add_book(title, publisher_id, page_count, word_count, read_time_hours, depth_level, approval_rating, description):
    """Inserts a new book record into the 'book' table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # We use %s placeholders to prevent SQL Injection attacks
    sql = """
        INSERT INTO book (title, publisher_id, page_count, word_count, read_time_hours, depth_level, approval_rating, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (title, publisher_id, page_count, word_count, read_time_hours, depth_level, approval_rating, description))
    
    # commit() is required to save changes to the database
    conn.commit()
    
    # Retrieve the auto-generated ID of the newly inserted row
    new_id = cursor.lastrowid
    
    # Always close the cursor and connection to free up resources
    cursor.close()
    conn.close()
    return new_id


def add_author(first_name, last_name, bio, field_of_expertise, credentials):
    """Inserts a new author record and returns the new author's ID."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO author (first_name, last_name, bio, field_of_expertise, credentials)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (first_name, last_name, bio, field_of_expertise, credentials))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def link_book_author(book_id, author_id):
    """
    Creates a relationship in the bridge table (book_author).
    Uses a Transaction (try/except) to ensure the data stays consistent.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (%s, %s)", (book_id, author_id))
        conn.commit()
        print("Book and author linked successfully.")
    except Exception as e:
        # If the insert fails, rollback() cancels any partial changes
        conn.rollback()
        print("Something went wrong. Changes were undone.")
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()


# --- READ OPERATIONS ---

def get_all_books():
    """Retrieves all books, sorted by highest approval rating."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, approval_rating, depth_level, read_time_hours FROM book ORDER BY approval_rating DESC")
    
    # fetchall() returns a list of tuples representing the rows
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_by_category(category_name):
    """Joins three tables to find books belonging to a specific category name."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT b.title, c.name, b.approval_rating
        FROM book b
        JOIN book_category bc ON b.book_id = bc.book_id
        JOIN category c ON bc.category_id = c.category_id
        WHERE c.name LIKE %s
    """
    # The comma in ("%" + category_name + "%",) is required to make it a tuple
    cursor.execute(sql, ("%" + category_name + "%",))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_by_min_rating(min_rating):
    """Filters books based on a minimum numeric rating."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, approval_rating, depth_level FROM book WHERE approval_rating >= %s ORDER BY approval_rating DESC", (min_rating,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_all_authors():
    """Retrieves basic author info sorted alphabetically by last name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author_id, first_name, last_name, field_of_expertise FROM author ORDER BY last_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_all_publishers():
    """Retrieves a list of all publishers available in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT publisher_id, name FROM publisher ORDER BY name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
    


# --- UPDATE OPERATIONS ---

def update_book_rating(book_id, new_rating):
    """Updates the approval rating of an existing book."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE book SET approval_rating = %s WHERE book_id = %s", (new_rating, book_id))
    conn.commit()  # Changes won't be visible in the DB without commit
    cursor.close()
    conn.close()


def update_author_credentials(author_id, new_credentials):
    """Updates the credentials (e.g., PhD, PE) for a specific author."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE author SET credentials = %s WHERE author_id = %s", (new_credentials, author_id))
    conn.commit()
    cursor.close()
    conn.close()


# --- DELETE OPERATIONS ---

def delete_book(book_id):
    """Permanently removes a book from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM book WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()


def delete_author(author_id):
    """Permanently removes an author from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM author WHERE author_id = %s", (author_id,))
    conn.commit()
    cursor.close()
    conn.close()