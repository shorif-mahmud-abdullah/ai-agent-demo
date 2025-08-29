"""
Pydantic schemas for AI agent operations
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    intent: str
    confidence: float
    needs_escalation: bool
    context_used: bool
    user_authenticated: bool
    authenticated: Optional[bool] = None
    username: Optional[str] = None
    error: Optional[str] = None