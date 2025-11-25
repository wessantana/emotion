from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/emotion")
async def analyze_image(image: UploadFile = File(...)):
    
    # these datas gonna be received from the IA model
    emotion: str
    embedding: list

    return {"emotion": emotion,
            "embedding": embedding
            }