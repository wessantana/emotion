from fastapi import APIRouter

router = APIRouter()

@router.post("/engagement")
async def engagement():
    return