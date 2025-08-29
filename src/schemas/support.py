"""
Pydantic schemas for support-related operations
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SupportTicketCreate(BaseModel):
    user_id: int
    title: str
    description: str
    priority: str = "medium"

class SupportTicketResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    priority: str
    assigned_to: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    language: str
    
    class Config:
        from_attributes = True