import fastapi

router = fastapi.APIRouter()

@router.get("/")
async def users_get():
    return {"message": "Hello World1"}
