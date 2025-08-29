"""
Authentication dependencies for FastAPI
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from src.database.connection import get_db
from src.database.models import User
from src.services.auth_service import AuthService

security = HTTPBearer()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get authentication service instance"""
    return AuthService(db)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        username = auth_service.verify_token(credentials.credentials)
        if username is None:
            raise credentials_exception
        
        user = auth_service.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        
        return user
        
    except Exception as e:
        print(f"Auth error: {e}")  # Debug logging
        raise credentials_exception

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    if not credentials:
        return None
    
    try:
        username = auth_service.verify_token(credentials.credentials)
        if username is None:
            return None
        
        user = auth_service.get_user_by_username(username)
        return user
        
    except Exception:
        return None