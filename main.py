from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from api import user,chat
from api.websocket import manager

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# WebSocket endpoint
@app.websocket("/ws/{chatid}")
async def websocket_endpoint(websocket: WebSocket, chatid: str):
    await manager.connect(websocket, chatid)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, chatid)
    except WebSocketDisconnect:
        manager.disconnect(chatid)

# Include REST API routes
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])