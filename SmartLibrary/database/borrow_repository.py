from database.connection import get_connection
from models.borrow import Borrow

def add_borrow(borrow, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO borrows (
                user_id,
                book_id,
                quantity,
                remaining_quantity,
                due_date
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            borrow.user_id,
            borrow.book_id,
            borrow.quantity,
            borrow.remaining_quantity,
            borrow.due_date
        )

        cursor.execute(query, values)
        borrow.borrow_id = cursor.lastrowid

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


def update_borrow(borrow, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            UPDATE borrows
            SET remaining_quantity = %s,
                return_date = %s
            WHERE borrow_id = %s
        """

        values = (
            borrow.remaining_quantity,
            borrow.return_date,
            borrow.borrow_id
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

def get_all_borrows():
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT borrow_id, book_id, user_id, quantity,
                   remaining_quantity, borrow_date, due_date, return_date
            FROM borrows
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        borrows = []

        for row in rows:
            borrow = Borrow(
                row[0],  # borrow_id
                row[1],  # book_id
                row[2],  # user_id
                row[3]   # quantity
            )

            borrow.remaining_quantity = row[4]
            borrow.borrow_date = row[5]
            borrow.due_date = row[6]
            borrow.return_date = row[7]

            borrows.append(borrow)

        return borrows

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()