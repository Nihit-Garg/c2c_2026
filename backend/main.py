"""
main.py — FastAPI application entry point.

OWNER: Person A (backend/api/, backend/db/)
RESPONSIBILITY: Creates the FastAPI app, registers all routers, and configures
CORS so the Vite frontend (localhost:5173) can talk to the API (localhost:8000).

Run with:
    cd backend && uvicorn main:app --reload --port 8000
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes_query import router as query_router
from api.routes_dashboard import router as dashboard_router
from api.routes_entity import router as entity_router

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hook."""
    logger.info("🚀 Code Archaeology API starting up...")
    # Validate all required config — crashes fast if anything is missing
    settings.validate()
    logger.info(f"✅ Config validated | LLM: {settings.LLM_PROVIDER}/{settings.LLM_MODEL}")
    logger.info(f"✅ Supabase: {settings.SUPABASE_URL}")
    yield
    logger.info("🛑 Code Archaeology API shutting down.")


app = FastAPI(
    title="Code Archaeology API",
    description="Multi-agent system that mines git history, PR threads, Jira, and Slack to explain WHY legacy code exists.",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS (allow Vite dev server + any localhost port during dev) ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(query_router)       # POST /query
app.include_router(dashboard_router)   # GET  /orphans
app.include_router(entity_router)      # GET  /entity/{entity_id}/timeline


@app.get("/health")
async def health_check() -> dict:
    """Simple liveness probe — tests config + returns Supabase project URL."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "llm_provider": settings.LLM_PROVIDER,
        "llm_model": settings.LLM_MODEL,
        "supabase_url": settings.SUPABASE_URL,
    }
