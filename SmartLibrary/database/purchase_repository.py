from database.connection import get_connection

def add_purchase(purchase, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO purchases (
                book_id,
                quantity,
                unit_cost,
                total_cost,
                admin_id
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            purchase["book_id"],
            purchase["quantity"],
            purchase["unit_cost"],
            purchase["quantity"] * purchase["unit_cost"],
            purchase["admin_id"]
        )

        cursor.execute(query, values)
        purchase_id = cursor.lastrowid

        if own_connection:
            connection.commit()

        return purchase_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        cursor.close()

        if own_connection:
            connection.close()

def get_average_unit_cost(book_id, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            SELECT
                SUM(quantity * unit_cost) / NULLIF(SUM(quantity), 0)
            FROM purchases
            WHERE book_id = %s
        """

        cursor.execute(query, (book_id,))
        result = cursor.fetchone()[0]

        return result

    finally:
        cursor.close()

        if own_connection:
            connection.close()