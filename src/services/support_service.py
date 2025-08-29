"""
Support service layer for FAQ and ticket management
"""
from sqlalchemy.orm import Session
from src.database.models import FAQ, SupportTicket
from src.schemas.support import SupportTicketCreate
from typing import Optional, List

class SupportService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_faqs(self, category: Optional[str] = None) -> List[FAQ]:
        """Get FAQs, optionally filtered by category"""
        query = self.db.query(FAQ)
        if category:
            query = query.filter(FAQ.category == category)
        return query.all()
    
    def search_faqs(self, search_term: str) -> List[FAQ]:
        """Search FAQs by question or answer content"""
        return self.db.query(FAQ).filter(
            FAQ.question.ilike(f"%{search_term}%") | 
            FAQ.answer.ilike(f"%{search_term}%")
        ).all()
    
    def create_support_ticket(self, ticket_data: SupportTicketCreate) -> SupportTicket:
        """Create a new support ticket"""
        ticket = SupportTicket(**ticket_data.dict())
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
    
    def get_support_ticket(self, ticket_id: int) -> Optional[SupportTicket]:
        """Get support ticket by ID"""
        return self.db.query(SupportTicket).filter(
            SupportTicket.id == ticket_id
        ).first()
    
    def get_user_tickets(self, user_id: int) -> List[SupportTicket]:
        """Get all tickets for a user"""
        return self.db.query(SupportTicket).filter(
            SupportTicket.user_id == user_id
        ).order_by(SupportTicket.created_at.desc()).all()