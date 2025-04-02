import json
import uuid
from fastapi import WebSocket

from api.rosapi import rosapi
from services.ai_services import aisvr
import datetime


class CommandServices:
    # def __init__(self):
    async def command_text_chat(self, websocket: WebSocket, chatid: str) -> None:
        try:
            prompt = rosapi.conversation_get_prompt(chatid)
            prompt = json.loads(prompt)
            prompt = list(prompt)

            msgid = uuid.uuid4()

            bot_reply =await aisvr.text_openai_chat(websocket, str(msgid), prompt)

            # save message to server
            msgModel = [
                {
                    "id": str(msgid),
                    "text": bot_reply,
                    "sender": "assistant",
                    "dataType": "text",
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
            
            rosapi.conversation_add_message(chatid, json.dumps(msgModel))


            return bot_reply
        except Exception as e:
            return ""

cmdsvr = CommandServices()