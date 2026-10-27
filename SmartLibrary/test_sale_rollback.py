from unittest.mock import patch

from database.connection import get_connection
from database import sale_repository
from models.book import Book
from services.library import Library


def count_sales(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM sales WHERE book_id = %s",
            (book_id,)
        )
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        connection.close()


def test_sale_rollback():
    library = Library()

    customer = library.login_user("charlie123", "password3")

    if customer is None:
        print("TEST FAILED: Customer login failed")
        return

    book_id = 14

    sales_before = count_sales(book_id)

    # Create a separate book object for the test.
    fake_book = Book(
        book_id,
        "Test Book",
        "Test Author",
        "Test Category",
        1,
        2.00,
        10.00,
        1,
        0
    )

    inserted_sale_ids = []

    # Keep the real sale insertion, but record its generated ID.
    real_add_sale = sale_repository.add_sale

    def track_add_sale(sale, connection=None):
        sale_id = real_add_sale(sale, connection)
        inserted_sale_ids.append(sale_id)
        return sale_id

    with patch(
        "services.library.book_repository.get_book_for_update",
        return_value=fake_book
    ), patch(
        "services.library.sale_repository.add_sale",
        side_effect=track_add_sale
    ), patch(
        "services.library.book_repository.update_book",
        side_effect=Exception("Simulated inventory update failure")
    ):
        result = library.sell_book(book_id, 1, customer)

    sales_after = count_sales(book_id)

    print("Sale result:", result)
    print("Sale insert executed:", bool(inserted_sale_ids))
    print("Sales count before:", sales_before)
    print("Sales count after:", sales_after)

    if (
        result == "Database error"
        and inserted_sale_ids
        and sales_before == sales_after
    ):
        print("TEST PASSED: Sale was rolled back successfully")
    else:
        print("TEST FAILED: Check the transaction handling")


if __name__ == "__main__":
    test_sale_rollback()