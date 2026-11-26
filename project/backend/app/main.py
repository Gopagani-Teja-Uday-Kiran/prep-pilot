from fastapi import FastAPI 
from app.api.tutor import router as tutor_router

app=FastAPI(title="prepilot",description="AI powereded study and quiz",version="0.1.0")
@app.get("/")
def home():
    return {"message":"welcome to prepilot","status":"running"}
@app.get("/health")
def health():
    return {"message":"prepilot is healthy","status":"healthy"}

app.include_router(tutor_router)
