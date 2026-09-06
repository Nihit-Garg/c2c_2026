"""
resolution/graph_builder.py — Builds the knowledge graph from the `links` table.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: After all linker passes are complete, compute aggregate graph
statistics (bus factor, evidence density, fan-in) used by the orphan detector.
Also provides in-memory graph traversal helpers for the retriever agent.
The graph is stored relationally in Supabase (links table), not in a separate
graph DB — see ARCHITECTURE.md.
"""

from __future__ import annotations


def compute_orphan_scores_for_all_entities() -> list[dict]:
    """
    Compute orphan risk scores for every entity in the DB and upsert them
    into the `orphan_scores` table.

    Scoring heuristic (rule-based, see ARCHITECTURE.md):
    - bus_factor=1 (only one author ever touched it) → +0.4
    - evidence_count=0 (no PR/ticket/slack links) → +0.4
    - last_touched_by is a "departed" author (zero commits in last N days) → +0.2
    - fan_in=0 (no other file imports/calls it) → +0.1 (stretch)

    Returns:
        List of upserted orphan_score dicts.
    """
    # TODO(Person C): fetch all entities, compute each heuristic, upsert scores
    raise NotImplementedError


def get_evidence_subgraph(entity_id: str) -> dict:
    """
    Return an in-memory subgraph of all nodes connected to an entity,
    one hop out (entity → links → source records).

    Args:
        entity_id: e.g. "src/billing/invoice.py::parseInvoice"

    Returns:
        dict: {
            "entity": {...},
            "commits": [...],
            "prs": [...],
            "tickets": [...],
            "slack": [...]
        }
    Used by retriever_agent.py to gather evidence without N+1 queries.
    """
    # TODO(Person C): call db.models.get_all_evidence_for_entity, split by source_type
    raise NotImplementedError


def identify_departed_authors(days_threshold: int = 180) -> list[str]:
    """
    Return a list of author emails with zero commits in the most recent
    `days_threshold` days of repository history.

    Args:
        days_threshold: Number of days to look back. Default 180 (≈6 months).

    Returns:
        List of author_email strings considered "departed".
    See ARCHITECTURE.md: "departed engineer" simulation decision.
    """
    # TODO(Person C): query commits table, group by author_email, filter
    raise NotImplementedError
