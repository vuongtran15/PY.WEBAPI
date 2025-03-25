import fastapi

router = fastapi.APIRouter()

@router.get("/")
async def users_get():
    return {"message": " 1123123 ádasdHello World 123123"}