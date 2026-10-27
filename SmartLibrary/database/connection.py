import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="amna_20204084",
        database="smart_library"
    )
