"""
api/routes_entity.py — GET /entity/{entity_id}/timeline route handler.

OWNER: Person A (backend/api/, backend/db/)
RESPONSIBILITY: Returns a chronologically sorted event timeline for a specific
entity. Matches the CONTRACTS.md GET /entity/{entity_id}/timeline response shape.
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.models import get_timeline_for_entity

router = APIRouter()


class TimelineEvent(BaseModel):
    """Single event in the entity timeline — matches CONTRACTS.md exactly."""
    type: str       # "commit" | "pr" | "ticket" | "slack"
    id: str
    timestamp: str  # ISO 8601
    summary: str
    author: str


class TimelineResponse(BaseModel):
    """GET /entity/{entity_id}/timeline response — matches CONTRACTS.md exactly."""
    entity_id: str
    events: list[TimelineEvent]


@router.get("/entity/{entity_id:path}/timeline", response_model=TimelineResponse)
async def get_entity_timeline(entity_id: str) -> TimelineResponse:
    """
    Return all historical events for a code entity, sorted chronologically ascending.

    entity_id uses `:path` converter to allow slashes (e.g. "src/billing/invoice.py::parseInvoice").
    Returns 404 if the entity is not known.
    """
    # TODO(Person A): validate entity exists first, raise 404 if not found
    events = get_timeline_for_entity(entity_id)
    if events is None:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found.")
    return TimelineResponse(
        entity_id=entity_id,
        events=[TimelineEvent(**e) for e in events],
    )
