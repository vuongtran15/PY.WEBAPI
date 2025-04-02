import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import uuid

from services.aidb_services import AIDBContext
from api.rosapi import rosapi
from services.ai_services import aisvr
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
            response = rosapi.conversation_get_command(chatinfo["chat_id"])
            # get object in command
            response = json.loads(response)
            conversation_id = response["ConversationId"]
            prompt = list(response["Prompt"])
            command = list(response["Command"])
            for cmd in command:
                commandType = cmd["CommandType"]
                if commandType == "TEXT_CHAT":
                    msgid = uuid.uuid4()
                    await aisvr.text_openai_chat(websocket, str(msgid), prompt)
                else:
                    await websocket.send_text(f"No command found for {commandType}!!")

        except WebSocketDisconnect:
            self.disconnect(chatid)


manager = ConnectionManager()
