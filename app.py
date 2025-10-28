from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(title="AI Visibility Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    """Serve the frontend"""
    try:
        return FileResponse("frontend/index.html")
    except:
        return HTMLResponse("""
        <html>
            <head><title>AI Visibility Tool</title></head>
            <body>
                <h1>🔍 AI Visibility Tool</h1>
                <p>Application is starting up...</p>
                <p>If you see this message, the frontend files are not found.</p>
            </body>
        </html>
        """)

@app.get("/api/")
async def api_root():
    """API health check"""
    return {"message": "AI Visibility Tool API", "version": "1.0.0", "status": "operational"}

@app.get("/api/keywords", methods=["POST"])
async def extract_keywords():
    """Mock keywords endpoint"""
    return {"keywords": ["AI", "visibility", "analysis", "brand", "optimization"]}

@app.get("/api/prompts", methods=["POST"])
async def generate_prompts():
    """Mock prompts endpoint"""
    return {"prompts": ["What is AI visibility?", "How to improve brand visibility?"]}

@app.get("/api/simulate", methods=["POST"])
async def simulate_analysis():
    """Mock analysis endpoint"""
    return {
        "visibility_percentage": 75.5,
        "platforms": {
            "chatgpt": {"score": 80, "position": 3},
            "perplexity": {"score": 70, "position": 5}
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "AI Visibility Tool API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
