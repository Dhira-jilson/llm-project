from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from transformers import pipeline
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM API", version="1.0.0")

# Global model variable
generator = None

# Load model on startup
@app.on_event("startup")
async def load_model():
    global generator
    try:
        logger.info("Loading TinyLlama model...")
        generator = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            device=-1  # Use CPU, set to 0 for GPU
        )
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    max_length: int = Field(default=100, ge=10, le=500)

@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "LLM API running",
        "model": "TinyLlama-1.1B-Chat-v1.0"
    }

@app.get("/health")
def health_check():
    """Kubernetes health check endpoint"""
    return {"status": "ok"}

@app.post("/ask")
def ask(request: PromptRequest):
    """Generate text based on prompt"""
    if generator is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    try:
        result = generator(
            request.prompt,
            max_length=request.max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )
        return {
            "prompt": request.prompt,
            "reply": result[0]["generated_text"]
        }
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

@app.get("/ui")
def serve_ui():
    """Serve the HTML UI"""
    return FileResponse("index.html", media_type="text/html")