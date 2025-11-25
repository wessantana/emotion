from fastapi import APIRouter

router = APIRouter()

@router.post("/engagement")
async def predict_engagement(vision_embedding:list, text_embedding:list):

    engagement_level:str
    
    return {"engagement_level": engagement_level}