from datetime import datetime, timedelta
from .book import Book
from .borrower import Borrower


class Library:
    """Main library management system class."""
    
    def __init__(self):
        """Initialize the library with empty collections."""
        self.books = {}  # Dictionary: {isbn: Book object}
        self.borrowers = {}  # Dictionary: {membership_id: Borrower object}
        self.borrowing_records = {}  # Dictionary: {(membership_id, isbn): due_date}
    
    # Book Management Methods
    def add_book(self, title, author, isbn, genre, quantity=1):
        """
        Add a new book to the library.
        
        Args:
            title (str): Title of the book
            author (str): Author of the book
            isbn (str): ISBN number
            genre (str): Genre of the book
            quantity (int): Number of copies (default: 1)
            
        Returns:
            bool: True if added successfully, False if ISBN already exists
        """
        if isbn in self.books:
            return False
        self.books[isbn] = Book(title, author, isbn, genre, quantity)
        return True
    
    def update_book(self, isbn, title=None, author=None, genre=None, quantity=None):
        """
        Update book information.
        
        Args:
            isbn (str): ISBN of the book to update
            title (str, optional): New title
            author (str, optional): New author
            genre (str, optional): New genre
            quantity (int, optional): New quantity
            
        Returns:
            bool: True if updated successfully, False if book not found
        """
        if isbn not in self.books:
            return False
        try:
            self.books[isbn].update_info(title, author, genre, quantity)
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def remove_book(self, isbn):
        """
        Remove a book from the library.
        
        Args:
            isbn (str): ISBN of the book to remove
            
        Returns:
            bool: True if removed successfully, False if book not found or has borrowed copies
        """
        if isbn not in self.books:
            return False
        if self.books[isbn].borrowed_count > 0:
            return False  # Cannot remove book with borrowed copies
        del self.books[isbn]
        return True
    
    # Borrower Management Methods
    def add_borrower(self, name, membership_id, contact=None):
        """
        Add a new borrower to the system.
        
        Args:
            name (str): Name of the borrower
            membership_id (str): Unique membership ID
            contact (str, optional): Contact information
            
        Returns:
            bool: True if added successfully, False if membership ID already exists
        """
        if membership_id in self.borrowers:
            return False
        self.borrowers[membership_id] = Borrower(name, membership_id, contact)
        return True
    
    def update_borrower(self, membership_id, name=None, contact=None):
        """
        Update borrower information.
        
        Args:
            membership_id (str): Membership ID of the borrower
            name (str, optional): New name
            contact (str, optional): New contact information
            
        Returns:
            bool: True if updated successfully, False if borrower not found
        """
        if membership_id not in self.borrowers:
            return False
        self.borrowers[membership_id].update_info(name, contact)
        return True
    
    def remove_borrower(self, membership_id):
        """
        Remove a borrower from the system.
        
        Args:
            membership_id (str): Membership ID of the borrower to remove
            
        Returns:
            bool: True if removed successfully, False if borrower not found or has borrowed books
        """
        if membership_id not in self.borrowers:
            return False
        if len(self.borrowers[membership_id].borrowed_books) > 0:
            return False  # Cannot remove borrower with active borrowings
        del self.borrowers[membership_id]
        return True
    
    # Borrowing and Returning Methods
    def borrow_book(self, membership_id, isbn, days=14):
        """
        Process a book borrowing transaction.
        
        Args:
            membership_id (str): Membership ID of the borrower
            isbn (str): ISBN of the book to borrow
            days (int): Number of days until due date (default: 14)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if membership_id not in self.borrowers:
            return False, "Borrower not found."
        if isbn not in self.books:
            return False, "Book not found."
        if isbn in self.borrowers[membership_id].borrowed_books:
            return False, "Borrower has already borrowed this book."
        if not self.books[isbn].borrow():
            return False, "No copies available."
        
        # Record the borrowing
        due_date = datetime.now() + timedelta(days=days)
        self.borrowers[membership_id].borrow_book(isbn, self.books[isbn].title, days)
        self.borrowing_records[(membership_id, isbn)] = due_date
        
        return True, f"Book borrowed successfully. Due date: {due_date.strftime('%Y-%m-%d')}"
    
    def return_book(self, membership_id, isbn):
        """
        Process a book return transaction.
        
        Args:
            membership_id (str): Membership ID of the borrower
            isbn (str): ISBN of the book to return
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if membership_id not in self.borrowers:
            return False, "Borrower not found."
        if isbn not in self.books:
            return False, "Book not found."
        if not self.borrowers[membership_id].return_book(isbn):
            return False, "This book was not borrowed by this borrower."
        
        # Update book availability
        self.books[isbn].return_book()
        if (membership_id, isbn) in self.borrowing_records:
            del self.borrowing_records[(membership_id, isbn)]
        
        return True, "Book returned successfully."
    
    # Search Methods
    def search_books(self, query, search_by='title'):
        """
        Search for books by title, author, or genre.
        
        Args:
            query (str): Search query
            search_by (str): Search field - 'title', 'author', or 'genre' (default: 'title')
            
        Returns:
            list: List of Book objects matching the search criteria
        """
        query = query.lower()
        results = []
        
        for book in self.books.values():
            if search_by == 'title' and query in book.title.lower():
                results.append(book)
            elif search_by == 'author' and query in book.author.lower():
                results.append(book)
            elif search_by == 'genre' and query in book.genre.lower():
                results.append(book)
        
        return results
    
    def get_book_availability(self, isbn):
        """
        Get availability information for a specific book.
        
        Args:
            isbn (str): ISBN of the book
            
        Returns:
            dict: Availability information or None if book not found
        """
        if isbn not in self.books:
            return None
        book = self.books[isbn]
        return {
            'title': book.title,
            'author': book.author,
            'total_copies': book.quantity,
            'available_copies': book.available_copies,
            'borrowed_copies': book.borrowed_count
        }
    
    def get_all_books(self):
        """Get all books in the library."""
        return list(self.books.values())
    
    def get_all_borrowers(self):
        """Get all borrowers in the system."""
        return list(self.borrowers.values())
    
    def get_borrower_books(self, membership_id):
        """
        Get all books borrowed by a specific borrower.
        
        Args:
            membership_id (str): Membership ID of the borrower
            
        Returns:
            list: List of borrowed book information or None if borrower not found
        """
        if membership_id not in self.borrowers:
            return None
        borrower = self.borrowers[membership_id]
        return [
            {
                'isbn': isbn,
                'title': info['title'],
                'due_date': info['due_date']
            }
            for isbn, info in borrower.borrowed_books.items()
        ]