"""
Context management for AI agent
"""
import requests
import re
from typing import Dict, List, Optional
from src.config.settings import settings

class ContextManager:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or settings.BACKEND_URL
    
    def gather_context(self, user_query: str, user_id: Optional[int], intent: str) -> Dict:
        """Gather context from backend APIs and FAQ database"""
        context = {
            "user_data": None,
            "faq_results": [],
            "backend_data": {},
            "conversation_history": []
        }
        
        try:
            # 1. Get user data if user_id provided and intent requires it
            if user_id and intent in ['balance_check', 'withdrawal', 'kyc_status', 'transaction_history']:
                context["user_data"] = self._get_user_data(user_id)
            
            # 2. Search FAQ database
            context["faq_results"] = self._search_faqs(user_query)
            
            # 3. Get specific backend data based on intent
            if user_id:
                if intent == 'balance_check':
                    context["backend_data"]["balance"] = self._get_user_balance(user_id)
                elif intent == 'kyc_status':
                    context["backend_data"]["kyc"] = self._get_kyc_status(user_id)
                elif intent == 'transaction_history':
                    context["backend_data"]["transactions"] = self._get_user_transactions(user_id)
            
        except Exception as e:
            print(f"Error gathering context: {e}")
        
        return context
    
    def build_context_string(self, context: Dict) -> str:
        """Build context string from gathered information"""
        context_parts = []
        
        # User data
        if context["user_data"]:
            user = context["user_data"]
            context_parts.append(f"""
USER PROFILE:
- Username: {user.get('username')}
- Balance: ₹{user.get('balance', 0)}
- KYC Status: {user.get('kyc_status')}
- VIP Level: {user.get('vip_level')}
""")
        
        # Backend data
        if context["backend_data"]:
            if "balance" in context["backend_data"]:
                balance_data = context["backend_data"]["balance"]
                context_parts.append(f"CURRENT BALANCE: ₹{balance_data.get('balance', 0)}")
            
            if "kyc" in context["backend_data"]:
                kyc_data = context["backend_data"]["kyc"]
                context_parts.append(f"KYC STATUS: {kyc_data.get('kyc_status')} - {kyc_data.get('message', '')}")
            
            if "transactions" in context["backend_data"]:
                trans_data = context["backend_data"]["transactions"]
                if trans_data:
                    recent_trans = trans_data[:3]  # Last 3 transactions
                    trans_list = []
                    for t in recent_trans:
                        trans_list.append(f"₹{t.get('amount')} {t.get('transaction_type')} ({t.get('status')})")
                    context_parts.append(f"RECENT TRANSACTIONS:\n" + "\n".join(trans_list))
        
        # FAQ results
        if context["faq_results"]:
            faq_text = []
            for faq in context["faq_results"][:2]:  # Top 2 FAQs
                faq_text.append(f"Q: {faq.get('question')}\nA: {faq.get('answer')}")
            context_parts.append(f"RELEVANT FAQs:\n" + "\n---\n".join(faq_text))
        
        return "\n\n".join(context_parts)
    
    # Backend API calls
    def _get_user_data(self, user_id: int) -> Optional[Dict]:
        """Get user data from backend API"""
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching user data: {e}")
        return None
    
    def _get_user_balance(self, user_id: int) -> Optional[Dict]:
        """Get user balance from backend API"""
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/balance")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching balance: {e}")
        return None
    
    def _get_kyc_status(self, user_id: int) -> Optional[Dict]:
        """Get KYC status from backend API"""
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/kyc-status")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching KYC status: {e}")
        return None
    
    def _get_user_transactions(self, user_id: int) -> Optional[List[Dict]]:
        """Get user transactions from backend API"""
        try:
            response = requests.get(f"{self.backend_url}/api/users/{user_id}/transactions")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching transactions: {e}")
        return None
    
    def _search_faqs(self, query: str) -> List[Dict]:
        """Search FAQ database"""
        try:
            # Extract keywords for better search
            keywords = re.findall(r'\b\w+\b', query.lower())
            search_term = ' '.join(keywords[:3])  # Use first 3 keywords
            
            response = requests.get(f"{self.backend_url}/api/faqs/search?q={search_term}")
            if response.status_code == 200:
                return response.json().get("results", [])
        except Exception as e:
            print(f"Error searching FAQs: {e}")
        return []