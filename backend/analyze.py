from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
import httpx
from dotenv import load_dotenv
import os
from backend.vision.vision import analyze_image
from backend.nlp.nlp import analyze_text
from backend.fusion.mlp import predict_engagement
from backend.llm.llm import generate_recommendation

load_dotenv()
API_URL = os.getenv("API_URL")

router = APIRouter()

@router.post("")
async def analyze(image: UploadFile = File(...), text_input: str = Form(...)):

    # here I need to verify if the image and the text are valid to, after that, call the functions

    allowed_image_types = ["image/jpeg", "image/png", "image/webp"]

    if image is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Imagem não pode ser vazia.")
    
    if not text_input or text_input.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Texto não pode ser vazio.")
    
    if image not in allowed_image_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tipo de imagem inválido: {image.content_type}. Use JPEG, PNG ou WEBP.")
    
    vision_response = analyze_image(image)

    nlp_response = analyze_text(text_input)

    fusion_response = predict_engagement(vision_embedding=vision_response["embedding"], text_embedding=nlp_response["embedding"])

    llm_response = generate_recommendation(emotion=vision_response["emotion"],
                                           sentiment=nlp_response["sentiment"],
                                           engagement_level=fusion_response["engagement_level"]
                                           )


    return {
        "facial_emotion":{vision_response["emotion"]},
        "text_sentiment":{nlp_response["sentiment"]},
        "engagement_level":{fusion_response["engagement_level"]},
        "suggestions":{llm_response["suggestions"]}
        }