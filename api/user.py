import fastapi

router = fastapi.APIRouter()

@router.get("/login")
async def login():
    return {"message": "Hello World1"}
