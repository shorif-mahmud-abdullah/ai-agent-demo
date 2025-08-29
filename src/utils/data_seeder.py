"""
Database seeding utilities
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.database.connection import SessionLocal
from src.database.models import User, Transaction, FAQ, SupportTicket

def insert_dummy_data():
    """Insert dummy data for development and testing"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Dummy data already exists, skipping insertion.")
            return
        
        # Password hashing context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Dummy users with hashed passwords
        users_data = [
            {"username": "rahul_gamer", "email": "rahul@example.com", "phone": "+919876543210", 
             "balance": 5000.0, "kyc_status": "approved", "vip_level": "gold", "password": "password123"},
            {"username": "priya_player", "email": "priya@example.com", "phone": "+919876543211", 
             "balance": 2500.0, "kyc_status": "pending", "vip_level": "silver", "password": "password123"},
            {"username": "amit_user", "email": "amit@example.com", "phone": "+919876543212", 
             "balance": 15000.0, "kyc_status": "approved", "vip_level": "platinum", "password": "password123"},
        ]
        
        for user_data in users_data:
            # Hash the password
            password = user_data.pop("password")
            hashed_password = pwd_context.hash(password)
            user_data["hashed_password"] = hashed_password
            
            user = User(**user_data)
            db.add(user)
        
        # Dummy transactions
        transactions_data = [
            {"user_id": 1, "transaction_type": "deposit", "amount": 1000.0, "status": "completed", "reference_id": "DEP001"},
            {"user_id": 1, "transaction_type": "withdrawal", "amount": 500.0, "status": "pending", "reference_id": "WIT001"},
            {"user_id": 2, "transaction_type": "deposit", "amount": 2000.0, "status": "completed", "reference_id": "DEP002"},
            {"user_id": 2, "transaction_type": "bonus", "amount": 500.0, "status": "completed", "reference_id": "BON001"},
            {"user_id": 3, "transaction_type": "withdrawal", "amount": 5000.0, "status": "completed", "reference_id": "WIT002"},
        ]
        
        for trans_data in transactions_data:
            transaction = Transaction(**trans_data)
            db.add(transaction)
        
        # Dummy FAQs
        faqs_data = [
            {
                "question": "Mera withdrawal kitni der mein process hoga?",
                "answer": "Sir, withdrawal usually 24-48 hours mein process hota hai. Agar aapka KYC complete hai toh jaldi ho jayega.",
                "category": "payment",
                "language": "hinglish"
            },
            {
                "question": "KYC verification kaise karu?",
                "answer": "KYC ke liye aap Aadhar card, PAN card, aur bank statement upload kar sakte hai. Profile section mein KYC option milega.",
                "category": "kyc",
                "language": "hinglish"
            },
            {
                "question": "Bonus kaise milega?",
                "answer": "First deposit par 100% bonus milta hai. Minimum deposit ₹500 hona chahiye. Wagering requirement 5x hai.",
                "category": "account",
                "language": "hinglish"
            },
            {
                "question": "Game mein technical problem hai",
                "answer": "Game refresh karke try karo. Agar phir bhi problem hai toh support team ko contact karo.",
                "category": "games",
                "language": "hinglish"
            },
            {
                "question": "Account balance check kaise karu?",
                "answer": "Dashboard mein wallet section mein aapka current balance dikhega. Real-time update hota hai.",
                "category": "account",
                "language": "hinglish"
            }
        ]
        
        for faq_data in faqs_data:
            faq = FAQ(**faq_data)
            db.add(faq)
        
        db.commit()
        print("Dummy data inserted successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error inserting dummy data: {e}")
    finally:
        db.close()