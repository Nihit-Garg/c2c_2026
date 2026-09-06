"""
ingestion/jira_parser.py — Parses a Jira CSV export into ticket rows.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Read a CSV file exported from Jira (or a mock CSV in demo_data/)
and produce rows matching the `tickets` schema in CONTRACTS.md. No live Jira API
— static export only (see ARCHITECTURE.md decision).

Input:  demo_data/jira_export.csv
Output: calls db.models.upsert_ticket for each row parsed
"""

from __future__ import annotations
from pathlib import Path


# Expected CSV column names — update if export format changes
EXPECTED_COLUMNS = {"id", "title", "description", "status", "created_at"}


def parse_jira_csv(csv_path: str | Path) -> list[dict]:
    """
    Parse a Jira CSV export file and return ticket dicts.

    Args:
        csv_path: Path to the exported CSV file.

    Returns:
        List of ticket dicts matching the `tickets` schema:
        [{id, title, description, status, created_at}]
        id is expected to be in "JIRA-<number>" format per CONTRACTS.md.

    Raises:
        FileNotFoundError: if csv_path does not exist.
        ValueError:        if required columns are missing from the CSV.
    """
    # TODO(Person C): use csv.DictReader, validate columns, map rows to ticket dicts
    raise NotImplementedError


def normalize_ticket_id(raw_id: str) -> str:
    """
    Ensure the ticket ID follows the "JIRA-<number>" format from CONTRACTS.md.

    Args:
        raw_id: Raw ID string from the CSV (e.g. "4421", "PROJ-4421").

    Returns:
        Normalized ID string (e.g. "JIRA-4421").
    """
    # TODO(Person C): strip project prefix variants, re-add canonical "JIRA-" prefix
    raise NotImplementedError
