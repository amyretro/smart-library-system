from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher = PasswordHasher()
def hash_password(password):
    return password_hasher.hash(password)

def verify_password(password, hashed_password):
    try:
        return password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False