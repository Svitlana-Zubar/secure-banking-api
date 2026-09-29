from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

password_hash = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        password_hash.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
    except VerificationError:
        return False
    except InvalidHashError:
        return False
