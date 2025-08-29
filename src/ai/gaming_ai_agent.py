"""
Main AI Agent class that orchestrates all AI components
"""
from typing import Dict, Optional
from datetime import datetime
from src.ai.intent_detector import IntentDetector
from src.ai.context_manager import ContextManager
from src.ai.response_generator import ResponseGenerator
from src.config.settings import settings

class GamingAIAgent:
    def __init__(self, backend_url: str = None):
        """Initialize the AI Agent with all components"""
        
        # Initialize components
        self.intent_detector = IntentDetector()
        self.context_manager = ContextManager(backend_url or settings.BACKEND_URL)
        self.response_generator = ResponseGenerator()
        
        # Conversation history storage (in production, use database)
        self.conversations = {}
    
    def process_query(self, user_query: str, user_id: Optional[int] = None, 
                     conversation_id: Optional[str] = None) -> Dict:
        """Main function to process user query and return response"""
        
        try:
            # Store conversation
            if conversation_id:
                if conversation_id not in self.conversations:
                    self.conversations[conversation_id] = []
                self.conversations[conversation_id].append({
                    "timestamp": datetime.now(),
                    "user": user_query,
                    "user_id": user_id
                })
            
            # Detect intent
            intent = self.intent_detector.detect_intent(user_query)
            
            # Get context from multiple sources
            context = self.context_manager.gather_context(user_query, user_id, intent)
            
            # Build context string
            context["context_string"] = self.context_manager.build_context_string(context)
            
            # Generate AI response
            response = self.response_generator.generate_response(user_query, context, intent, user_id)
            
            # Store AI response in conversation
            if conversation_id:
                self.conversations[conversation_id].append({
                    "timestamp": datetime.now(),
                    "ai": response["message"],
                    "intent": intent,
                    "confidence": response.get("confidence", 0.8)
                })
            
            return response
            
        except Exception as e:
            return {
                "message": "Sorry, main technical issue face kar raha hun. Kya aap thoda wait kar sakte hai ya human agent se baat karna chahenge?",
                "error": str(e),
                "needs_escalation": True,
                "intent": "error",
                "confidence": 0.1,
                "context_used": False,
                "user_authenticated": bool(user_id)
            }
    
    def get_conversation_history(self, conversation_id: str) -> Optional[list]:
        """Get conversation history for a given conversation ID"""
        return self.conversations.get(conversation_id)
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation history for a given conversation ID"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False