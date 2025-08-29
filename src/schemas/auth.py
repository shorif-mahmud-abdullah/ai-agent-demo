"""
Pydantic schemas for authentication operations
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    message: str
    user_id: int
    welcome_bonus: str

class AuthenticatedUserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    balance: float
    kyc_status: str
    vip_level: str