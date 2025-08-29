"""
Intent detection for AI agent
"""
from typing import Dict, List

class IntentDetector:
    def __init__(self):
        self.intent_patterns = {
            'balance_check': ['balance', 'amount', 'money', 'paisa', 'rupee', 'kitna', 'account'],
            'withdrawal': ['withdrawal', 'withdraw', 'nikalna', 'payout', 'cash out'],
            'deposit': ['deposit', 'add money', 'recharge', 'paisa dalna'],
            'kyc_status': ['kyc', 'verification', 'documents', 'verify', 'approved'],
            'transaction_history': ['history', 'transactions', 'previous', 'last'],
            'bonus': ['bonus', 'offer', 'promotion', 'free'],
            'technical_issue': ['not working', 'error', 'problem', 'issue', 'bug'],
            'human_request': ['human', 'agent', 'representative', 'person', 'manager']
        }
    
    def detect_intent(self, user_query: str) -> str:
        """Detect user intent from query"""
        query_lower = user_query.lower()
        
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return 'general_query'
    
    def get_intent_confidence(self, user_query: str, detected_intent: str) -> float:
        """Calculate confidence score for detected intent"""
        if detected_intent == 'general_query':
            return 0.5
        
        query_lower = user_query.lower()
        keywords = self.intent_patterns.get(detected_intent, [])
        
        matches = sum(1 for keyword in keywords if keyword in query_lower)
        confidence = min(0.9, 0.3 + (matches * 0.2))
        
        return confidence