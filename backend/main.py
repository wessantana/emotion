from fastapi import FastAPI
from fastapi import APIRouter
from backend.routers import vision, llm, nlp, fusion

app = FastAPI()

app.include_router(vision.router, prefix="/vision", tags=["vision"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
app.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
app.include_router(fusion.router, prefix="/fusion", tags=["fusion"])

@app.get("/")
async def root():
    return {"message": "API ON!"}