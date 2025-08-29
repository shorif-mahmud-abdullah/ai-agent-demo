
import gradio as gr
import sys
import os
import json
import requests
import pandas as pd
from datetime import datetime
from typing import List, Tuple, Optional, Dict

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ai.gaming_ai_agent import GamingAIAgent
    from src.config.settings import settings
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure the modular structure is set up correctly")
    sys.exit(1)

class AuthenticatedGradioDemo:
    def __init__(self):
        self.agent = GamingAIAgent()
        self.conversation_history = {}
        self.backend_url = "http://localhost:8000"
        self.current_token = None
        self.current_user = None
        
        # Demo credentials for easy testing
        self.demo_credentials = {
            "rahul_gamer": "password123",
            "priya_player": "password123", 
            "amit_user": "password123"
        }
    
    def login_user(self, username: str, password: str) -> Tuple[str, str, bool, Dict]:
        """Login user and return status"""
        try:
            response = requests.post(f"{self.backend_url}/api/auth/login", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                token_data = response.json()
                self.current_token = token_data["access_token"]
                
                # Get user profile
                headers = {"Authorization": f"Bearer {self.current_token}"}
                profile_response = requests.get(f"{self.backend_url}/api/auth/me", headers=headers)
                
                if profile_response.status_code == 200:
                    self.current_user = profile_response.json()
                    
                    success_msg = f"✅ Welcome back, {self.current_user['username']}!"
                    user_info = self.format_user_info(self.current_user)
                    
                    return success_msg, user_info, True, self.current_user
                else:
                    return "❌ Failed to get user profile", "", False, {}
            else:
                error_data = response.json()
                return f"❌ Login failed: {error_data.get('detail', 'Unknown error')}", "", False, {}
                
        except requests.exceptions.RequestException:
            return "❌ Cannot connect to server. Please make sure the API is running.", "", False, {}
        except Exception as e:
            return f"❌ Login error: {str(e)}", "", False, {}
    
    def register_user(self, username: str, email: str, phone: str, password: str) -> str:
        """Register new user"""
        try:
            response = requests.post(f"{self.backend_url}/api/auth/register", json={
                "username": username,
                "email": email,
                "phone": phone,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                return f"✅ {data['message']}\n🎁 {data['welcome_bonus']}"
            else:
                error_data = response.json()
                return f"❌ Registration failed: {error_data.get('detail', 'Unknown error')}"
                
        except requests.exceptions.RequestException:
            return "❌ Cannot connect to server. Please make sure the API is running."
        except Exception as e:
            return f"❌ Registration error: {str(e)}"
    
    def logout_user(self) -> Tuple[str, str, bool]:
        """Logout current user"""
        self.current_token = None
        self.current_user = None
        return "👋 Logged out successfully!", "", False
    
    def format_user_info(self, user_data: Dict) -> str:
        """Format user information for display"""
        if not user_data:
            return "Please login to see your profile"
        
        return f"""
**👤 User Profile:**
- **Username**: {user_data.get('username', 'N/A')}
- **Email**: {user_data.get('email', 'N/A')}
- **💰 Balance**: ₹{user_data.get('balance', 0):,.2f}
- **📋 KYC Status**: {user_data.get('kyc_status', 'N/A')}
- **⭐ VIP Level**: {user_data.get('vip_level', 'N/A')}
"""
    
    def get_user_balance(self) -> str:
        """Get authenticated user's balance"""
        if not self.current_token:
            return "❌ Please login first"
        
        try:
            headers = {"Authorization": f"Bearer {self.current_token}"}
            response = requests.get(f"{self.backend_url}/api/users/me/balance", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return f"💰 Your current balance: ₹{data['balance']:,.2f}"
            else:
                return f"❌ Failed to get balance: {response.status_code}"
                
        except Exception as e:
            return f"❌ Error getting balance: {str(e)}"
    
    def get_user_transactions(self) -> str:
        """Get authenticated user's transactions"""
        if not self.current_token:
            return "❌ Please login first"
        
        try:
            headers = {"Authorization": f"Bearer {self.current_token}"}
            response = requests.get(f"{self.backend_url}/api/users/me/transactions", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('transactions', [])
                
                if not transactions:
                    return "📝 No transactions found"
                
                trans_text = f"📊 Recent Transactions ({data.get('count', 0)}):\n\n"
                for trans in transactions[:5]:  # Show last 5
                    trans_text += f"• ₹{trans.get('amount', 0)} - {trans.get('transaction_type', 'N/A')} ({trans.get('status', 'N/A')})\n"
                
                return trans_text
            else:
                return f"❌ Failed to get transactions: {response.status_code}"
                
        except Exception as e:
            return f"❌ Error getting transactions: {str(e)}"
    
    def chat_with_agent(self, message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """Process chat message with authentication"""
        if not message.strip():
            return history, ""
        
        try:
            # Prepare request data
            chat_data = {
                "message": message,
                "conversation_id": f"gradio_auth_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            # Add authentication if available
            headers = {}
            if self.current_token:
                headers["Authorization"] = f"Bearer {self.current_token}"
            
            # Send request to API
            response = requests.post(f"{self.backend_url}/api/chat", json=chat_data, headers=headers)
            
            if response.status_code == 200:
                ai_response_data = response.json()
                ai_message = ai_response_data['message']
                
                # Add metadata
                metadata_parts = []
                if ai_response_data.get('intent') != 'general_query':
                    metadata_parts.append(f"🎯 Intent: {ai_response_data['intent']}")
                if ai_response_data.get('confidence', 0) > 0.7:
                    metadata_parts.append(f"📊 Confidence: {ai_response_data['confidence']:.1%}")
                if ai_response_data.get('needs_escalation'):
                    metadata_parts.append("🚨 Escalation needed")
                if ai_response_data.get('authenticated'):
                    metadata_parts.append(f"👤 User: {ai_response_data.get('username', 'N/A')}")
                
                if metadata_parts:
                    ai_message += f"\n\n<small>{'  •  '.join(metadata_parts)}</small>"
                
                history.append((message, ai_message))
                return history, ""
            else:
                error_msg = f"❌ API Error: {response.status_code}"
                history.append((message, error_msg))
                return history, ""
                
        except requests.exceptions.RequestException:
            error_msg = "❌ Cannot connect to API server. Please make sure it's running."
            history.append((message, error_msg))
            return history, ""
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            history.append((message, error_msg))
            return history, ""
    
    def get_sample_queries(self, authenticated: bool = False) -> List[str]:
        """Get sample queries based on authentication status"""
        base_queries = [
            "Hello, how can you help me?",
            "Game mein problem hai",
            "Bonus kaise milega?",
            "Human agent se baat karni hai"
        ]
        
        auth_queries = [
            "Mera balance kitna hai?",
            "Withdrawal kaise karu?", 
            "KYC status check karo",
            "Last transaction kya tha?",
            "Account details dikhao"
        ]
        
        return auth_queries if authenticated else base_queries
    
    def create_interface(self):
        """Create enhanced Gradio interface with authentication"""
        
        css = """
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .auth-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .user-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #28a745;
        }
        .demo-creds {
            background: #fff3cd;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
        """
        
        with gr.Blocks(css=css, title="Gaming Platform AI Agent - Auth Demo") as demo:
            # State variables
            is_logged_in = gr.State(False)
            user_data = gr.State({})
            
            gr.Markdown("""
            ### 🎮 Gaming Platform AI Agent - Demo
            """
            )
                        
            # Experience our AI agent with **full authentication** and **real API integration**!
            
            # **New Features:**
            # - 🔐 **User Login/Registration**
            # - 👤 **Real user profiles** from database
            # - 💰 **Live balance** and transaction data
            # - 🔒 **Authenticated chat** with personalized responses
            # - 📊 **Account management** features
            # 
            
            with gr.Row():
                # Left Column - Authentication & User Info
                with gr.Column(scale=1):
                    with gr.Tab("🔐 Login"):
                        gr.Markdown("### 👤 User Login")
                        
                        # Demo credentials info
                        gr.Markdown("""
                        <div class="demo-creds">
                        <strong>🎯 Demo Credentials:</strong><br>
                        • <code>rahul_gamer</code> / <code>password123</code><br>
                        • <code>priya_player</code> / <code>password123</code><br>
                        • <code>amit_user</code> / <code>password123</code>
                        </div>
                        """)
                        
                        login_username = gr.Textbox(label="Username", placeholder="rahul_gamer")
                        login_password = gr.Textbox(label="Password", type="password", placeholder="password123")
                        login_btn = gr.Button("Login 🚀", variant="primary")
                        logout_btn = gr.Button("Logout 👋", visible=False)
                        
                        login_status = gr.Markdown("Please login to access authenticated features")
                    
                    with gr.Tab("📝 Register"):
                        gr.Markdown("### 📝 New User Registration")
                        
                        reg_username = gr.Textbox(label="Username", placeholder="newuser123")
                        reg_email = gr.Textbox(label="Email", placeholder="user@example.com")
                        reg_phone = gr.Textbox(label="Phone", placeholder="+919876543210")
                        reg_password = gr.Textbox(label="Password", type="password", placeholder="securepassword")
                        register_btn = gr.Button("Register 📝", variant="secondary")
                        
                        register_status = gr.Markdown("")
                    
                    # User Profile Section
                    user_profile = gr.Markdown("", elem_classes=["user-info"])
                    
                    # Account Actions (visible when logged in)
                    with gr.Group(visible=False) as account_actions:
                        gr.Markdown("### 💼 Account Actions")
                        balance_btn = gr.Button("Check Balance 💰")
                        transactions_btn = gr.Button("View Transactions 📊")
                        
                        account_info = gr.Markdown("")
                
                # Right Column - Chat Interface
                with gr.Column(scale=2):
                    gr.Markdown("### 💬 AI Agent Chat")
                    
                    chatbot = gr.Chatbot(
                        height=500,
                        placeholder="Login to start chatting with personalized responses...",
                        show_label=False
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            placeholder="Type your message... (Login for account-specific queries)",
                            show_label=False,
                            scale=4
                        )
                        send_btn = gr.Button("Send 📤", scale=1, variant="primary")
                    
                    with gr.Row():
                        clear_btn = gr.Button("Clear Chat 🗑️")
                        sample_btn = gr.Button("Try Sample Query 🎲")
                    
                    # Sample queries section
                    sample_queries_display = gr.Markdown("""
                    **💡 Sample Queries (Login for more):**
                    • Hello, how can you help me?
                    • Game mein problem hai
                    • Bonus kaise milega?
                    • Human agent se baat karni hai
                    """)
            
            # Event Handlers
            def handle_login(username, password):
                status, profile, logged_in, user_info = self.login_user(username, password)
                
                # Update sample queries based on login status
                queries = self.get_sample_queries(logged_in)
                sample_text = f"**💡 Sample Queries ({'Authenticated' if logged_in else 'Public'}):**\n"
                sample_text += "\n".join([f"• {q}" for q in queries])
                
                return (
                    status,  # login_status
                    profile,  # user_profile
                    logged_in,  # is_logged_in state
                    user_info,  # user_data state
                    gr.update(visible=logged_in),  # logout_btn
                    gr.update(visible=not logged_in),  # login_btn
                    gr.update(visible=logged_in),  # account_actions
                    sample_text,  # sample_queries_display
                    "Chat with personalized AI responses!" if logged_in else "Login for account-specific help"  # msg placeholder
                )
            
            def handle_logout():
                status, profile, logged_in = self.logout_user()
                queries = self.get_sample_queries(False)
                sample_text = "**💡 Sample Queries (Public):**\n" + "\n".join([f"• {q}" for q in queries])
                
                return (
                    status,  # login_status
                    profile,  # user_profile
                    logged_in,  # is_logged_in state
                    {},  # user_data state
                    gr.update(visible=False),  # logout_btn
                    gr.update(visible=True),  # login_btn
                    gr.update(visible=False),  # account_actions
                    sample_text,  # sample_queries_display
                    "Type your message... (Login for account-specific queries)"  # msg placeholder
                )
            
            def handle_register(username, email, phone, password):
                return self.register_user(username, email, phone, password)
            
            def send_sample_query(logged_in):
                import random
                queries = self.get_sample_queries(logged_in)
                return random.choice(queries)
            
            # Wire up events
            login_btn.click(
                fn=handle_login,
                inputs=[login_username, login_password],
                outputs=[login_status, user_profile, is_logged_in, user_data, 
                        logout_btn, login_btn, account_actions, sample_queries_display, msg]
            )
            
            logout_btn.click(
                fn=handle_logout,
                outputs=[login_status, user_profile, is_logged_in, user_data,
                        logout_btn, login_btn, account_actions, sample_queries_display, msg]
            )
            
            register_btn.click(
                fn=handle_register,
                inputs=[reg_username, reg_email, reg_phone, reg_password],
                outputs=[register_status]
            )
            
            # Chat functionality
            send_btn.click(
                fn=self.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )
            
            msg.submit(
                fn=self.chat_with_agent,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )
            
            clear_btn.click(
                fn=lambda: ([], ""),
                outputs=[chatbot, msg]
            )
            
            sample_btn.click(
                fn=send_sample_query,
                inputs=[is_logged_in],
                outputs=[msg]
            )
            
            # Account actions
            balance_btn.click(
                fn=self.get_user_balance,
                outputs=[account_info]
            )
            
            transactions_btn.click(
                fn=self.get_user_transactions,
                outputs=[account_info]
            )
            
            # Footer
            # gr.Markdown("""
            # ---
            # ### 🔧 Enhanced Features
            # - **🔐 Full Authentication**: Login/Register with JWT tokens
            # - **🌐 Live API Integration**: Real-time data from FastAPI backend
            # - **👤 Personalized Chat**: Context-aware responses based on user profile
            # - **💰 Account Management**: Check balance, view transactions
            # - **📊 Real-time Data**: Live user profiles and transaction history
            
            # ### 🚀 Getting Started
            # 1. **Start the API server**: `python main_new.py`
            # 2. **Login** with demo credentials above
            # 3. **Chat** with personalized AI responses
            # 4. **Explore** account features and authenticated queries
            # """)
        
        return demo

def main():
    """Main function to run enhanced Gradio demo"""
    print("🚀 Starting Gaming Platform AI Agent - Enhanced Auth Demo")
    print("=" * 60)
    
    try:
        demo_app = AuthenticatedGradioDemo()
        interface = demo_app.create_interface()
        
        print("✅ Enhanced Gradio interface created successfully!")
        print("🔐 Features: Login, Registration, Authenticated Chat")
        print("🌐 Starting web server...")
        print("\n📋 Demo Credentials:")
        print("   • rahul_gamer / password123")
        print("   • priya_player / password123")
        print("   • amit_user / password123")
        print("\n⚠️  Make sure the API server is running: python main_new.py")
        
        # Launch the interface
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True
        )
        
    except Exception as e:
        print(f"❌ Error starting enhanced Gradio demo: {e}")
        print("Please make sure:")
        print("1. All dependencies are installed: pip install -r requirements.txt")
        print("2. API server is running: python main_new.py")

if __name__ == "__main__":
    main()