from services.library import Library
from database.connection import get_connection
from database import user_repository, book_repository
from models.book import Book

library = Library()

# Find an Admin user directly from the database.
connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    "SELECT user_id FROM users WHERE role = %s LIMIT 1",
    ("Admin",)
)

admin_row = cursor.fetchone()

cursor.close()
connection.close()

if admin_row is None:
    print("Test stopped: No Admin user found.")
    raise SystemExit

admin = user_repository.get_user_by_id(admin_row[0])

# Create a temporary book for testing.
test_book = Book(
    None,
    "Borrow Return Test Book",
    "Test Author",
    "Testing",
    2,    # Total quantity
    1.0,  # Borrow price
    5.0,  # Purchase price
    2,    # Available quantity
    0     # Borrowed quantity
)

try:
    # Add the temporary book to the database.
    book_repository.add_book(test_book)
    library.books.append(test_book)

    print("Temporary book added:", test_book.book_id)

    # Borrow one copy.
    borrow_result = library.borrow_book(
        test_book.book_id,
        1,
        admin.user_id
    )

    print("Borrow result:", borrow_result)

    if borrow_result != "borrowed":
        raise RuntimeError("Borrow test failed.")

    updated_book = library.search_by_id(test_book.book_id)

    print(
        "After borrowing:",
        "Available =", updated_book.available_quantity,
        "| Borrowed =", updated_book.borrowed_quantity
    )

    # Find the newly created borrow record.
    library.load_borrows()

    test_borrow = next(
        (
            borrow
            for borrow in library.borrows
            if borrow.book_id == test_book.book_id
            and borrow.user_id == admin.user_id
        ),
        None
    )

    if test_borrow is None:
        raise RuntimeError("Borrow record not found.")

    # Return the borrowed copy.
    return_result = library.return_book(
        test_borrow.borrow_id,
        1
    )

    print("Return result:", return_result)

    updated_book = library.search_by_id(test_book.book_id)

    print(
        "After returning:",
        "Available =", updated_book.available_quantity,
        "| Borrowed =", updated_book.borrowed_quantity
    )

    # Verify the final quantities.
    if (
        return_result == "returned"
        and updated_book.available_quantity == 2
        and updated_book.borrowed_quantity == 0
    ):
        print("PASS: Borrow and return test succeeded.")
    else:
        print("FAIL: Borrow and return test failed.")

finally:
    # Remove test borrow records before deleting the temporary book.
    connection = get_connection()
    cursor = connection.cursor()
try:
    cursor.execute(
        "DELETE FROM borrows WHERE book_id = %s",
        (test_book.book_id,)
    )
    connection.commit()
except Exception:
    connection.rollback()
    raise
finally:
    cursor.close()
    connection.close()

# Delete the temporary book.
book_repository.delete_book(test_book.book_id)

library.books = [
    book
    for book in library.books
    if book.book_id != test_book.book_id
]

print("Temporary book and test borrow records deleted.")