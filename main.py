"""
Library Management System - Main Entry Point
A console-based library management system for managing books and borrowers.
"""

from src.library import Library
from datetime import datetime


def print_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Book Management")
    print("2. Borrower Management")
    print("3. Borrow/Return Books")
    print("4. Search Books")
    print("5. View All Books")
    print("6. View All Borrowers")
    print("7. View Borrower's Books")
    print("8. View Overdue Books")
    print("0. Exit")
    print("="*50)


def book_management_menu(library):
    """Handle book management operations."""
    while True:
        print("\n--- BOOK MANAGEMENT ---")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. View Book Details")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            print("\n--- ADD NEW BOOK ---")
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            isbn = input("Enter ISBN: ").strip()
            genre = input("Enter genre: ").strip()
            try:
                quantity = int(input("Enter quantity (default: 1): ").strip() or "1")
            except ValueError:
                quantity = 1
            
            if library.add_book(title, author, isbn, genre, quantity):
                print(f"\n✓ Book '{title}' added successfully!")
            else:
                print(f"\n✗ Error: Book with ISBN {isbn} already exists.")
        
        elif choice == '2':
            print("\n--- UPDATE BOOK ---")
            isbn = input("Enter ISBN of the book to update: ").strip()
            
            print("Leave fields empty to keep current values:")
            title = input("Enter new title (or press Enter to skip): ").strip() or None
            author = input("Enter new author (or press Enter to skip): ").strip() or None
            genre = input("Enter new genre (or press Enter to skip): ").strip() or None
            quantity_str = input("Enter new quantity (or press Enter to skip): ").strip()
            quantity = int(quantity_str) if quantity_str else None
            
            if library.update_book(isbn, title, author, genre, quantity):
                print(f"\n✓ Book updated successfully!")
            else:
                print(f"\n✗ Error: Book not found or invalid update.")
        
        elif choice == '3':
            print("\n--- REMOVE BOOK ---")
            isbn = input("Enter ISBN of the book to remove: ").strip()
            
            if library.remove_book(isbn):
                print(f"\n✓ Book removed successfully!")
            else:
                print(f"\n✗ Error: Book not found or has borrowed copies.")
        
        elif choice == '4':
            print("\n--- VIEW BOOK DETAILS ---")
            isbn = input("Enter ISBN: ").strip()
            availability = library.get_book_availability(isbn)
            
            if availability:
                print(f"\nBook Details:")
                print(f"  Title: {availability['title']}")
                print(f"  Author: {availability['author']}")
                print(f"  Total Copies: {availability['total_copies']}")
                print(f"  Available: {availability['available_copies']}")
                print(f"  Borrowed: {availability['borrowed_copies']}")
            else:
                print(f"\n✗ Book not found.")
        
        elif choice == '0':
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


def borrower_management_menu(library):
    """Handle borrower management operations."""
    while True:
        print("\n--- BORROWER MANAGEMENT ---")
        print("1. Add Borrower")
        print("2. Update Borrower")
        print("3. Remove Borrower")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            print("\n--- ADD NEW BORROWER ---")
            name = input("Enter borrower name: ").strip()
            membership_id = input("Enter membership ID: ").strip()
            contact = input("Enter contact info (optional): ").strip() or None
            
            if library.add_borrower(name, membership_id, contact):
                print(f"\n✓ Borrower '{name}' added successfully!")
            else:
                print(f"\n✗ Error: Borrower with membership ID {membership_id} already exists.")
        
        elif choice == '2':
            print("\n--- UPDATE BORROWER ---")
            membership_id = input("Enter membership ID: ").strip()
            
            print("Leave fields empty to keep current values:")
            name = input("Enter new name (or press Enter to skip): ").strip() or None
            contact = input("Enter new contact (or press Enter to skip): ").strip() or None
            
            if library.update_borrower(membership_id, name, contact):
                print(f"\n✓ Borrower updated successfully!")
            else:
                print(f"\n✗ Error: Borrower not found.")
        
        elif choice == '3':
            print("\n--- REMOVE BORROWER ---")
            membership_id = input("Enter membership ID: ").strip()
            
            if library.remove_borrower(membership_id):
                print(f"\n✓ Borrower removed successfully!")
            else:
                print(f"\n✗ Error: Borrower not found or has active borrowings.")
        
        elif choice == '0':
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


def borrow_return_menu(library):
    """Handle book borrowing and returning operations."""
    while True:
        print("\n--- BORROW/RETURN BOOKS ---")
        print("1. Borrow Book")
        print("2. Return Book")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            print("\n--- BORROW BOOK ---")
            membership_id = input("Enter membership ID: ").strip()
            isbn = input("Enter ISBN of the book: ").strip()
            
            try:
                days = int(input("Enter loan period in days (default: 14): ").strip() or "14")
            except ValueError:
                days = 14
            
            success, message = library.borrow_book(membership_id, isbn, days)
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
        
        elif choice == '2':
            print("\n--- RETURN BOOK ---")
            membership_id = input("Enter membership ID: ").strip()
            isbn = input("Enter ISBN of the book: ").strip()
            
            success, message = library.return_book(membership_id, isbn)
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
        
        elif choice == '0':
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


