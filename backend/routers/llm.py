from fastapi import APIRouter

router = APIRouter()

@router.post("/recommend")
async def recommend():
    return