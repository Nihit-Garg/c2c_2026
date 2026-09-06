"""
api/routes_query.py — POST /query route handler.

OWNER: Person A (backend/api/, backend/db/)
RESPONSIBILITY: Validates the incoming request body, calls the agent orchestrator,
and returns a response exactly matching the CONTRACTS.md POST /query shape.
Do not add business logic here — delegate entirely to orchestrator.run_query_pipeline().
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.orchestrator import run_query_pipeline

router = APIRouter()


class QueryRequest(BaseModel):
    """POST /query request body — matches CONTRACTS.md."""
    query: str
    entity_id: str | None = None   # optional; backend resolves if omitted


class EvidenceItem(BaseModel):
    """Single evidence item in the /query response."""
    source_type: str   # "commit" | "pr" | "ticket" | "slack"
    source_id: str
    snippet: str
    author: str
    timestamp: str     # ISO 8601
    url: str | None


class ContradictionItem(BaseModel):
    """Single contradiction pair in the /query response."""
    claim_a: str
    source_a: str
    claim_b: str
    source_b: str


class QueryResponse(BaseModel):
    """POST /query response — matches CONTRACTS.md exactly."""
    answer: str
    confidence: str    # "high" | "medium" | "low"
    evidence: list[EvidenceItem]
    contradictions: list[ContradictionItem]


@router.post("/query", response_model=QueryResponse)
async def query_entity(body: QueryRequest) -> QueryResponse:
    """
    Main query endpoint. Runs the full retrieve → synthesize → verify pipeline.

    - If entity_id is omitted, backend fuzzy-resolves it from the query text.
    - If no evidence is found, returns the canonical no-evidence response (not a 404).
    """
    # TODO(Person A): call run_query_pipeline, wrap in try/except for 500 errors
    result = run_query_pipeline(query=body.query, entity_id=body.entity_id)
    return QueryResponse(**result)
