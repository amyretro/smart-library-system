from services.report_access import can_view_financial_reports
from database import user_repository
from database.connection import get_connection

def test_report_access():
    # Test 1: No user should be denied.
    result = can_view_financial_reports(None)
    assert result is False
    print("Test 1 passed: None user denied.")

    # Get users with different roles.
    connection = None
    cursor = None

    try:
     
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id FROM users WHERE role = %s LIMIT 1",
            ("Finance Manager",)
        )
        finance_row = cursor.fetchone()

        cursor.execute(
            "SELECT user_id FROM users WHERE role = %s LIMIT 1",
            ("Admin",)
        )
        admin_row = cursor.fetchone()

        cursor.execute(
            "SELECT user_id FROM users WHERE role = %s LIMIT 1",
            ("Customer",)
        )
        customer_row = cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    if finance_row is None:
        print("SKIP: No Finance Manager user found.")
    else:
        finance_user = user_repository.get_user_by_id(finance_row[0])
        assert can_view_financial_reports(finance_user) is True
        print("Test 2 passed: Finance Manager allowed.")

    if admin_row is None:
        print("SKIP: No Admin user found.")
    else:
        admin_user = user_repository.get_user_by_id(admin_row[0])
        assert can_view_financial_reports(admin_user) is False
        print("Test 3 passed: Admin denied.")

    if customer_row is None:
        print("SKIP: No Customer user found.")
    else:
        customer_user = user_repository.get_user_by_id(customer_row[0])
        assert can_view_financial_reports(customer_user) is False
        print("Test 4 passed: Customer denied.")

if __name__ == "__main__":
    test_report_access()
