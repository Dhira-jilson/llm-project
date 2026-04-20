from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/ask")
def ask(req: PromptRequest):
    try:
        response = model.generate_content(req.prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))