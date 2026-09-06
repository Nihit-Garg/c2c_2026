"""
resolution/entity_linker.py — Links commits/PRs/tickets/Slack to code entities.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: After raw ingestion, scan all text sources (commit messages, PR
descriptions, ticket titles, Slack messages) for references to entity IDs, file
paths, function names, or JIRA ticket IDs using regex + rapidfuzz fuzzy matching.
Writes rows into the `links` table via db.models.insert_link.
"""

from __future__ import annotations
from rapidfuzz import fuzz


# Minimum fuzzy similarity score (0-100) to accept a link
FUZZY_THRESHOLD = 80


def link_commits_to_entities(entity_ids: list[str]) -> int:
    """
    For every commit in the DB, scan its message and diff_summary for mentions of
    known entity IDs or file paths, then insert a link row.

    Args:
        entity_ids: All known entity IDs (from entities table).

    Returns:
        Number of new link rows inserted.
    """
    # TODO(Person C): fetch all commits via db.models, iterate, fuzzy match, insert links
    raise NotImplementedError


def link_prs_to_entities(entity_ids: list[str]) -> int:
    """
    For every PR in the DB, scan title + description for entity references.

    Args:
        entity_ids: All known entity IDs.

    Returns:
        Number of new link rows inserted.
    """
    # TODO(Person C):
    raise NotImplementedError


def link_tickets_to_prs() -> int:
    """
    Match ticket IDs (e.g. "JIRA-4421") mentioned in commit messages or PR
    descriptions. Insert links between ticket↔commit and ticket↔pr where found.

    Returns:
        Number of new link rows inserted.
    """
    # TODO(Person C): regex r"JIRA-\d+" across commit messages and PR descriptions
    raise NotImplementedError


def link_slack_to_entities(entity_ids: list[str]) -> int:
    """
    Scan Slack messages for mentions of entity IDs, file paths, or function names.

    Args:
        entity_ids: All known entity IDs.

    Returns:
        Number of new link rows inserted.
    """
    # TODO(Person C):
    raise NotImplementedError


def fuzzy_match_entity(text: str, entity_ids: list[str]) -> list[tuple[str, int]]:
    """
    Return all entity IDs that fuzzy-match any substring of `text` above FUZZY_THRESHOLD.

    Args:
        text:       Source text to search (commit message, PR description, etc.)
        entity_ids: Candidate entity ID strings.

    Returns:
        List of (entity_id, score) tuples sorted by score descending.
    """
    # TODO(Person C): use rapidfuzz.fuzz.partial_ratio or token_set_ratio
    raise NotImplementedError
