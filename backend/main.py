import sys
import pathlib

# Ensure project root is on sys.path so imports like `from backend.utils import ...`
# work even if the process is started with the current working directory set to
# the `backend/` folder (for example: `cd backend && python -m uvicorn main:app`).
project_root = pathlib.Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base
from routers import auth, users, vehicles, breakdowns, service_providers, assistance, upload
# removed unused import: middleware.auth.get_current_user (module not present in repo)
from websocket_manager import websocket_manager

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Vehicle Breakdown Assistance Management System",
    description="A comprehensive system for managing vehicle breakdowns with real-time assistance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
# Read allowed origins from environment variable
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = []

if allowed_origins_env:
    # Split comma-separated origins and strip whitespace
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
else:
    # Default origins for development
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

print(f"[CORS] Allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(breakdowns.router, prefix="/api/breakdowns", tags=["Breakdowns"])
app.include_router(service_providers.router, prefix="/api/service-providers", tags=["Service Providers"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(assistance.router, prefix="/api/assistance", tags=["Assistance"])

# Mount static files
from fastapi.staticfiles import StaticFiles
os.makedirs("uploads", exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory="uploads"), name="uploads")

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.handle_message(client_id, data)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(client_id)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Vehicle Breakdown Assistance Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )
