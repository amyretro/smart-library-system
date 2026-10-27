from services.library import Library
from services.report_service import (
get_sales_report,
get_purchases_report,
get_profit_report
)
from services.report_access import can_view_financial_reports

def display_financial_reports(current_user):
    if not can_view_financial_reports(current_user):
        print("Permission denied")
        return

    print("\n--- Sales Report ---")
    print(get_sales_report())

    print("\n--- Purchases Report ---")
    print(get_purchases_report())

    print("\n--- Profit Report ---")
    print(get_profit_report())

def main():
    library = Library()

    print("Welcome to SmartLibrary!")
    print(f"Loaded {len(library.books)} books.")

    current_user = None

    while current_user is None:
        username = input("Username: ")
        password = input("Password: ")

        current_user = library.login_user(username, password)

        if current_user is None:
            print("Invalid username or password. Please try again.")

    print(f"\nWelcome, {current_user.user_name}!")
    print(f"Role: {current_user.role}")

    if current_user.role == "Finance Manager":
        display_financial_reports(current_user)

    elif current_user.role == "Admin":
        print("You are logged in as Admin.")

    elif current_user.role == "Customer":
        print("You are logged in as Customer.")

if __name__ == "__main__":
    main()
