from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
import app.models

from app.routers import auth
from app.routers import quizzes
from app.routers import questions
from app.routers import sessions
from app.routers import answers
from app.routers import leaderboard

from app.websocket.routes import router as websocket_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Live AI Quiz Engine",
    description="Real-time AI-powered classroom quiz platform",
    version="1.0.0"
)


# CORS configuration
# Allows the React frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(auth.router)
app.include_router(quizzes.router)
app.include_router(questions.router)
app.include_router(sessions.router)
app.include_router(answers.router)
app.include_router(leaderboard.router)

# Register WebSocket routes
app.include_router(websocket_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Live AI Quiz Engine API is running"
    }


# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }