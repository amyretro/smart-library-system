from database.connection import get_connection
from models.user import User

def add_user(user):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO users (
                name,
                username,
                password_hash,
                phone_number,
                email,
                role
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            user.name,
            user.user_name,
            user.password_hash,
            user.phone_number,
            user.email,
            user.role
        )

        cursor.execute(query, values)
        user.user_id = cursor.lastrowid
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def get_user_by_username(username):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row is None:
            return None

        user = User(
            row[0],  # user_id
            row[1],  # name
            row[2],  # username
            row[3],  # password_hash
            row[4],  # phone_number
            row[5],  # email
        )
        user.role = row[6]

        return user

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def update_user_role(user_id, new_role):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether the user exists.
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone() is None:
            connection.rollback()
            return False

        # Update the user's role.
        query = """
            UPDATE users
            SET role = %s
            WHERE user_id = %s
        """

        cursor.execute(query, (new_role, user_id))
        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def get_user_by_id(user_id):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        user = User(
            row[0],  # user_id
            row[1],  # name
            row[2],  # username
            row[3],  # password_hash
            row[4],  # phone_number
            row[5],  # email
        )

        user.role = row[6]
        return user

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
