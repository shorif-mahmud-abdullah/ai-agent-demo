"""
Support-related API routes (FAQ and tickets)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from src.database.connection import get_db
from src.services.support_service import SupportService
from src.schemas.support import SupportTicketCreate, SupportTicketResponse, FAQResponse

router = APIRouter(prefix="/api", tags=["support"])

@router.get("/faqs", response_model=List[FAQResponse])
def get_faqs(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Get FAQs, optionally filtered by category"""
    support_service = SupportService(db)
    faqs = support_service.get_faqs(category)
    return faqs

@router.get("/faqs/search")
def search_faqs(q: str, db: Session = Depends(get_db)):
    """Search FAQs by question or answer content"""
    support_service = SupportService(db)
    faqs = support_service.search_faqs(q)
    return {"query": q, "results": faqs}

@router.post("/support-tickets")
def create_support_ticket(
    ticket_data: SupportTicketCreate,
    db: Session = Depends(get_db)
):
    """Create a new support ticket"""
    support_service = SupportService(db)
    ticket = support_service.create_support_ticket(ticket_data)
    
    return {
        "ticket_id": ticket.id,
        "message": f"Support ticket #{ticket.id} created successfully",
        "expected_response": "2-4 hours"
    }

@router.get("/support-tickets/{ticket_id}", response_model=SupportTicketResponse)
def get_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get support ticket by ID"""
    support_service = SupportService(db)
    ticket = support_service.get_support_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket