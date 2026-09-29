from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

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

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing")
if not ALGORITHM:
    raise ValueError("ALGORITHM is missing")

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except InvalidTokenError:
        raise ValueError("Invalid or expired token")
