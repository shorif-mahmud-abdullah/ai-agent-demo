"""
Response generation using Gemini AI
"""
import google.generativeai as genai
from typing import Dict, Optional
from src.config.settings import settings

class ResponseGenerator:
    def __init__(self):
        """Initialize the response generator with Gemini API"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL_NAME)
        
        self.system_prompt = """
                You are a helpful customer support AI agent for an Indian gaming/casino platform.

                PERSONALITY:
                - Be friendly, respectful, and professional
                - Use mix of English and Hindi (Hinglish) naturally
                - If user ask question in english give response in english if user ask query in hinglish response accordingly.
                - Address users as "Sir" or "Madam" respectfully
                - Be empathetic and understanding

                CAPABILITIES:
                - Answer questions about gaming platform
                - Help with account issues, withdrawals, deposits
                - Provide KYC guidance
                - Search FAQ database
                - Escalate to human agents when needed

                IMPORTANT RULES:
                1. Always check user authentication before sharing personal account info
                2. Use real-time data from backend APIs when available
                3. If you cannot help, offer to connect them with human support
                4. Be concise but helpful
                5. Never make promises about money or transactions you cannot fulfill

                RESPONSE FORMAT:
                - Keep responses under 150 words
                - Use bullet points for multiple items
                - End with asking if they need more help
                """
    
    def generate_response(self, user_query: str, context: Dict, intent: str, user_id: Optional[int]) -> Dict:
        """Generate AI response using Gemini with gathered context"""
        
        # Build context string for AI
        context_str = context.get("context_string", "")
        
        # Create prompt
        prompt = f"""
{self.system_prompt}

CONTEXT INFORMATION:
{context_str}

USER QUERY: "{user_query}"
DETECTED INTENT: {intent}
USER_ID: {user_id if user_id else "Not authenticated"}

Please provide a helpful response based on the context above. If you need user authentication for sensitive information, ask them to login first.
"""

        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            ai_message = response.text.strip()
            
            # Determine if escalation needed
            needs_escalation = self._should_escalate(user_query, ai_message, intent)
            
            # Calculate confidence (simple heuristic)
            confidence = self._calculate_confidence(context, intent, ai_message)
            
            return {
                "message": ai_message,
                "intent": intent,
                "confidence": confidence,
                "needs_escalation": needs_escalation,
                "context_used": bool(context_str),
                "user_authenticated": bool(user_id)
            }
            
        except Exception as e:
            return {
                "message": "Sorry, main abhi kuch technical problem face kar raha hun. Human agent se baat karna chahenge?",
                "intent": intent,
                "confidence": 0.1,
                "needs_escalation": True,
                "error": str(e)
            }
    
    def _should_escalate(self, user_query: str, ai_response: str, intent: str) -> bool:
        """Determine if query should be escalated to human"""
        
        escalation_triggers = [
            intent == 'human_request',
            'human' in user_query.lower() and 'agent' in user_query.lower(),
            'manager' in user_query.lower(),
            'complaint' in user_query.lower(),
            'frustrated' in user_query.lower(),
            'not helping' in user_query.lower(),
            len(user_query.split()) > 50,  # Very long queries
        ]
        
        return any(escalation_triggers)
    
    def _calculate_confidence(self, context: Dict, intent: str, ai_response: str) -> float:
        """Calculate confidence score for the response"""
        confidence = 0.5
        
        # Boost confidence if we have relevant context
        if context.get("user_data"):
            confidence += 0.2
        if context.get("backend_data"):
            confidence += 0.2
        if context.get("faq_results"):
            confidence += 0.1
        
        # Reduce confidence for certain intents
        if intent == 'general_query':
            confidence -= 0.1
        if 'sorry' in ai_response.lower():
            confidence -= 0.2
        
        return max(0.1, min(1.0, confidence))