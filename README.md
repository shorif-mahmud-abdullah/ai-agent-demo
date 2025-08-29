# Gaming Platform with AI Agent

A modular gaming platform API with integrated AI customer support agent built with FastAPI and Google Gemini AI.

## Project Structure

```
ai_agent_demo/
├── src/                          # Main source code directory
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py           # Application settings
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py         # Database connection & session
│   │   └── models.py             # SQLAlchemy models
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py               # User-related schemas
│   │   ├── transaction.py        # Transaction schemas
│   │   ├── support.py            # Support & FAQ schemas
│   │   └── ai_agent.py           # AI agent schemas
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py       # User business logic
│   │   └── support_service.py    # Support business logic
│   ├── ai/                       # AI Agent components
│   │   ├── __init__.py
│   │   ├── gaming_ai_agent.py    # Main AI agent orchestrator
│   │   ├── intent_detector.py    # Intent detection logic
│   │   ├── context_manager.py    # Context gathering & management
│   │   └── response_generator.py # AI response generation
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── routes/               # API route handlers
│   │       ├── __init__.py
│   │       ├── users.py          # User API endpoints
│   │       ├── support.py        # Support API endpoints
│   │       └── ai_agent.py       # AI agent API endpoints
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── data_seeder.py        # Database seeding utilities
├── main_new.py                   # New modular main entry point
├── ai_agent_new.py               # New modular AI agent entry point
├── main.py                       # Original monolithic file (kept for reference)
├── ai_agent.py                   # Original monolithic file (kept for reference)
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## Architecture Benefits

### 1. **Separation of Concerns**
- **Database Layer**: Models and connection management
- **Service Layer**: Business logic and data operations
- **API Layer**: HTTP request/response handling
- **AI Layer**: AI-specific components and logic
- **Configuration**: Centralized settings management

### 2. **Modularity**
- Each component has a single responsibility
- Easy to test individual components
- Components can be developed independently
- Clear dependencies between layers

### 3. **Scalability**
- Easy to add new features without affecting existing code
- Components can be scaled independently
- Database operations are abstracted through services
- AI components are loosely coupled

### 4. **Maintainability**
- Code is organized logically
- Easy to locate and modify specific functionality
- Clear import structure
- Consistent naming conventions

## Key Components

### AI Agent Architecture
The AI agent is now split into specialized components:

1. **IntentDetector**: Analyzes user queries to determine intent
2. **ContextManager**: Gathers relevant context from APIs and databases
3. **ResponseGenerator**: Uses Gemini AI to generate contextual responses
4. **GamingAIAgent**: Orchestrates all AI components

### Service Layer
Business logic is separated into services:
- **UserService**: User management and data operations
- **SupportService**: FAQ and ticket management

### API Layer
RESTful endpoints organized by domain:
- **Users API**: User-related endpoints
- **Support API**: FAQ and ticket endpoints
- **AI Agent API**: Chat and AI interaction endpoints

## Running the Application

### Using the New Modular Structure

```bash
# Run the main application
python main_new.py

# Or run directly with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing the AI Agent

```bash
# Test the AI agent independently
python ai_agent_new.py
```

## Environment Setup

Make sure your `.env` file contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro
SECRET_KEY=your_secret_key_here
```

## API Documentation

Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Migration from Old Structure

The original `main.py` and `ai_agent.py` files are preserved for reference. The new structure provides:

1. **Better Organization**: Code is logically separated
2. **Easier Testing**: Components can be tested in isolation
3. **Improved Maintainability**: Changes are localized to specific modules
4. **Enhanced Scalability**: New features can be added without affecting existing code

## Development Guidelines

1. **Follow the layered architecture**: API → Service → Database
2. **Keep AI components modular**: Each AI component should have a single responsibility
3. **Use dependency injection**: Pass dependencies through constructors
4. **Maintain clear interfaces**: Use Pydantic schemas for data validation
5. **Add proper error handling**: Each layer should handle its own errors appropriately

## Future Enhancements

The modular structure makes it easy to add:
- Authentication middleware
- Caching layers
- Message queues for async processing
- Additional AI models or providers
- Monitoring and logging components
- API rate limiting
- Database migrations