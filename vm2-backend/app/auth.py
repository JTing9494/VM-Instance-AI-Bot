from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Mock users for development
MOCK_USERS = {
    "john_doe": {"username": "john_doe", "password": "password123", "company_id": 1, "user_id": 1},
    "jane_smith": {"username": "jane_smith", "password": "password123", "company_id": 2, "user_id": 2},
    "bob_johnson": {"username": "bob_johnson", "password": "password123", "company_id": 3, "user_id": 3},
    "alice_wilson": {"username": "alice_wilson", "password": "password123", "company_id": 4, "user_id": 4},
    "tom_hank": {"username": "tom_hank", "password": "password123", "company_id": 5, "user_id": 5},
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    if username in MOCK_USERS:
        user = MOCK_USERS[username]
        if user["password"] == password:
            return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        company_id: int = payload.get("company_id")
        username: str = payload.get("username")
        if user_id is None or company_id is None or username is None:
            raise credentials_exception
        # Return dict matching what frontend expects
        return {"user_id": user_id, "company_id": company_id, "username": username}
    except JWTError:
        raise credentials_exception
