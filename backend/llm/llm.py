from fastapi import APIRouter

router = APIRouter()

@router.post("/recommend")
async def generate_recommendation(emotion:str, sentiment:str, engagement_level: str, context:str):

    suggestions: str
    
    return {"suggestions": suggestions}