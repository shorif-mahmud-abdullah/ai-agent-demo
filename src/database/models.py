"""
Database models for the gaming platform
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
from src.database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    hashed_password = Column(String)  # Added for authentication
    balance = Column(Float, default=0.0)
    kyc_status = Column(String, default="pending")  # pending, approved, rejected
    vip_level = Column(String, default="bronze")  # bronze, silver, gold, platinum
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    transaction_type = Column(String)  # deposit, withdrawal, bonus, bet
    amount = Column(Float)
    status = Column(String)  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    reference_id = Column(String)

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(String)  # account, payment, games, kyc
    language = Column(String, default="hinglish")
    created_at = Column(DateTime, default=datetime.utcnow)

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="open")  # open, in_progress, resolved
    priority = Column(String, default="medium")  # low, medium, high
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)