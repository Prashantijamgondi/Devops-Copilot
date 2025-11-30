from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.config import get_settings
from app.routes import incidents, webhooks, analytics
from app.services.redis_service import RedisService
from app.services.websocket_manager import ConnectionManager

settings = get_settings()

# WebSocket manager
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting DevOps Co-Pilot...")
    
    # Initialize Redis
    redis_service = RedisService()
    await redis_service.connect()
    app.state.redis = redis_service
    
    # Start background tasks
    asyncio.create_task(redis_service.listen_for_incidents())
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    await redis_service.disconnect()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "DevOps Co-Pilot API",
        "version": settings.API_VERSION,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)
