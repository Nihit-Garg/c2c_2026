"""
db/models.py — Supabase client wrapper and typed data access layer.

OWNER: Person A (backend/db/)
RESPONSIBILITY: Single place where all Supabase queries happen. Every other module
calls functions here instead of touching the supabase client directly, so we can
swap the DB layer in tests. Table names must exactly match schema.sql.
"""

from __future__ import annotations
from functools import lru_cache
from typing import Any

from supabase import create_client, Client
from config import settings


# ── Client singleton ──────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def get_client() -> Client:
    """Return a cached Supabase client using the service-role key (full write access)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase credentials not configured. Check your .env file.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


# ── Entities ──────────────────────────────────────────────────────────────────

def upsert_entity(entity: dict) -> dict:
    """
    Insert or update a row in the `entities` table.

    Args:
        entity: dict with keys {id, file_path, function_name, entity_type}
    Returns:
        The upserted row as returned by Supabase.
    """
    client = get_client()
    result = client.table("entities").upsert(entity).execute()
    return result.data[0] if result.data else {}


def get_entity(entity_id: str) -> dict | None:
    """
    Fetch a single entity row by primary key.

    Args:
        entity_id: e.g. "src/invoice.py::parseInvoice"
    Returns:
        Entity dict or None if not found.
    """
    client = get_client()
    result = client.table("entities").select("*").eq("id", entity_id).execute()
    return result.data[0] if result.data else None


def get_all_entity_ids() -> list[str]:
    """Return all entity IDs — used by retriever_agent for fuzzy matching."""
    client = get_client()
    result = client.table("entities").select("id").execute()
    return [row["id"] for row in result.data]


# ── Commits ───────────────────────────────────────────────────────────────────

def upsert_commit(commit: dict) -> dict:
    """
    Insert or update a row in the `commits` table.

    Args:
        commit: dict with keys {sha, author, author_email, timestamp, message, diff_summary}
    """
    client = get_client()
    result = client.table("commits").upsert(commit).execute()
    return result.data[0] if result.data else {}


def get_commits_for_entity(entity_id: str) -> list[dict]:
    """
    Return all commits linked to an entity via the `links` table.
    """
    client = get_client()
    # Get source_ids for commits linked to this entity
    links = (
        client.table("links")
        .select("source_id")
        .eq("entity_id", entity_id)
        .eq("source_type", "commit")
        .execute()
    )
    if not links.data:
        return []
    sha_list = [l["source_id"] for l in links.data]
    result = client.table("commits").select("*").in_("sha", sha_list).execute()
    return result.data or []


# ── PRs ───────────────────────────────────────────────────────────────────────

def upsert_pr(pr: dict) -> dict:
    """Insert or update a row in the `prs` table."""
    client = get_client()
    result = client.table("prs").upsert(pr).execute()
    return result.data[0] if result.data else {}


def get_prs_for_entity(entity_id: str) -> list[dict]:
    """Return all PRs linked to an entity via the `links` table."""
    client = get_client()
    links = (
        client.table("links")
        .select("source_id")
        .eq("entity_id", entity_id)
        .eq("source_type", "pr")
        .execute()
    )
    if not links.data:
        return []
    pr_ids = [l["source_id"] for l in links.data]
    result = client.table("prs").select("*").in_("id", pr_ids).execute()
    return result.data or []


# ── Tickets ───────────────────────────────────────────────────────────────────

def upsert_ticket(ticket: dict) -> dict:
    """Insert or update a row in the `tickets` table."""
    client = get_client()
    result = client.table("tickets").upsert(ticket).execute()
    return result.data[0] if result.data else {}


def get_tickets_for_entity(entity_id: str) -> list[dict]:
    """Return all tickets linked to an entity via the `links` table."""
    client = get_client()
    links = (
        client.table("links")
        .select("source_id")
        .eq("entity_id", entity_id)
        .eq("source_type", "ticket")
        .execute()
    )
    if not links.data:
        return []
    ticket_ids = [l["source_id"] for l in links.data]
    result = client.table("tickets").select("*").in_("id", ticket_ids).execute()
    return result.data or []


# ── Slack Messages ────────────────────────────────────────────────────────────

def upsert_slack_message(msg: dict) -> dict:
    """Insert or update a row in the `slack_messages` table."""
    client = get_client()
    result = client.table("slack_messages").upsert(msg).execute()
    return result.data[0] if result.data else {}


def get_slack_for_entity(entity_id: str) -> list[dict]:
    """Return all Slack messages linked to an entity via the `links` table."""
    client = get_client()
    links = (
        client.table("links")
        .select("source_id")
        .eq("entity_id", entity_id)
        .eq("source_type", "slack")
        .execute()
    )
    if not links.data:
        return []
    msg_ids = [l["source_id"] for l in links.data]
    result = client.table("slack_messages").select("*").in_("id", msg_ids).execute()
    return result.data or []


# ── Links (graph) ─────────────────────────────────────────────────────────────

def insert_link(entity_id: str, source_type: str, source_id: str, relation: str) -> dict:
    """
    Insert a row into the `links` join table.

    Args:
        entity_id:   e.g. "src/billing/invoice.py::parseInvoice"
        source_type: "commit" | "pr" | "ticket" | "slack"
        source_id:   FK into the relevant source table
        relation:    "introduced_by" | "discussed_in" | "resolves" | "references"
    """
    client = get_client()
    row = {
        "entity_id": entity_id,
        "source_type": source_type,
        "source_id": source_id,
        "relation": relation,
    }
    result = client.table("links").insert(row).execute()
    return result.data[0] if result.data else {}


def get_all_evidence_for_entity(entity_id: str) -> list[dict]:
    """
    Return all evidence rows (commits + PRs + tickets + slack) linked to an entity,
    as a flat list with a `source_type` discriminator field.

    Each row has the raw source-table fields plus `source_type` and `relation`.
    Used by retriever_agent.py.
    """
    evidence: list[dict] = []

    # Commits
    for commit in get_commits_for_entity(entity_id):
        evidence.append({**commit, "source_type": "commit", "source_id": commit["sha"]})

    # PRs
    for pr in get_prs_for_entity(entity_id):
        evidence.append({**pr, "source_type": "pr", "source_id": pr["id"]})

    # Tickets
    for ticket in get_tickets_for_entity(entity_id):
        evidence.append({**ticket, "source_type": "ticket", "source_id": ticket["id"]})

    # Slack
    for msg in get_slack_for_entity(entity_id):
        evidence.append({**msg, "source_type": "slack", "source_id": msg["id"]})

    # Sort by timestamp ascending
    evidence.sort(key=lambda x: x.get("timestamp") or x.get("merged_at") or x.get("created_at") or "")
    return evidence


# ── Orphan Scores ─────────────────────────────────────────────────────────────

def upsert_orphan_score(score: dict) -> dict:
    """
    Insert or update a row in the `orphan_scores` table.

    Args:
        score: dict with keys {entity_id, risk_score, reason, last_touched_by,
                               last_touched_at, evidence_count}
    """
    client = get_client()
    result = client.table("orphan_scores").upsert(score).execute()
    return result.data[0] if result.data else {}


def get_all_orphan_scores(limit: int = 100) -> list[dict]:
    """
    Return all orphan scores sorted by risk_score descending.
    Used by GET /orphans route.
    """
    client = get_client()
    result = (
        client.table("orphan_scores")
        .select("*")
        .order("risk_score", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


# ── Timeline (for GET /entity/{id}/timeline) ──────────────────────────────────

def get_timeline_for_entity(entity_id: str) -> list[dict] | None:
    """
    Return a chronologically sorted list of all events (commit/pr/ticket/slack)
    for an entity. Each item has: {type, id, timestamp, summary, author}.

    Returns None if the entity doesn't exist in the DB.
    """
    # First verify entity exists
    entity = get_entity(entity_id)
    if entity is None:
        return None

    raw_evidence = get_all_evidence_for_entity(entity_id)
    events = []

    for item in raw_evidence:
        source_type = item.get("source_type", "")

        if source_type == "commit":
            events.append({
                "type": "commit",
                "id": item.get("sha", item.get("source_id", "")),
                "timestamp": item.get("timestamp", ""),
                "summary": item.get("message", ""),
                "author": item.get("author", ""),
            })
        elif source_type == "pr":
            events.append({
                "type": "pr",
                "id": item.get("source_id", item.get("id", "")),
                "timestamp": item.get("merged_at", ""),
                "summary": item.get("title", ""),
                "author": item.get("author", ""),
            })
        elif source_type == "ticket":
            events.append({
                "type": "ticket",
                "id": item.get("source_id", item.get("id", "")),
                "timestamp": item.get("created_at", ""),
                "summary": item.get("title", ""),
                "author": "",  # Jira tickets don't track author in our schema
            })
        elif source_type == "slack":
            events.append({
                "type": "slack",
                "id": item.get("source_id", item.get("id", "")),
                "timestamp": item.get("timestamp", ""),
                "summary": item.get("text", "")[:120],   # truncate for timeline display
                "author": item.get("author", ""),
            })

    # Sort chronologically ascending (earliest first)
    events.sort(key=lambda x: x.get("timestamp") or "")
    return events
