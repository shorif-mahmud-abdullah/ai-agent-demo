"""
AI Agent API routes
"""
from fastapi import APIRouter, Depends
from typing import Optional

from src.ai.gaming_ai_agent import GamingAIAgent
from src.schemas.ai_agent import ChatRequest, ChatResponse
from src.auth.dependencies import get_current_user_optional
from src.database.models import User

router = APIRouter(prefix="/api", tags=["ai-agent"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Chat with AI agent (authenticated)"""
    agent = GamingAIAgent()
    user_id = current_user.id if current_user else request.user_id
    
    response = agent.process_query(
        user_query=request.message,
        user_id=user_id,
        conversation_id=request.conversation_id
    )
    
    # Add user context to response
    if current_user:
        response["authenticated"] = True
        response["username"] = current_user.username
    else:
        response["authenticated"] = False
        if not request.user_id:
            response["message"] += "\n\n(For account-specific help, please login first)"
    
    return ChatResponse(**response)

@router.post("/chat/public", response_model=ChatResponse)
def chat_public(request: ChatRequest):
    """Public chat with AI agent (no authentication)"""
    agent = GamingAIAgent()
    response = agent.process_query(
        user_query=request.message,
        user_id=None,
        conversation_id=request.conversation_id
    )
    response["authenticated"] = False
    return ChatResponse(**response)