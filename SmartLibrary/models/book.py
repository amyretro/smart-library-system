class Book:
    def __init__(self, book_id, title, author, category, total_quantity, borrow_price, purchase_price,
                 available_quantity=None, borrowed_quantity=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.total_quantity = total_quantity
        
        if available_quantity is None:
            available_quantity = total_quantity
        if borrowed_quantity is None:
            borrowed_quantity = 0
        
        self.available_quantity = available_quantity
        self.borrowed_quantity = borrowed_quantity
        self.borrow_price = borrow_price
        self.purchase_price = purchase_price
    def __str__(self):
        return (
            f"Book ID: {self.book_id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Category: {self.category}\n"
            f"Total Quantity: {self.total_quantity}\n"
            f"Available Quantity: {self.available_quantity}\n"
            f"Borrowed Quantity: {self.borrowed_quantity}\n"
        )