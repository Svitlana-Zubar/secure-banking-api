from fastapi import Depends, HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import decode_access_token

security = HTTPBearer()

def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    return credentials.credentials

def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Missing user ID")
        return int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )