"""
Configuration settings for the gaming platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/gaming_prototype",
    )
    
    # API configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_TITLE = "Gaming Platform Prototype"
    API_VERSION = "1.0.0"
    
    # AI Agent configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")
    BACKEND_URL = "http://localhost:8000"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
