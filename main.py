from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
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
            await manager.broadcast(websocket, data, chatid)
    except WebSocketDisconnect:
        manager.disconnect(chatid)