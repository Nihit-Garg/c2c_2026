"""
ingestion/slack_parser.py — Parses a Slack workspace export (JSON files).

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Read the folder structure of a Slack export (one JSON file per
channel per day) and produce rows matching the `slack_messages` schema in
CONTRACTS.md. No live Slack API — static export only (see ARCHITECTURE.md).

Input:  demo_data/slack_export/  (folder containing <channel>/<YYYY-MM-DD>.json files)
Output: calls db.models.upsert_slack_message for each message
"""

from __future__ import annotations
from pathlib import Path


def parse_slack_export(export_dir: str | Path) -> list[dict]:
    """
    Walk a Slack export directory and return all messages as a flat list.

    Args:
        export_dir: Path to the Slack export root folder.

    Returns:
        List of message dicts matching the `slack_messages` schema:
        [{id, channel, author, timestamp, text, thread_id}]
        - id: "<channel>-<ts>" composite key (unique enough for demo scale)
        - timestamp: ISO 8601 (converted from Slack's Unix float timestamp)
        - thread_id: Slack's thread_ts if present, else None

    Raises:
        FileNotFoundError: if export_dir does not exist.
    """
    # TODO(Person C): os.walk export_dir, load each .json file with json.load,
    # iterate messages, map to slack_messages schema, collect and return all
    raise NotImplementedError


def slack_ts_to_iso(slack_ts: str | float) -> str:
    """
    Convert Slack's "1689123456.789012" Unix timestamp to ISO 8601 string.

    Args:
        slack_ts: Slack timestamp (string or float).

    Returns:
        ISO 8601 string, e.g. "2023-07-12T08:57:36Z".
    """
    # TODO(Person C): datetime.utcfromtimestamp(float(slack_ts)).isoformat() + "Z"
    raise NotImplementedError
