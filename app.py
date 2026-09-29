"""
Agentic AI Team Former - Application Entry Point
File: app.py
Description: FastAPI app factory. Wires together routes, static files, and the frontend.

Project Structure:
  models.py   - Pydantic data models
  database.py - In-memory student DB + seed data
  agent.py    - AgenticTeamFormer core reasoning engine
  routes.py   - API route handlers (APIRouter)
  app.py      - App entry point (this file)
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes import router

app = FastAPI(title="Agentic AI Project Team Former", version="1.0.0")

# Register all API routes under /api prefix
app.include_router(router, prefix="/api")

# Serve the React/JS frontend static assets
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """Serves the main frontend UI."""
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
