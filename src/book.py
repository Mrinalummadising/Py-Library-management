from datetime import datetime, timedelta


class Book:
    """Represents a book in the library system."""
    
    def __init__(self, title, author, isbn, genre, quantity=1):
        """
        Initialize a Book object.
        
        Args:
            title (str): Title of the book
            author (str): Author of the book
            isbn (str): ISBN number (unique identifier)
            genre (str): Genre of the book
            quantity (int): Number of copies available (default: 1)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.quantity = quantity
        self.borrowed_count = 0  # Number of copies currently borrowed
    
    @property
    def available_copies(self):
        """Calculate and return the number of available copies."""
        return self.quantity - self.borrowed_count
    
    def borrow(self):
        """Mark one copy as borrowed. Returns True if successful, False otherwise."""
        if self.available_copies > 0:
            self.borrowed_count += 1
            return True
        return False
    
    def return_book(self):
        """Mark one copy as returned. Returns True if successful, False otherwise."""
        if self.borrowed_count > 0:
            self.borrowed_count -= 1
            return True
        return False
    
    def update_info(self, title=None, author=None, genre=None, quantity=None):
        """
        Update book information.
        
        Args:
            title (str, optional): New title
            author (str, optional): New author
            genre (str, optional): New genre
            quantity (int, optional): New quantity (must be >= borrowed_count)
        """
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if genre is not None:
            self.genre = genre
        if quantity is not None:
            if quantity < self.borrowed_count:
                raise ValueError(f"Cannot set quantity to {quantity}. {self.borrowed_count} copies are currently borrowed.")
            self.quantity = quantity
    
    def __str__(self):
        """String representation of the book."""
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {self.available_copies}/{self.quantity} available"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}', genre='{self.genre}', quantity={self.quantity})"