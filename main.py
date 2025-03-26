from fastapi import FastAPI
from api import user

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World aaa"}

app.include_router(user.router, tags=["user"])

