def can_view_financial_reports(current_user):
    if current_user is None:
        return False

    return current_user.role == "Finance Manager"