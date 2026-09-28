from argon2 import PasswordHasher

password_hash = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hash.hash(password)