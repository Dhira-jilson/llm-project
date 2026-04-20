from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

# Initialize client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/ask")
def ask(req: PromptRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # lightweight + supported
            contents=req.prompt
        )
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))