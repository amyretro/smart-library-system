from services.library import Library
from database.user_repository import get_user_by_username

# Create the library service.
library = Library()

# Use a unique username for this test.
username = "test_user_001"
password = "TestPassword123!"

# Check whether the test user already exists.
existing_user = get_user_by_username(username)

if existing_user is not None:
    print("Test user already exists. Choose another username.")
else:
    # Test user registration.
    result = library.add_user(
        "Test User",
        username,
        password,
        "0910000000",
        "test_user@example.com"
    )

    if isinstance(result, str):
        print("Registration failed:", result)
    else:
        print("Registration successful.")
        print("Database-generated user ID:", result.user_id)

        # Verify that the password is stored as a hash.
        if result.password_hash != password:
            print("Password hashing check passed.")
        else:
            print("Password hashing check failed.")

        # Test login with the correct password.
        logged_in_user = library.login_user(username, password)

        if logged_in_user is not None:
            print("Login with correct password passed.")
        else:
            print("Login with correct password failed.")

        # Test login with an incorrect password.
        failed_login = library.login_user(username, "WrongPassword123!")

        if failed_login is None:
            print("Login with incorrect password rejected successfully.")
        else:
            print("Login with incorrect password was incorrectly accepted.")
