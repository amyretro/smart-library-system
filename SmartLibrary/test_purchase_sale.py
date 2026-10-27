from services.library import Library
from database.connection import get_connection
from database import user_repository, book_repository
from models.book import Book

library = Library()
test_book_id = None

try:
    # Find an Admin user and a Customer.
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id FROM users WHERE role = %s LIMIT 1",
            ("Admin",)
        )
        admin_row = cursor.fetchone()

        cursor.execute(
            "SELECT user_id FROM users WHERE role = %s LIMIT 1",
            ("Customer",)
        )
        customer_row = cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    if admin_row is None:
        raise RuntimeError("Test stopped: No Admin user found.")

    if customer_row is None:
        raise RuntimeError("Test stopped: No Customer user found.")

    admin = user_repository.get_user_by_id(admin_row[0])
    customer = user_repository.get_user_by_id(customer_row[0])

    # Create a temporary book.
    test_book = Book(
        None,
        "Purchase Sale Test Book",
        "Test Author",
        "Testing",
        0,
        1.0,
        10.0,
        0,
        0
        )

    book_repository.add_book(test_book)
    test_book_id = test_book.book_id
    library.books.append(test_book)

    print("Temporary book added:", test_book_id)

    # Test 1: Admin purchases 5 copies.
    result = library.purchase_books(
        test_book_id,
        5,
        4.0,
        admin
        )

    print("Purchase result:", result)

    if result != "Purchase recorded successfully":
        raise RuntimeError("Purchase test failed.")

    updated_book = library.search_by_id(test_book_id)

    if (
        updated_book.total_quantity != 5
        or updated_book.available_quantity != 5
        ):
        raise RuntimeError("Stock quantities after purchase are incorrect.")

    # Test 2: Customer buys 2 copies.
    result = library.sell_book(
        test_book_id,
        2,
        customer
        )

    print("Sale result:", result)

    if result != "Sale recorded successfully":
        raise RuntimeError("Sale test failed.")

    updated_book = library.search_by_id(test_book_id)

    if (
        updated_book.total_quantity != 3
        or updated_book.available_quantity != 3
        ):
        raise RuntimeError("Stock quantities after sale are incorrect.")

    # Verify purchase and sale records.
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        cursor.execute(
    """
    SELECT quantity, unit_cost, total_cost
    FROM purchases
    WHERE book_id = %s
    ORDER BY purchase_id DESC
    LIMIT 1
    """,
    (test_book_id,)
)
        purchase_row = cursor.fetchone()

        cursor.execute(
    """
    SELECT quantity, unit_price, unit_cost, total_amount
    FROM sales
    WHERE book_id = %s
    ORDER BY sale_id DESC
    LIMIT 1
    """,
    (test_book_id,)
)
        sale_row = cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        
        connection.close()

    if purchase_row is None:
        raise RuntimeError("Purchase record not found.")

    if sale_row is None:
        raise RuntimeError("Sale record not found.")

    purchase_quantity, purchase_cost, purchase_total = purchase_row
    sale_quantity, sale_price, sale_cost, sale_total = sale_row

    print(
    "Purchase record:",
    "Quantity =", purchase_quantity,
    "| Unit cost =", purchase_cost,
    "| Total cost =", purchase_total
    )

    print(
    "Sale record:",
    "Quantity =", sale_quantity,
    "| Unit price =", sale_price,
    "| Unit cost =", sale_cost,
    "| Total amount =", sale_total
    )

    if (
        purchase_quantity != 5
        or float(purchase_total) != 20.0
        ):
        raise RuntimeError("Purchase record values are incorrect.")

    if (
        sale_quantity != 2
        or float(sale_total) != 20.0
        ):
        raise RuntimeError("Sale record values are incorrect.")

    # Test 3: Selling more copies than available must fail.
    result = library.sell_book(
        test_book_id,
        100,
        customer
        )

    print("Insufficient stock test:", result)

    if result != "Insufficient quantity":
        raise RuntimeError("Insufficient stock test failed.")

    # Test 4: Customer cannot purchase stock.
    result = library.purchase_books(
        test_book_id,
        1,
        4.0,
        customer
        )

    print("Purchase permission test:", result)

    if result != "Permission denied":
        raise RuntimeError("Purchase permission test failed.")

    # Test 5: Admin cannot sell through sell_book.
    result = library.sell_book(
        test_book_id,
        1,
        admin
        )

    print("Sale permission test:", result)

    if result != "Permission denied":
        raise RuntimeError("Sale permission test failed.")

    print("PASS: Purchase and sale tests succeeded.")

finally:
    # Clean up test records.
    if test_book_id is not None:
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM sales WHERE book_id = %s",
                (test_book_id,)
                )

            cursor.execute(
                "DELETE FROM purchases WHERE book_id = %s",
                (test_book_id,)
                )

            connection.commit()

        except Exception:
            if connection is not None:
                connection.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

        book_repository.delete_book(test_book_id)

        library.books = [
            book
            for book in library.books
            if book.book_id != test_book_id
            ]

    print("Temporary book and test records deleted.")