"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database.connection import get_db
from src.services.auth_service import AuthService
from src.auth.dependencies import get_current_user, get_auth_service
from src.schemas.auth import (
    UserCreate, UserLogin, Token, 
    UserRegistrationResponse, AuthenticatedUserResponse
)
from src.database.models import User
from src.config.settings import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserRegistrationResponse)
def register_user(
    user_data: UserCreate, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register new user"""
    # Check if username already exists
    if auth_service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if auth_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = auth_service.create_user(user_data)
    
    return UserRegistrationResponse(
        message=f"User {user_data.username} registered successfully!",
        user_id=db_user.id,
        welcome_bonus="₹1000 welcome bonus credited!"
    )

@router.post("/login", response_model=Token)
def login_user(
    user_credentials: UserLogin, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login user and return JWT token"""
    user = auth_service.authenticate_user(
        user_credentials.username, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username
    )

@router.get("/me", response_model=AuthenticatedUserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return AuthenticatedUserResponse(
        user_id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        balance=current_user.balance,
        kyc_status=current_user.kyc_status,
        vip_level=current_user.vip_level
    )