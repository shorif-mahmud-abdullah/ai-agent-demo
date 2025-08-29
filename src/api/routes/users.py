"""
User-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.database.connection import get_db
from src.services.user_service import UserService
from src.schemas.user import UserResponse
from src.schemas.transaction import TransactionResponse, BalanceResponse
from src.auth.dependencies import get_current_user
from src.database.models import User

# Create main router
router = APIRouter(prefix="/api/users", tags=["users"])

# Create a separate sub-router for authenticated user endpoints
me_router = APIRouter(prefix="/me", tags=["authenticated-user"])

# ===== AUTHENTICATED USER ENDPOINTS (me/*) =====
@me_router.get("/balance")
def get_my_balance(current_user: User = Depends(get_current_user)):
    """Get authenticated user's balance"""
    return {
        "user_id": current_user.id,
        "balance": current_user.balance,
        "currency": "INR",
        "last_updated": datetime.utcnow(),
        "username": current_user.username
    }

@me_router.get("/transactions")
def get_my_transactions(
    current_user: User = Depends(get_current_user),
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Get authenticated user's transactions"""
    user_service = UserService(db)
    transactions = user_service.get_user_transactions(current_user.id, limit)
    
    return {
        "user_id": current_user.id,
        "transactions": transactions,
        "count": len(transactions)
    }

@me_router.get("/kyc-status")
def get_my_kyc_status(current_user: User = Depends(get_current_user)):
    """Get authenticated user's KYC status"""
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "kyc_status": current_user.kyc_status,
        "message": f"KYC status is {current_user.kyc_status}" + (
            " - You can withdraw money" if current_user.kyc_status == "approved"
            else " - Please complete KYC to withdraw"
        )
    }

@me_router.get("/profile", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get authenticated user's profile"""
    return current_user

# Include the me_router in the main router
router.include_router(me_router)

# ===== PUBLIC USER ENDPOINTS =====
@router.get("/by-username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get user by username"""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/balance")
def get_user_balance(user_id: int, db: Session = Depends(get_db)):
    """Get user balance by ID"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return BalanceResponse(
        user_id=user_id,
        balance=user.balance,
        currency="INR",
        last_updated=datetime.utcnow()
    )

@router.get("/{user_id}/transactions", response_model=List[TransactionResponse])
def get_user_transactions(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get user transaction history by ID"""
    user_service = UserService(db)
    transactions = user_service.get_user_transactions(user_id, limit)
    return transactions

@router.get("/{user_id}/kyc-status")
def get_kyc_status(user_id: int, db: Session = Depends(get_db)):
    """Get user KYC status by ID"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user_id,
        "kyc_status": user.kyc_status,
        "message": f"KYC status is {user.kyc_status}" + (
            " - You can withdraw money" if user.kyc_status == "approved" 
            else " - Please complete KYC to withdraw"
        )
    }