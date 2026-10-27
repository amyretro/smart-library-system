from datetime import datetime, timedelta

class Borrow:
    def __init__(self, borrow_id, book_id, user_id, requested_quantity):
        self.borrow_id = borrow_id
        self.book_id = book_id
        self.user_id = user_id
        self.quantity = requested_quantity # كمية النسخ الأصلية في عملية الاستعارة
        self.remaining_quantity = requested_quantity # كمية النسخ التي ما زالت مع المستخدم
        self.borrow_date = datetime.now()
        # الموعد المطلوب للإرجاع
        self.due_date = self.borrow_date + timedelta(days=14)
        # متى رجّع الشخص الكتاب فعليًا
        self.return_date = None

    def __str__(self):
            return (
                f"Borrow ID: {self.borrow_id}\n"
                f"Book ID: {self.book_id}\n"
                f"User ID: {self.user_id}\n"
                f"Quantity: {self.quantity}\n"
                f"Remaining Quantity: {self.remaining_quantity}\n"
                f"Borrow Date: {self.borrow_date}\n"
                f"Due Date: {self.due_date}\n"
                f"Return Date: {self.return_date}\n"
            )