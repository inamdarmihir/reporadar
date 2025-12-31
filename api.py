"""
FastAPI Server for GitHub Trending Agent
Provides REST API endpoints for interacting with the agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from app import agent

# Initialize FastAPI app
app = FastAPI(
    title="GitHub Trending Agent API",
    description="REST API for discovering GitHub trending repositories using natural language",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GitHub Trending Agent"}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the GitHub Trending Agent
    
    Args:
        request: ChatRequest with message and optional session_id
        
    Returns:
        ChatResponse with agent's response
    """
    try:
        # Run the agent
        response = agent.run(
            request.message,
            stream=request.stream,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=response.content,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "GitHub Trending Agent",
        "version": "2.0.0",
        "framework": "Agno",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    print("🚀 Starting GitHub Trending Agent API Server...")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔗 API Endpoint: http://localhost:8000/chat")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
