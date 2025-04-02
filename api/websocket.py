import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import uuid

from services.aidb_services import AIDBContext
from api.rosapi import rosapi
from services.command_service import cmdsvr
# Initialize ROSApi


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

    async def broadcast(self, websocket: WebSocket, message: str, chatid: str):
        try:
            parts = chatid.split("__")
            chatinfo = {
                "emp_id": parts[0],
                "chat_id": parts[1],
                "type": parts[2],
                "uuid": parts[3]
            }
            rosapi.conversation_add_message(chatinfo["chat_id"], message)
            # get command from server
            command = rosapi.conversation_get_command(chatinfo["chat_id"])
            command = json.loads(command)
            command = list(command)
            
            for cmd in command:
                commandType = cmd["CommandType"]
                if commandType == "TEXT_CHAT":
                    await cmdsvr.command_text_chat(websocket, chatinfo["chat_id"])
                else:
                    await websocket.send_text(f"No command found for {commandType}!!")

        except WebSocketDisconnect:
            self.disconnect(chatid)


manager = ConnectionManager()
