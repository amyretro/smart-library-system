from database.connection import get_connection

def add_sale(sale, connection=None):
    own_connection = connection is None

    if own_connection:
        connection = get_connection()

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO sales (
                book_id,
                user_id,
                quantity,
                unit_price,
                unit_cost,
                total_amount
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            sale["book_id"],
            sale["user_id"],
            sale["quantity"],
            sale["unit_price"],
            sale["unit_cost"],
            sale["quantity"] * sale["unit_price"]
        )

        cursor.execute(query, values)
        sale_id = cursor.lastrowid

        if own_connection:
            connection.commit()

        return sale_id

    except Exception:
        if own_connection:
            connection.rollback()
        raise

    finally:
        cursor.close()

        if own_connection:
            connection.close()