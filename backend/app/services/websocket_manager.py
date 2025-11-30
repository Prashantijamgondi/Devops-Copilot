from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔌 New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.remove(websocket)
        print(f"🔌 WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.remove(conn)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        await websocket.send_json(message)

manager = ConnectionManager()
