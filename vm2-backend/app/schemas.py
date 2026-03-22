from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Authentication schemas
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    company_id: Optional[int] = None

# Company schemas
class CompanyBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    name: str

# User schemas
class UserBase(BaseModel):
    id: int
    username: str
    company_id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    company_id: int

# Company data schemas
class CompanyDataBase(BaseModel):
    id: int
    company_id: int
    data_key: str
    data_value: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CompanyDataCreate(BaseModel):
    data_key: str
    data_value: str

class CompanyDataResponse(BaseModel):
    id: int
    data_key: str
    data_value: Optional[str] = None