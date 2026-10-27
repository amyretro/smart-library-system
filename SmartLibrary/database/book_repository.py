from database.connection import get_connection
from models.book import Book

def add_book(book):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO books (
                title,
                author,
                category,
                total_quantity,
                available_quantity,
                borrowed_quantity,
                borrow_price,
                purchase_price
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            book.title,
            book.author,
            book.category,
            book.total_quantity,
            book.available_quantity,
            book.borrowed_quantity,
            book.borrow_price,
            book.purchase_price
        )

        cursor.execute(query, values)
        book.book_id = cursor.lastrowid
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_all_books():
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                book_id,
                title,
                author,
                category,
                total_quantity,
                available_quantity,
                borrowed_quantity,
                borrow_price,
                purchase_price
            FROM books
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        books = [
            Book(
                row[0],  # book_id
                row[1],  # title
                row[2],  # author
                row[3],  # category
                row[4],  # total_quantity
                row[7],  # borrow_price
                row[8],  # purchase_price
                row[5],  # available_quantity
                row[6]   # borrowed_quantity
            )
            for row in rows
        ]

        return books

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def update_book(book, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            UPDATE books
            SET title = %s,
                author = %s,
                category = %s,
                total_quantity = %s,
                available_quantity = %s,
                borrowed_quantity = %s,
                borrow_price = %s,
                purchase_price = %s
            WHERE book_id = %s
        """

        values = (
            book.title,
            book.author,
            book.category,
            book.total_quantity,
            book.available_quantity,
            book.borrowed_quantity,
            book.borrow_price,
            book.purchase_price,
            book.book_id
        )

        cursor.execute(query, values)

        if own_connection:
            connection.commit()

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        cursor.close()

        if own_connection:
            connection.close()


def delete_book(book_id):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = "DELETE FROM books WHERE book_id = %s"
        cursor.execute(query, (book_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def get_book_for_update(book_id, connection):
    cursor = connection.cursor()

    try:
        query = """
            SELECT *
            FROM books
            WHERE book_id = %s
            FOR UPDATE
        """

        cursor.execute(query, (book_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return Book(
            row[0],  # book_id
            row[1],  # title
            row[2],  # author
            row[3],  # category
            row[4],  # total_quantity
            row[7],  # borrow_price
            row[8],  # purchase_price
            row[5],  # available_quantity
            row[6],  # borrowed_quantity
        )

    finally:
        cursor.close()