from fastapi import APIRouter

router = APIRouter()

@router.post("/emotion")
async def emotion(payload: dict):
    return