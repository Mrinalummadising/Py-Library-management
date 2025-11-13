class Borrower:
    """Represents a borrower in the library system."""
    
    def __init__(self, name, membership_id, contact=None):
        """
        Initialize a Borrower object.
        
        Args:
            name (str): Name of the borrower
            membership_id (str): Unique membership ID
            contact (str, optional): Contact information (email/phone)
        """
        self.name = name
        self.membership_id = membership_id
        self.contact = contact
        self.borrowed_books = {}  # Dictionary: {isbn: {'due_date': datetime, 'title': str}}
    
    def borrow_book(self, isbn, title, days=14):
        """
        Record a book borrowing.
        
        Args:
            isbn (str): ISBN of the book being borrowed
            title (str): Title of the book
            days (int): Number of days until due date (default: 14)
        """
        from datetime import datetime, timedelta
        due_date = datetime.now() + timedelta(days=days)
        self.borrowed_books[isbn] = {
            'due_date': due_date,
            'title': title
        }
    
    def return_book(self, isbn):
        """
        Record a book return.
        
        Args:
            isbn (str): ISBN of the book being returned
            
        Returns:
            bool: True if book was borrowed, False otherwise
        """
        if isbn in self.borrowed_books:
            del self.borrowed_books[isbn]
            return True
        return False
    
    def get_overdue_books(self):
        """
        Get list of overdue books.
        
        Returns:
            list: List of tuples (isbn, title, due_date) for overdue books
        """
        from datetime import datetime
        overdue = []
        current_date = datetime.now()
        for isbn, info in self.borrowed_books.items():
            if info['due_date'] < current_date:
                overdue.append((isbn, info['title'], info['due_date']))
        return overdue
    
    def update_info(self, name=None, contact=None):
        """
        Update borrower information.
        
        Args:
            name (str, optional): New name
            contact (str, optional): New contact information
        """
        if name is not None:
            self.name = name
        if contact is not None:
            self.contact = contact
    
    def __str__(self):
        """String representation of the borrower."""
        contact_info = f" - {self.contact}" if self.contact else ""
        return f"{self.name} (ID: {self.membership_id}){contact_info}"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Borrower(name='{self.name}', membership_id='{self.membership_id}', contact='{self.contact}')"