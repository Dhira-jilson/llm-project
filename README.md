# LLM API - FastAPI Application

A FastAPI application serving TinyLlama for text generation.

## Features

- FastAPI framework for high performance
- TinyLlama (1.1B parameters) for efficient inference
- Proper error handling and logging
- Health check endpoints for Kubernetes
- Docker containerization
- Cloud Build integration

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Standard
uvicorn app:app --reload

# Production-like
uvicorn app:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for API documentation.

## Docker Build & Run

```bash
# Build image
docker build -t llm-api .

# Run container
docker run -p 8000:8000 llm-api
```

## Cloud Deployment

### Google Cloud Build

```bash
# Trigger build
gcloud builds submit --config=cloudbuild.yaml

# Or let Cloud Build auto-trigger from git
```

### Kubernetes with Skaffold

```bash
# Deploy
skaffold run

# Or for development with live reload
skaffold dev
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Kubernetes health check
- `POST /ask` - Generate text
  ```json
  {
    "prompt": "What is AI?",
    "max_length": 100
  }
  ```
- `GET /ui` - Web UI

## Environment Variables

- `HF_HOME` - Hugging Face cache directory (set in Dockerfile)
- `PYTHONUNBUFFERED` - Disable Python buffering

## Improvements Made

1. **Dockerfile**: Multi-stage build for smaller images, proper dependency separation
2. **requirements.txt**: Pinned versions for reproducibility
3. **app.py**: 
   - Startup event for model loading (prevents blocking requests)
   - Proper error handling and logging
   - Input validation with Pydantic
   - Health check endpoints
   - Better API documentation
4. **Cloud Build**: Proper configuration for GCP deployment
5. **.dockerignore**: Reduced image size by excluding unnecessary files
6. **skaffold.yaml**: Kubernetes development workflow

## Troubleshooting

- **Model download timeout**: Increase Cloud Build timeout (set to 1200s in cloudbuild.yaml)
- **Out of memory**: Use GPU nodes or increase machine type memory
- **Slow first request**: Model is pre-downloaded in Dockerfile startup
