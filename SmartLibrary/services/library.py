from models.book import Book
from models.borrow import Borrow
from datetime import datetime
from models.user import User
from services.auth import hash_password, verify_password
from database import (
    book_repository,
    user_repository,
    borrow_repository,
    purchase_repository,
    sale_repository
)
from database.connection import get_connection


class Library:
    def __init__(self):
        self.books = []
        self.borrows = []
        self.users = []
        self.next_borrow_id = 1
        self.next_user_id = 1
        self.load_books()
        self.load_borrows()

    def add_book(self, book, current_user):
        if current_user.role != "Admin":
            return "Permission denied"
        book_repository.add_book(book)
        self.books.append(book)
        return "Book added successfully"

    def search_by_title(self, title):
        for book in self.books:
            if book.title.lower().strip()== title.lower().strip():
                return book
        return None

    def search_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def delete_book(self, book_id, current_user):
        if current_user.role != "Admin":
            return "Permission denied"
        book = self.search_by_id(book_id)
        if book is None:
            return "Book not found"
        if book.borrowed_quantity > 0:
            return "Cannot delete a borrowed book"
        book_repository.delete_book(book_id)
        self.books.remove(book)
        return "Book deleted successfully"


    def update_book(self, book_id, current_user, title=None, author=None, category=None,
                    total_quantity=None, borrow_price=None, purchase_price=None):
        
        if current_user is None or current_user.role != "Admin":
            return "Permission denied"
        
        book = self.search_by_id(book_id)
        
        # Validation
        if book is None:
            return "Not found"
        
        if all(value is None for value in (
            title, author, category, total_quantity, borrow_price, purchase_price
            )):
            return "No fields to update"
        
        if total_quantity is not None:
            if total_quantity < 0 or total_quantity < book.borrowed_quantity:
                return "Invalid total quantity"
        
        if borrow_price is not None and borrow_price < 0:
            return "Invalid borrow price"
        
        if purchase_price is not None and purchase_price < 0:
            return "Invalid purchase price"
        
        # Prepare updated values without modifying the cached book.
        updated_book = Book(
            book.book_id,
            title if title is not None else book.title,
            author if author is not None else book.author,
            category if category is not None else book.category,
            total_quantity if total_quantity is not None else book.total_quantity,
            borrow_price if borrow_price is not None else book.borrow_price,
            purchase_price if purchase_price is not None else book.purchase_price,
            (
                total_quantity - book.borrowed_quantity
                 if total_quantity is not None
                 else book.available_quantity
            ),
            book.borrowed_quantity
        )
        
        try:
            # Save changes to the database before updating the cache.
            book_repository.update_book(updated_book)
            
            # Update the cached book only after the database update succeeds.
            book.title = updated_book.title
            book.author = updated_book.author
            book.category = updated_book.category
            book.total_quantity = updated_book.total_quantity
            book.available_quantity = updated_book.available_quantity
            book.borrow_price = updated_book.borrow_price
            book.purchase_price = updated_book.purchase_price
            
            return "Updated"
        
        except Exception:
            return "Database error"


    def purchase_books(self, book_id, quantity, unit_cost, current_user):
        if current_user.role != "Admin":
            return "Permission denied"

        if quantity <= 0:
            return "Invalid quantity"

        if unit_cost < 0:
            return "Invalid unit cost"

        connection = get_connection()

        try:
            book = book_repository.get_book_for_update(
                book_id, connection
            )

            if book is None:
                connection.rollback()
                return "Book not found"

            purchase = {
                "book_id": book_id,
                "quantity": quantity,
                "unit_cost": unit_cost,
                "admin_id": current_user.user_id
            }

            purchase_repository.add_purchase(purchase, connection)

            book.total_quantity += quantity
            book.available_quantity += quantity

            book_repository.update_book(book, connection)

            connection.commit()

            # Update the in-memory copy after a successful commit.
            cached_book = self.search_by_id(book_id)

            if cached_book is not None:
                cached_book.total_quantity = book.total_quantity
                cached_book.available_quantity = book.available_quantity
                cached_book.borrowed_quantity = book.borrowed_quantity

            return "Purchase recorded successfully"

        except Exception:
            connection.rollback()
            return "Database error"

        finally:
            connection.close()
    
    def sell_book(self, book_id, quantity, current_user):
        if current_user is None or current_user.role != "Customer":
            return "Permission denied"

        if quantity <= 0:
            return "Invalid quantity"

        connection = get_connection()

        try:
            book = book_repository.get_book_for_update(
                book_id, connection
            )

            if book is None:
                connection.rollback()
                return "Book not found"

            if quantity > book.available_quantity:
                connection.rollback()
                return "Insufficient quantity"

            unit_cost = purchase_repository.get_average_unit_cost(
            book_id, connection
            )

            if unit_cost is None:
                connection.rollback()
                return "Purchase cost unavailable"

            sale = {
                "book_id": book_id,
                "user_id": current_user.user_id,
                "quantity": quantity,
                "unit_price": book.purchase_price,
                "unit_cost": unit_cost
            }

            sale_repository.add_sale(sale, connection)

            book.total_quantity -= quantity
            book.available_quantity -= quantity

            book_repository.update_book(book, connection)

            connection.commit()

            cached_book = self.search_by_id(book_id)

            if cached_book is not None:
                cached_book.total_quantity = book.total_quantity
                cached_book.available_quantity = book.available_quantity
                cached_book.borrowed_quantity = book.borrowed_quantity

            return "Sale recorded successfully"

        except Exception as error:
            connection.rollback()
            print(f"Error while selling book: {error}")
            return "Database error"

        finally:
            connection.close()
    
    def borrow_book(self, book_id, requested_quantity, user_id):
        if requested_quantity <= 0:
            return "Invalid quantity"

        connection = get_connection()

        try:
            book = book_repository.get_book_for_update(
                book_id, connection
            )

            if book is None:
                connection.rollback()
                return "Not found"

            if book.available_quantity == 0:
                connection.rollback()
                return "Not available"

            if requested_quantity > book.available_quantity:
                connection.rollback()
                return "Insufficient quantity"

            borrow = Borrow(
                None,
                book_id,
                user_id,
                requested_quantity
            )

            borrow_repository.add_borrow(borrow, connection)

            book.available_quantity -= requested_quantity
            book.borrowed_quantity += requested_quantity

            book_repository.update_book(book, connection)

            connection.commit()

            # Update the in-memory book after a successful commit.
            cached_book = self.search_by_id(book_id)

            if cached_book is not None:
                cached_book.available_quantity = book.available_quantity
                cached_book.borrowed_quantity = book.borrowed_quantity
                cached_book.total_quantity = book.total_quantity

            # Reload borrows to get the database-generated borrow_id.
            self.load_borrows()

            return "borrowed"

        except Exception:
            connection.rollback()
            return "Database error"

        finally:
            connection.close()
    
    def return_book(self, borrow_id, returned_quantity):
        if returned_quantity <= 0:
            return "Invalid quantity"
        
        connection = get_connection()
        cursor = None
        borrow = None
        old_remaining = None
        old_return_date = None
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Lock the borrow record and retrieve its current database values.
            cursor.execute(
                """ SELECT
                borrow_id, book_id, user_id, quantity,
                remaining_quantity, borrow_date, due_date, return_date
            FROM borrows
            WHERE borrow_id = %s
            FOR UPDATE """,
                (borrow_id,)
            )
            borrow_row = cursor.fetchone()
            
            if borrow_row is None:
                connection.rollback()
                return "Borrow not found"
            
            remaining_quantity = borrow_row["remaining_quantity"]
            
            if returned_quantity > remaining_quantity:
                connection.rollback()
                return "Invalid return quantity"
            
            # Find the corresponding borrow record in memory.
            for item in self.borrows:
                if item.borrow_id == borrow_id:
                    borrow = item
                    break
            
            # Lock the book record within the same transaction.
            book = book_repository.get_book_for_update(
                borrow_row["book_id"],
                connection
            )
            
            if book is None:
                connection.rollback()
                return "Book not found"
            
            # Preserve the original in-memory values in case the transaction fails.
            if borrow is not None:
                old_remaining = borrow.remaining_quantity
                old_return_date = borrow.return_date
            
            # Update the locked book quantities.
            book.available_quantity += returned_quantity
            book.borrowed_quantity -= returned_quantity
            
            if book.borrowed_quantity < 0:
                connection.rollback()
                return "Database error"
            
            # Calculate the updated borrow values.
            new_remaining = remaining_quantity - returned_quantity
            new_return_date = (
                datetime.now() if new_remaining == 0 else borrow_row["return_date"]
            )
            
            # Update the borrow record in the database.
            cursor.execute(
                """ UPDATE borrows
                SET remaining_quantity = %s,
                    return_date = %s
                WHERE borrow_id = %s """,
                (new_remaining, new_return_date, borrow_id)
            )
            
            # Save both changes within the same transaction.
            book_repository.update_book(book, connection)
            connection.commit()
            
            # Update the in-memory borrow record after the commit succeeds.
            if borrow is not None:
                borrow.remaining_quantity = new_remaining
                borrow.return_date = new_return_date
            
            # Update the cached book after the commit succeeds.
            cached_book = self.search_by_id(book.book_id)
            
            if cached_book is not None:
                cached_book.available_quantity = book.available_quantity
                cached_book.borrowed_quantity = book.borrowed_quantity
                cached_book.total_quantity = book.total_quantity
            
            # Synchronize the in-memory borrow list with the database.
            self.load_borrows()
            
            return "returned"
        
        except Exception:
            connection.rollback()
            
            # Restore the original in-memory borrow values if the transaction fails.
            if borrow is not None:
                borrow.remaining_quantity = old_remaining
                borrow.return_date = old_return_date
            
            return "Database error"
        
        finally:
            if cursor is not None:
                cursor.close()
    
    
    def get_user_borrows(self, user_id):
        user_borrows = []

        for borrow in self.borrows:
            if borrow.user_id == user_id:
                user_borrows.append(borrow)

        return user_borrows

    def search_user_by_username(self, user_name):
        return user_repository.get_user_by_username(user_name)

    def search_user_by_id(self, user_id):
        return user_repository.get_user_by_id(user_id)

    def change_user_role(self, user_id, new_role, current_user):
        # Check whether the current user is an admin.
        if current_user is None or current_user.role != "Admin":
            return "Permission denied"
        
        # Validate the requested role.
        valid_roles = ["Admin", "Finance Manager", "Customer"]
        
        if new_role not in valid_roles:
            return "Invalid role"
        
        # Find the target user in the database.
        user = user_repository.get_user_by_id(user_id)
        
        if user is None:
            return "User not found"
        
        try:
            # Save the new role in the database first.
            updated = user_repository.update_user_role(user_id, new_role)
            
            if not updated:
                return "User not found"
            
            # Update the retrieved user object.
            user.role = new_role
            
            # Synchronize the cached user object, if present.
            for cached_user in self.users:
                if cached_user.user_id == user_id:
                    cached_user.role = new_role
            
            # Synchronize the current session if it belongs to the target user.
            if current_user.user_id == user_id:
                current_user.role = new_role
            
            return "Role updated successfully"
        
        except Exception:
            return "Database error"

    def add_user(self, name, user_name, password, phone_number, email):
        # Check whether the username already exists.
        existing_user = self.search_user_by_username(user_name)
        
        if existing_user is not None:
            return "Username already exists"
        
        # Hash the password before storing it.
        password_hash = hash_password(password)
        
        # Let the database assign the actual user ID.
        user = User( None, name, user_name, password_hash, phone_number, email )
        
        try:
            # Save the user to the database first.
            user_repository.add_user(user)
            
            # Update the in-memory list only after the database insert succeeds.
            self.users.append(user)
            
            # Keep the next user ID synchronized with the database-generated ID.
            self.next_user_id = max(self.next_user_id, user.user_id + 1)
            
            return user
        
        except Exception:
            return "Database error"

    def login_user(self, user_name, password):
        user = user_repository.get_user_by_username(user_name)
        if user is None:
            return None
        if verify_password(password, user.password_hash):
            return user
        return None

    def load_books(self):
        self.books = book_repository.get_all_books()

    def load_borrows(self):
        self.borrows = borrow_repository.get_all_borrows()
        