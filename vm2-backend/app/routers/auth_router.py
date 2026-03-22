from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserLogin, Token
from app.auth import create_access_token, authenticate_user
from app.config import settings
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    user = authenticate_user(user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user["user_id"], "company_id": user["company_id"], "username": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
