"""
resolution/line_tracker.py — Tracks function history through file renames and moves.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Given an entity (file + function), follow the git blame chain
across renames/moves using GitPython's follow-mode, so we don't lose provenance
when a file is renamed or moved. Produces a list of (sha, author, timestamp) for
every time the function was touched, even across renames.
"""

from __future__ import annotations
from pathlib import Path


def track_function_history(
    repo_path: str | Path,
    file_path: str,
    function_name: str,
) -> list[dict]:
    """
    Follow a function's full change history across file renames/moves.

    Args:
        repo_path:     Local path to the git repo.
        file_path:     Current relative file path (e.g. "src/billing/invoice.py").
        function_name: Function name (e.g. "parseInvoice").

    Returns:
        Chronologically sorted list of change events:
        [{sha, author, author_email, timestamp, message, old_file_path}]
        `old_file_path` is set if the file was renamed, else equals `file_path`.
    """
    # TODO(Person C): use git log --follow -p to trace renames
    # Identify the function's line range per commit using parse_functions_from_diff
    raise NotImplementedError


def resolve_renames(repo_path: str | Path, file_path: str) -> list[dict]:
    """
    Return the full rename chain for a file (most recent first).

    Args:
        repo_path: Local path to the git repo.
        file_path: Current relative file path.

    Returns:
        List of {old_path, new_path, sha, timestamp} rename events.
    """
    # TODO(Person C): git log --follow --diff-filter=R -- <file>
    raise NotImplementedError
