from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# Create FastAPI app
app = FastAPI(title="AI Visibility Tool", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include API routes
from backend.app.api.routes import router
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "AI Visibility Tool API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
