from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load small open-source model
generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "LLM running"}

@app.post("/ask")
def ask(request: PromptRequest):
    result = generator(request.prompt, max_length=100)
    return {"reply": result[0]["generated_text"]}