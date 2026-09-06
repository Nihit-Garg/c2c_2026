"""
agents/orchestrator.py — Sequential multi-agent pipeline coordinator.

OWNER: Person B (backend/agents/)
RESPONSIBILITY: Wires the three-step pipeline (retrieve → synthesize → verify) into
a single callable function that the FastAPI route handlers call. No heavy agent
framework — pure sequential Python function calls, as decided in ARCHITECTURE.md.

This is the ONLY file that imports from multiple agents. Route handlers
import only from orchestrator, not from individual agent files directly.
"""

from __future__ import annotations
from agents import retriever_agent, synthesis_agent, contradiction_agent, orphan_detector_agent


def run_query_pipeline(query: str, entity_id: str | None = None) -> dict:
    """
    Full query pipeline: resolve entity → retrieve evidence → synthesize → detect contradictions.

    Args:
        query:     Free-text user question (e.g. "why is parseInvoice written this way").
        entity_id: Optional pre-resolved entity ID. If None, retriever resolves it from query.

    Returns:
        Response dict exactly matching CONTRACTS.md POST /query response shape:
        {
            "answer": str,
            "confidence": "high" | "medium" | "low",
            "evidence": [ {source_type, source_id, snippet, author, timestamp, url} ],
            "contradictions": [ {claim_a, source_a, claim_b, source_b} ]
        }
        If no evidence found, returns the canonical "No historical evidence found." response.
    """
    # TODO(Person B): implement sequential pipeline:
    # 1. if not entity_id: entity_id = retriever_agent.resolve_entity_from_query(query)
    # 2. evidence = retriever_agent.retrieve_evidence(entity_id) if entity_id else []
    # 3. if not evidence: return _no_evidence_response()
    # 4. context = retriever_agent.build_evidence_context_string(evidence)
    # 5. synthesis = synthesis_agent.synthesize(query, entity_id, evidence, context)
    # 6. contradictions = contradiction_agent.detect_contradictions(entity_id, evidence)
    # 7. return assembled response dict
    raise NotImplementedError


def run_orphan_scan() -> list[dict]:
    """
    Trigger a full orphan score recomputation for all entities.
    Called by GET /orphans route on-demand (or cached).

    Returns:
        Sorted list of orphan_score dicts (risk_score descending) matching
        CONTRACTS.md GET /orphans response shape entity list.
    """
    # TODO(Person B): call orphan_detector_agent.score_all_entities(), sort by risk_score desc
    raise NotImplementedError


def _no_evidence_response() -> dict:
    """Return the canonical CONTRACTS.md 'no evidence' response."""
    return {
        "answer": "No historical evidence found.",
        "confidence": "low",
        "evidence": [],
        "contradictions": [],
    }
