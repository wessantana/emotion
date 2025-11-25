from fastapi import FastAPI
from fastapi import APIRouter
from backend import analyze
from fusion import mlp
from llm import llm
from nlp import nlp
from vision import vision

app = FastAPI()

app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
app.include_router(vision.router, prefix="/vision", tags=["vision"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
app.include_router(nlp.router, prefix="/nlp", tags=["nlp"])
app.include_router(mlp.router, prefix="/fusion", tags=["fusion"])

@app.get("/")
async def root():
    return {"message": "API ON!"}
