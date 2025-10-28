"""Main FastAPI application - Clean and scalable"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import get_settings
from app.api.routes import router

# Load settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving frontend)
frontend_path = Path("/app/frontend")
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
@app.head("/")
async def root():
    """Root endpoint - Serve frontend"""
    from fastapi.responses import FileResponse
    import os
    
    frontend_file = Path("/app/frontend/index.html")
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    else:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content={"message": "Frontend not found", "api": "/api"},
            status_code=404
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

