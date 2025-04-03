
import asyncio
import json
from uuid import UUID
from fastapi import WebSocket
from openai import OpenAI


class AIService:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://172.19.137.30:11435/v1",
            api_key="sk-4e6d7f0c-5a2b-4b3c-9f8e-1c8f6a2b7d1a",
        )

    async def text_openai_chat(self, websocket: WebSocket, msgid: str, message: list) -> None:
        try:
            response = self.client.chat.completions.create(
                model="gemma3:27b",
                messages=message,
                stream=True
            )
            bot_reply = ""
            for chunk in response:
                if chunk.choices[0].finish_reason == "stop":
                    break
                if chunk.choices[0].delta is not None:
                    delta = chunk.choices[0].delta
                    await websocket.send_text(json.dumps({
                        "msgid": msgid,
                        "dataType": "text",
                        "content": delta.content
                    }))
                    bot_reply += delta.content
                    await asyncio.sleep(0.01)
            await websocket.send_text(json.dumps({
                "msgid": msgid,
                "dataType": "text",
                "content": 'END_OF_MESSAGE'
            }))
            return bot_reply
        except Exception as e:
            await websocket.send_text(json.dumps({
                "msgid": msgid,
                "dataType": "text",
                "content": 'END_OF_MESSAGE'
            }))
            return ""


aisvr = AIService()
