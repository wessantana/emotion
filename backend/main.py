from fastapi import FastAPI
from backend.routers import *

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "API ON!"}