def search_books_menu(library):
    """Handle book search operations."""
    print("\n--- SEARCH BOOKS ---")
    print("Search by:")
    print("1. Title")
    print("2. Author")
    print("3. Genre")
    
    search_type = input("\nEnter your choice: ").strip()
    search_by_map = {'1': 'title', '2': 'author', '3': 'genre'}
    
    if search_type not in search_by_map:
        print("\n✗ Invalid choice.")
        return
    
    query = input(f"Enter {search_by_map[search_type]} to search: ").strip()
    results = library.search_books(query, search_by_map[search_type])
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        print("-" * 60)
        for book in results:
            print(f"  {book}")
            print(f"    Genre: {book.genre}")
            print(f"    Available: {book.available_copies}/{book.quantity} copies")
            print("-" * 60)
    else:
        print(f"\n✗ No books found matching '{query}'.")


def view_all_books(library):
    """Display all books in the library."""
    books = library.get_all_books()
    
    if not books:
        print("\n✗ No books in the library.")
        return
    
    print(f"\n--- ALL BOOKS ({len(books)} total) ---")
    print("-" * 60)
    for book in books:
        print(f"  {book}")
        print(f"    Genre: {book.genre}")
        print("-" * 60)


def view_all_borrowers(library):
    """Display all borrowers in the system."""
    borrowers = library.get_all_borrowers()
    
    if not borrowers:
        print("\n✗ No borrowers in the system.")
        return
    
    print(f"\n--- ALL BORROWERS ({len(borrowers)} total) ---")
    print("-" * 60)
    for borrower in borrowers:
        print(f"  {borrower}")
        print(f"    Active Borrowings: {len(borrower.borrowed_books)}")
        print("-" * 60)


def view_borrower_books(library):
    """Display books borrowed by a specific borrower."""
    print("\n--- VIEW BORROWER'S BOOKS ---")
    membership_id = input("Enter membership ID: ").strip()
    
    books = library.get_borrower_books(membership_id)
    
    if books is None:
        print("\n✗ Borrower not found.")
        return
    
    if not books:
        print(f"\n✓ No books currently borrowed.")
        return
    
    print(f"\n--- BORROWED BOOKS ---")
    print("-" * 60)
    for book_info in books:
        due_date = book_info['due_date'].strftime('%Y-%m-%d')
        is_overdue = book_info['due_date'] < datetime.now()
        status = "OVERDUE" if is_overdue else "On Time"
        print(f"  Title: {book_info['title']}")
        print(f"  ISBN: {book_info['isbn']}")
        print(f"  Due Date: {due_date} [{status}]")
        print("-" * 60)


def view_overdue_books(library):
    """Display all overdue books across all borrowers."""
    print("\n--- OVERDUE BOOKS ---")
    
    all_overdue = []
    for borrower in library.get_all_borrowers():
        overdue = borrower.get_overdue_books()
        for isbn, title, due_date in overdue:
            all_overdue.append({
                'borrower': borrower.name,
                'membership_id': borrower.membership_id,
                'isbn': isbn,
                'title': title,
                'due_date': due_date
            })
    
    if not all_overdue:
        print("\n✓ No overdue books.")
        return
    
    print(f"\nFound {len(all_overdue)} overdue book(s):")
    print("-" * 60)
    for item in all_overdue:
        print(f"  Borrower: {item['borrower']} (ID: {item['membership_id']})")
        print(f"  Book: {item['title']} (ISBN: {item['isbn']})")
        print(f"  Due Date: {item['due_date'].strftime('%Y-%m-%d')}")
        print("-" * 60)


def main():
    """Main program entry point."""
    library = Library()
    
    print("Welcome to the Library Management System!")
    print("This system helps you manage books, borrowers, and borrowing transactions.")
    
    # Add some sample data for demonstration
    print("\nLoading sample data...")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5", "Fiction", 3)
    library.add_book("1984", "George Orwell", "978-0-452-28423-4", "Dystopian", 2)
    library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4", "Fiction", 2)
    library.add_borrower("John Doe", "MEM001", "john.doe@email.com")
    library.add_borrower("Jane Smith", "MEM002", "jane.smith@email.com")
    print("Sample data loaded!")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            book_management_menu(library)
        elif choice == '2':
            borrower_management_menu(library)
        elif choice == '3':
            borrow_return_menu(library)
        elif choice == '4':
            search_books_menu(library)
        elif choice == '5':
            view_all_books(library)
        elif choice == '6':
            view_all_borrowers(library)
        elif choice == '7':
            view_borrower_books(library)
        elif choice == '8':
            view_overdue_books(library)
        elif choice == '0':
            print("\nThank you for using the Library Management System. Goodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()