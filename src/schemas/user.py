"""
Pydantic schemas for user-related operations
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    balance: float
    kyc_status: str
    vip_level: str
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    kyc_status: Optional[str] = None
    vip_level: Optional[str] = None