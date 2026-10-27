from database.connection import get_connection
from mysql.connector import Error

connection = None

try:
    connection = get_connection()

    if connection.is_connected():
        print("Connected successfully!")

except Error as error:
    print(f"Database connection failed: {error}")

finally:
    if connection is not None and connection.is_connected():
        connection.close()