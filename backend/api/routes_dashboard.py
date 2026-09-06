"""
api/routes_dashboard.py — GET /orphans route handler.

OWNER: Person A (backend/api/, backend/db/)
RESPONSIBILITY: Returns the orphan risk score list from the `orphan_scores` table,
sorted by risk_score descending. Matches the CONTRACTS.md GET /orphans response shape.
"""

from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

from agents.orchestrator import run_orphan_scan

router = APIRouter()


class OrphanEntity(BaseModel):
    """Single entity in the GET /orphans response — matches CONTRACTS.md exactly."""
    entity_id: str
    risk_score: float          # 0.0 – 1.0
    reason: str
    last_touched_by: str | None
    last_touched_at: str | None  # ISO 8601
    evidence_count: int


class OrphansResponse(BaseModel):
    """GET /orphans response — matches CONTRACTS.md exactly."""
    entities: list[OrphanEntity]


@router.get("/orphans", response_model=OrphansResponse)
async def get_orphans() -> OrphansResponse:
    """
    Return all entities scored as orphaned knowledge, sorted by risk_score descending.

    Triggers a fresh orphan scan via the orchestrator. For production, add caching.
    """
    # TODO(Person A): add Redis/in-memory cache with TTL to avoid rescanning on every request
    entities = run_orphan_scan()
    return OrphansResponse(entities=[OrphanEntity(**e) for e in entities])
