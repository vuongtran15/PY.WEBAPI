import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from typing import  Dict

from services.aidb_services import AIDBContext



# chatid bao gồm tổ hợp empid__chatid__type__uuid. cách nhau bởi dấu __
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, chatid: str):
        await websocket.accept()
        self.active_connections[chatid] = websocket

        parts = chatid.split("__")
        chatinfo = {
            "emp_id": parts[0],
            "chat_id": parts[1],
            "type": parts[2],
            "uuid": parts[3]
        }
        
        # Insert chat connection info to database
        # Initialize database context
        db_context = AIDBContext()
        
        # Insert conversation to database with appropriate fields
        db_context.insert_conversation(
            id=chatinfo["chat_id"],
            emp_id=chatinfo["emp_id"],
            title=f"New Conversation",
            conversation_type=chatinfo["type"]
        )

    def disconnect(self, chatid: str):
        if chatid in self.active_connections:
            del self.active_connections[chatid]

    async def broadcast(self, message: str, sender_id: str):
        print(f"Broadcasting message: {message}")

        try:
            if sender_id in self.active_connections:
                conn = self.active_connections[sender_id]
            print(f"Sending message to {sender_id}: {message}")
            # wait 5s

            await asyncio.sleep(2)

            await conn.send_text(f"{message}")
        except WebSocketDisconnect:
            self.disconnect(sender_id)



manager = ConnectionManager()