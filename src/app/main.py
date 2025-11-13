# src/app/main.py
import os
from fastapi import FastAPI
from .api.v1 import router as v1_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Quiz Solver API", version="1.0")
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "ok", "service": "quiz-solver"}

# Run with: uvicorn src.app.main:app --reload
