class User:
    def __init__(self, user_id, name, user_name, password_hash, phone_number, email):
        self.user_id = user_id
        self.name = name
        self.user_name = user_name
        self.password_hash = password_hash
        self.phone_number = phone_number
        self.email = email
        self.role = "Customer"

    def __str__(self):
        return (
            f"User ID: {self.user_id}\n"
            f"Name: {self.name}\n"
            f"Username: {self.user_name}\n"
            f"Phone Number: {self.phone_number}\n"
            f"Email: {self.email}\n"
            f"Role: {self.role}\n"
        )