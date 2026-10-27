from database.connection import get_connection


def get_sales_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                COUNT(*) AS total_sales,
                COALESCE(SUM(quantity), 0) AS total_quantity_sold,
                COALESCE(SUM(total_amount), 0) AS total_revenue
            FROM sales
        """

        cursor.execute(query)
        row = cursor.fetchone()

        return {
            "total_sales": row[0],
            "total_quantity_sold": row[1],
            "total_revenue": row[2]
        }

    finally:
        cursor.close()
        connection.close()


def get_purchases_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                COUNT(*) AS total_purchases,
                COALESCE(SUM(quantity), 0) AS total_quantity_purchased,
                COALESCE(SUM(total_cost), 0) AS total_cost
            FROM purchases
        """

        cursor.execute(query)
        row = cursor.fetchone()

        return {
            "total_purchases": row[0],
            "total_quantity_purchased": row[1],
            "total_cost": row[2]
        }

    finally:
        cursor.close()
        connection.close()


def get_inventory_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                book_id,
                title,
                total_quantity,
                available_quantity,
                borrowed_quantity
            FROM books
            ORDER BY book_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        return [
            {
                "book_id": row[0],
                "title": row[1],
                "total_quantity": row[2],
                "available_quantity": row[3],
                "borrowed_quantity": row[4]
            }
            for row in rows
        ]

    finally:
        cursor.close()
        connection.close()


def get_profit_report():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                COALESCE(SUM(quantity * unit_price), 0) AS total_revenue,
                COALESCE(SUM(quantity * unit_cost), 0) AS cost_of_goods_sold,
                COALESCE(
                    SUM(quantity * unit_price) -
                    SUM(quantity * unit_cost),
                    0
                ) AS gross_profit
            FROM sales
        """

        cursor.execute(query)
        row = cursor.fetchone()

        return {
            "total_revenue": row[0],
            "cost_of_goods_sold": row[1],
            "gross_profit": row[2]
        }

    finally:
        cursor.close()
        connection.close()