from services.library import Library
from database import user_repository


library = Library()

# Find an existing Admin user.
connection = user_repository.get_user_by_username

admin = None

connection_db = None

from database.connection import get_connection

connection_db = get_connection()
cursor = connection_db.cursor()

try:
    cursor.execute(
        "SELECT user_id FROM users WHERE role = %s LIMIT 1",
        ("Admin",)
    )
    admin_row = cursor.fetchone()
finally:
    cursor.close()
    connection_db.close()

if admin_row is None:
    print("STOP: No Admin user found.")
    raise SystemExit

admin = user_repository.get_user_by_id(admin_row[0])

# Find an existing user to test.
test_user = None

connection_db = get_connection()
cursor = connection_db.cursor()

try:
    cursor.execute(
        "SELECT user_id FROM users WHERE user_id != %s LIMIT 1",
        (admin.user_id,)
    )
    user_row = cursor.fetchone()
finally:
    cursor.close()
    connection_db.close()

if user_row is None:
    print("STOP: No second user found to test.")
    raise SystemExit

test_user = user_repository.get_user_by_id(user_row[0])

print("\n--- User Role Tests ---")

# Test 1: Admin assigns a valid role.
original_role = test_user.role

new_role = (
    "Finance Manager"
    if original_role != "Finance Manager"
    else "Customer"
)

result = library.change_user_role(
    test_user.user_id,
    new_role,
    admin
)

print("Test 1 - Admin changes role:", result)

# Test 2: Assign the same role again.
result_same = library.change_user_role(
    test_user.user_id,
    new_role,
    admin
)

print("Test 2 - Same role:", result_same)

# Test 3: Nonexistent user.
result_missing = library.change_user_role(
    -999999,
    "Customer",
    admin
)

print("Test 3 - Missing user:", result_missing)

# Test 4: Non-admin attempts to change a role.
result_permission = library.change_user_role(
    admin.user_id,
    "Customer",
    test_user
)

print("Test 4 - Permission check:", result_permission)

# Test 5: Invalid role.
result_invalid = library.change_user_role(
    test_user.user_id,
    "InvalidRole",
    admin
)

print("Test 5 - Invalid role:", result_invalid)

# Restore the original role.
restore_result = library.change_user_role(
    test_user.user_id,
    original_role,
    admin
)

print("Restore original role:", restore_result)