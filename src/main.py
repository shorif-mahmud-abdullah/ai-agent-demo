"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.security import HTTPBearer

from src.config.settings import settings
from src.database.connection import create_tables
from src.utils.data_seeder import insert_dummy_data
from src.api.routes import users, support, ai_agent, auth

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Gaming Platform Prototype with AI Agent Support"
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(support.router)
app.include_router(ai_agent.router)

@app.on_event("startup")
def startup_event():
    """Initialize database and seed data on startup"""
    create_tables()
    insert_dummy_data()

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Gaming Platform Prototype API", 
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gaming-platform-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )