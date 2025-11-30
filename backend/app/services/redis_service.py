import redis.asyncio as redis
import json
from typing import Optional
from app.config import get_settings

settings = get_settings()

class RedisService:
    """
    Redis service for pub/sub and caching
    Handles real-time incident notifications
    """
    
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
    
    async def connect(self):
        """Initialize Redis connection"""
        self.client = await redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        self.pubsub = self.client.pubsub()
        print("✅ Redis connected")
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.pubsub:
            await self.pubsub.close()
        if self.client:
            await self.client.close()
        print("👋 Redis disconnected")
    
    async def publish_incident(self, incident_id: int):
        """Publish incident event to channel"""
        await self.client.publish(
            "incidents:new",
            json.dumps({"incident_id": incident_id})
        )
    
    async def publish_incident_update(self, incident_id: int, status: str, data: dict = None):
        """Publish incident status update"""
        message = {
            "incident_id": incident_id,
            "status": status,
            "data": data or {}
        }
        await self.client.publish(
            f"incidents:updates:{incident_id}",
            json.dumps(message)
        )
    
    async def listen_for_incidents(self):
        """Background task to listen for incident events"""
        await self.pubsub.subscribe("incidents:new")
        
        print("👂 Listening for incidents on Redis...")
        
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                print(f"🔔 New incident received: {data}")
                
                # Broadcast to WebSocket clients
                from app.services.websocket_manager import manager
                await manager.broadcast(data)
    
    async def cache_incident(self, incident_id: int, data: dict, ttl: int = 3600):
        """Cache incident data"""
        await self.client.setex(
            f"incident:{incident_id}",
            ttl,
            json.dumps(data)
        )
    
    async def get_cached_incident(self, incident_id: int) -> Optional[dict]:
        """Retrieve cached incident"""
        data = await self.client.get(f"incident:{incident_id}")
        if data:
            return json.loads(data)
        return None
    
    async def set_key_expiry_listener(self, callback):
        """Listen for key expiry events (for SLA monitoring)"""
        await self.client.config_set("notify-keyspace-events", "Ex")
        
        keyspace_pubsub = self.client.pubsub()
        await keyspace_pubsub.psubscribe("__keyevent@0__:expired")
        
        async for message in keyspace_pubsub.listen():
            if message["type"] == "pmessage":
                expired_key = message["data"]
                await callback(expired_key)
