from fastapi import APIRouter, File, Form

router = APIRouter()

@router.post("/analyze")
async def analyze_text(text_input: str = Form(...)):

    sentiment: str
    embedding: list
    
    return {"sentiment": sentiment,
            "embedding": embedding
            }