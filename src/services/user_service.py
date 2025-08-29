"""
User service layer for business logic
"""
from sqlalchemy.orm import Session
from src.database.models import User, Transaction
from src.schemas.user import UserCreate, UserUpdate
from typing import Optional, List

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        user = User(**user_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_balance(self, user_id: int) -> Optional[float]:
        """Get user balance"""
        user = self.get_user_by_id(user_id)
        return user.balance if user else None
    
    def get_user_transactions(self, user_id: int, limit: int = 10) -> List[Transaction]:
        """Get user transaction history"""
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).limit(limit).all()