from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from api.websocket import manager
import uvicorn
import ssl

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

# Add route for the chat API
from api.chat import router as chat_router
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

if __name__ == "__main__":
    # SSL Configuration
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('config/cert.pem', keyfile='config/key.pem')
    
    # Run with HTTPS
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        ssl_keyfile="config/key.pem",
        ssl_certfile="config/cert.pem"
    )