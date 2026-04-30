# main.py
# This file serves as the User Interface (UI). 
# It handles user input and calls the functions defined in database.py.

import database as db

# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────
# These ensure the app doesn't crash if a user types text when a number is expected.

def get_int(prompt):
    """Loop until the user provides a valid integer."""
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("Please enter a whole number.")


def get_float(prompt):
    """Loop until the user provides a valid decimal/float."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number like 8.5")


# ── CREATE FUNCTIONS ───────────────────────────────────────────────────────────

def add_book():
    """Gathers book details from user and saves to DB."""
    print("\n-- Add a New Book --")
    title = input("Book title: ")

    # UI Step: Show available publishers so the user doesn't have to guess IDs
    publishers = db.get_all_publishers()
    print("\nAvailable publishers:")
    for pub in publishers:
        print(f"  ID {pub[0]}: {pub[1]}")
    
    publisher_id = get_int("Enter publisher ID: ")
    page_count = get_int("Page count: ")
    word_count = get_int("Word count: ")
    read_time = get_float("Estimated read time in hours: ")

    # Input validation for specific database ENUM or string constraints
    print("Depth options: broad, moderate, in-depth")
    depth = input("Depth level: ")
    while depth not in ["broad", "moderate", "in-depth"]:
        print("Please type: broad, moderate, or in-depth")
        depth = input("Depth level: ")

    rating = get_float("Approval rating (0-10): ")
    description = input("Short description: ")

    try:
        # Call the DB function and capture the new primary key
        new_id = db.add_book(title, publisher_id, page_count, word_count, read_time, depth, rating, description)
        print(f"Book added! Book ID is {new_id}")

        # Optional workflow: Link an author immediately after creating a book
        link = input("Do you want to link an author to this book? (yes/no): ")
        if link == "yes":
            authors = db.get_all_authors()
            print("\nAvailable authors:")
            for a in authors:
                print(f"  ID {a[0]}: {a[1]} {a[2]}")
            author_id = get_int("Enter author ID: ")
            db.link_book_author(new_id, author_id)

    except Exception as e:
        print("Error adding book:", e)


def add_author():
    """Gathers author details and saves to DB."""
    print("\n-- Add a New Author --")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    bio = input("Short bio: ")
    expertise = input("Field of expertise: ")
    credentials = input("Credentials: ")

    try:
        new_id = db.add_author(first_name, last_name, bio, expertise, credentials)
        print(f"Author added! Author ID is {new_id}")
    except Exception as e:
        print("Error adding author:", e)


# ── READ FUNCTIONS ─────────────────────────────────────────────────────────────

def show_all_books():
    """Displays all books formatted for the terminal."""
    print("\n-- All Books (sorted by rating) --")
    try:
        books = db.get_all_books()
        if not books:
            print("No books found.")
        for book in books:
            # book[0]=ID, [1]=Title, [2]=Rating, [3]=Depth, [4]=Hours
            print(f"  ID {book[0]} | {book[1]} | Rating: {book[2]} | {book[3]} | {book[4]} hrs")
    except Exception as e:
        print("Error loading books:", e)


def show_books_by_category():
    """Filters books by category name using user search string."""
    print("\n-- Search Books by Category --")
    category = input("Enter category name (e.g. Psychology, Habits): ")
    try:
        results = db.search_by_category(category)
        if not results:
            print(f"No books found in category: {category}")
        for row in results:
            print(f"  {row[0]} | Category: {row[1]} | Rating: {row[2]}")
    except Exception as e:
        print("Error searching by category:", e)


def show_books_by_rating():
    """
    NEW: Handles UI for 'Search by minimum rating'
    Asks the user for a number and displays matching books.
    """
    print("\n-- Search Books by Minimum Rating --")
    min_rating = get_float("Enter minimum rating (0-10): ")
    try:
        results = db.search_by_min_rating(min_rating)
        if not results:
            print(f"No books found with a rating of {min_rating} or higher.")
        for row in results:
            # row[0]=ID, [1]=Title, [2]=Rating, [3]=Depth
            print(f"  ID {row[0]} | {row[1]} | Rating: {row[2]} | Depth: {row[3]}")
    except Exception as e:
        print("Error searching by rating:", e)


def show_all_authors():
    """
    NEW: Handles UI for 'View all authors'
    Retrieves and prints a list of all authors in the database.
    """
    print("\n-- All Authors --")
    try:
        authors = db.get_all_authors()
        if not authors:
            print("No authors found in the database.")
        for a in authors:
            # a[0]=ID, [1]=First, [2]=Last, [3]=Expertise
            print(f"  ID {a[0]} | {a[1]} {a[2]} | Expertise: {a[3]}")
    except Exception as e:
        print("Error loading authors:", e)

        


# ── UPDATE FUNCTIONS ───────────────────────────────────────────────────────────

def update_book_rating():
    """Modifies the rating of an existing book."""
    print("\n-- Update Book Rating --")
    show_all_books() # Show list so user can see IDs
    book_id = get_int("Enter book ID to update: ")
    new_rating = get_float("Enter new rating (0-10): ")
    try:
        db.update_book_rating(book_id, new_rating)
        print("Rating updated.")
    except Exception as e:
        print("Error updating rating:", e)

def update_author_credentials():
    """
    Handles the UI for changing an author's credentials (e.g., adding 'PhD').
    1. Shows all authors so the user knows which ID to pick.
    2. Collects the ID and the new string.
    3. Sends it to the database.
    """
    print("\n-- Update Author Credentials --")
    
    # First, show the list so the user doesn't have to guess the ID
    show_all_authors()
    
    author_id = get_int("Enter author ID to update: ")
    new_creds = input("Enter new credentials (e.g., PhD, MD, Lead Researcher): ")
    
    try:
        # Call the function in database.py
        db.update_author_credentials(author_id, new_creds)
        print(f"Successfully updated credentials for Author ID {author_id}.")
    except Exception as e:
        print("Error updating credentials:", e)


# ── DELETE FUNCTIONS ───────────────────────────────────────────────────────────

def delete_book():
    """Removes a book after a manual confirmation step."""
    print("\n-- Delete a Book --")
    show_all_books()
    book_id = get_int("Enter book ID to delete: ")
    # Confirmation prevents accidental data loss
    confirm = input(f"Are you sure you want to delete book {book_id}? (yes/no): ")
    if confirm == "yes":
        try:
            db.delete_book(book_id)
            print("Book deleted.")
        except Exception as e:
            print("Error deleting book:", e)
    else:
        print("Deletion cancelled.")


def delete_author():
    """
    Handles the UI for removing an author from the database.
    1. Displays all authors so the user can identify the correct ID.
    2. Prompts for the ID.
    3. Asks for a final confirmation before calling the database.
    """
    print("\n-- Delete an Author --")
    
    # Show the list first so the user can see the IDs
    show_all_authors()
    
    author_id = get_int("Enter author ID to delete: ")
    
    # Safety check: Confirm the user actually wants to do this
    confirm = input(f"Are you sure you want to delete author ID {author_id}? (yes/no): ").lower()
    
    if confirm == "yes":
        try:
            # Call the delete function in database.py
            db.delete_author(author_id)
            print(f"Author ID {author_id} has been deleted.")
        except Exception as e:
            # This might fail if the author is still linked to books (Foreign Key constraint)
            print(f"Error deleting author: {e}")
    else:
        print("Deletion cancelled.")

# ── MENUS ──────────────────────────────────────────────────────────────────────
# These functions control the flow of the program using Infinite Loops (while True)

def create_menu():
    """Sub-menu for adding new records (Books and Authors)."""
    while True:
        print("\n-- Create Menu --")
        print("1. Add a new book")
        print("2. Add a new author")
        print("0. Back to Main Menu")
        choice = input("Choice: ")

        if choice == "1":
            add_book()    # Calls the UI function for adding books
        elif choice == "2":
            add_author()  # Calls the UI function for adding authors
        elif choice == "0":
            break         # Returns to the main() loop
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")

def read_menu():
    """Sub-menu for all 'Read' operations."""
    while True:
        print("\n-- Read Menu --")
        print("1. View all books")
        print("2. Search by category")
        print("3. Search by minimum rating") # Added option 3
        print("4. View all authors")        # Added option 4
        print("0. Back")
        choice = input("Choice: ")

        if choice == "1":
            show_all_books()
        elif choice == "2":
            show_books_by_category()
        elif choice == "3":
            # Calls the function that asks for a rating and filters the list
            show_books_by_rating()
        elif choice == "4":
            # Calls the function that lists all authors in the DB
            show_all_authors()
        elif choice == "0":
            break # Exit the loop to go back to the main menu
        else:
            print("Invalid choice. Please select 0-4.")

def update_menu():
    """Sub-menu for modifying existing records."""
    while True:
        print("\n-- Update Menu --")
        print("1. Update book rating")
        print("2. Update author credentials")
        print("0. Back to Main Menu")
        choice = input("Choice: ")

        if choice == "1":
            update_book_rating()
        elif choice == "2":
            update_author_credentials()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")

def delete_menu():
    """Sub-menu for removing records from the database."""
    while True:
        print("\n-- Delete Menu --")
        print("1. Delete a book")
        print("2. Delete an author")
        print("0. Back to Main Menu")
        choice = input("Choice: ")

        if choice == "1":
            delete_book()
        elif choice == "2":
            delete_author()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")

def main():
    """The entry point of the application."""
    print("Welcome to the Book Tracker!")

    # Initial Health Check: Can we even talk to the DB?
    try:
        conn = db.get_connection()
        if conn is None:
            raise Exception("Connection returned None")
        conn.close()
        print("Connected to database successfully.")
    except Exception as e:
        print("Could not connect to the database.")
        print("Check if Docker is running.")
        return # Kill the app if no DB connection

    # Main Navigation Loop
    while True:
        print("\n===== MAIN MENU =====")
        print("C - Create (add books/authors)")
        print("R - Read   (search/view)")
        print("U - Update (edit records)")
        print("D - Delete (remove records)")
        print("Q - Quit")
        choice = input("Choice: ").lower()

        if choice == "c":
            create_menu()
        elif choice == "r":
            read_menu()
        elif choice == "u":
            update_menu()
        elif choice == "d":
            delete_menu()
        elif choice == "q":
            print("Goodbye!")
            break # Breaks the main loop and ends the script
        else:
            print("Invalid choice. Press C, R, U, D, or Q.")

# Ensure the app starts only if this file is run directly
if __name__ == "__main__":
    main()