from fastapi import FastAPI 

app=FastAPI(title="prepilot",description="AI powereded study and quiz",version="0.1.0")
@app.get("/")
def home():
    return {"message":"welcome to prepilot","status":"running"}
@app.get("/health")
def health():
    return {"message":"prepilot is healthy","status":"healthy"}