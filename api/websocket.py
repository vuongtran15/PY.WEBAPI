from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def broadcast(self, message: str, sender_id: str):
        disconnected_clients = []
        for client_id, connection in self.active_connections.items():
            try:
                if client_id != sender_id:  # Don't send message back to sender
                    print(f"Sending message to {client_id}: {message}")
                    await connection.send_text(f"{sender_id}: {message}")
            except WebSocketDisconnect:
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

manager = ConnectionManager()