"""
Pydantic schemas for transaction-related operations
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionResponse(BaseModel):
    id: int
    transaction_type: str
    amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    reference_id: Optional[str] = None

class BalanceResponse(BaseModel):
    user_id: int
    balance: float
    currency: str = "INR"
    last_updated: datetime