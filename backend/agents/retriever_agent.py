"""
agents/retriever_agent.py — Pulls all evidence for a queried code entity.

OWNER: Person B (backend/agents/)
RESPONSIBILITY: Given an entity_id (or a free-text query to resolve one), fetch
all linked evidence from Supabase (commits, PRs, tickets, Slack) and return a
structured evidence list. This is step 1 of the sequential pipeline defined in
ARCHITECTURE.md: retrieve → synthesize → verify.

Does NOT call any LLM. Pure DB retrieval + optional fuzzy entity resolution.
"""

from __future__ import annotations
from db import models


def resolve_entity_from_query(query: str) -> str | None:
    """
    Given a free-text query (e.g. "why is parseInvoice like this"), attempt to
    identify the best matching entity_id using fuzzy matching against known entities.

    Args:
        query: Free-text user question.

    Returns:
        Best-match entity_id string, or None if no confident match found.
    """
    # TODO(Person B): fetch all entity ids from DB, use rapidfuzz.process.extractOne
    # against file_path + function_name tokens
    raise NotImplementedError


def retrieve_evidence(entity_id: str) -> list[dict]:
    """
    Fetch all evidence linked to an entity, normalized to a flat list of
    evidence items suitable for the /query response and for the synthesis agent.

    Args:
        entity_id: e.g. "src/billing/invoice.py::parseInvoice"

    Returns:
        List of evidence dicts, each matching the `evidence` item shape from CONTRACTS.md:
        [{source_type, source_id, snippet, author, timestamp, url}]
        Sorted by timestamp descending (most recent first).

    Returns [] if no evidence found (not an error — valid "no history" case).
    """
    # TODO(Person B): call db.models.get_all_evidence_for_entity(entity_id)
    # map each row to the CONTRACTS.md evidence shape, sort by timestamp desc
    raise NotImplementedError


def build_evidence_context_string(evidence: list[dict]) -> str:
    """
    Format a list of evidence dicts into a compact string block suitable for
    inclusion in an LLM prompt (used by synthesis_agent).

    Args:
        evidence: Output of retrieve_evidence().

    Returns:
        Multi-line string with each evidence item as a labelled block.
    """
    # TODO(Person B): format as "--- [commit a1b2c3] by Alice on 2022-03-15:\n<snippet>\n"
    raise NotImplementedError
