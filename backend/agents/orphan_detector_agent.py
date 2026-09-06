"""
agents/orphan_detector_agent.py — Batch-scores all entities for orphaned knowledge risk.

OWNER: Person B (backend/agents/)
RESPONSIBILITY: Iterates all entities in the DB, computes a risk score using the
rule-based + LLM hybrid approach defined in ARCHITECTURE.md, and upserts results
into the `orphan_scores` table. Called by the /orphans route.

Scoring weights (rule-based component, as defined in graph_builder.py):
  bus_factor=1   → +0.40
  evidence_count=0 → +0.40
  departed author  → +0.20
  fan_in=0 (stretch) → +0.10
LLM component: optional summary of WHY it's risky (cheap short call).
"""

from __future__ import annotations
from db import models


def score_all_entities() -> list[dict]:
    """
    Compute and persist orphan risk scores for every entity in the DB.

    Returns:
        List of upserted orphan_score dicts matching CONTRACTS.md orphan_scores schema:
        [{entity_id, risk_score, reason, last_touched_by, last_touched_at, evidence_count}]
    """
    # TODO(Person B): call resolution.graph_builder.compute_orphan_scores_for_all_entities()
    # optionally call _generate_llm_reason() for entities with risk_score > 0.6
    raise NotImplementedError


def score_single_entity(entity_id: str) -> dict:
    """
    Compute and persist orphan score for a single entity (used for incremental updates).

    Args:
        entity_id: e.g. "src/billing/invoice.py::parseInvoice"

    Returns:
        The upserted orphan_score dict.
    """
    # TODO(Person B): same logic as score_all_entities but scoped to one entity
    raise NotImplementedError


def _generate_llm_reason(entity_id: str, heuristic_reason: str, evidence: list[dict]) -> str:
    """
    Optional: ask the LLM to generate a richer human-readable reason for high-risk
    orphans. Falls back to heuristic_reason if LLM call fails.

    Args:
        entity_id:        The entity being scored.
        heuristic_reason: The rule-based reason string (always safe to display).
        evidence:         Evidence items retrieved for this entity.

    Returns:
        A 1-2 sentence reason string for display in the Orphan Dashboard.
    """
    # TODO(Person B): short LLM call via synthesis_agent._call_llm()
    # Prompt: "In 1-2 sentences, explain why {entity_id} may be orphaned knowledge.
    #          Evidence: {heuristic_reason}. No code, no formatting, just a sentence."
    raise NotImplementedError
