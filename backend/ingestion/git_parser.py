"""
ingestion/git_parser.py — Mines git history using PyDriller and GitPython.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Extract commits, diffs, blame, and function-level change history
from a local git repository clone. Output rows matching the `commits` and
`entities` table schemas in CONTRACTS.md.

Input:  path to a local git repo clone (demo_data/chosen_repo/)
Output: calls db.models.upsert_commit / upsert_entity for each discovered item
"""

from __future__ import annotations
from pathlib import Path


def parse_repo(repo_path: str | Path) -> dict:
    """
    Walk all commits in the repository and extract commit metadata, diffs,
    and modified file paths.

    Args:
        repo_path: Local path to the cloned git repository.

    Returns:
        A summary dict {"commits_inserted": int, "entities_discovered": int}

    Raises:
        FileNotFoundError: if repo_path does not exist or is not a git repo.
    """
    # TODO(Person C): use pydriller.Repository to iterate commits
    # For each commit: build commit dict, call db.models.upsert_commit
    # For each modified file: call parse_functions_from_diff to extract entities
    raise NotImplementedError


def parse_functions_from_diff(diff: str, file_path: str) -> list[dict]:
    """
    Extract function-level entities touched by a diff using regex heuristics.

    Args:
        diff:      Raw unified diff string for one file in one commit.
        file_path: Relative path of the file in the repo (e.g. "src/billing/invoice.py").

    Returns:
        List of entity dicts matching the `entities` schema:
        [{id, file_path, function_name, entity_type}]
    """
    # TODO(Person C): regex on "def <name>(" / "class <name>(" in diff context
    raise NotImplementedError


def run_blame(repo_path: str | Path, file_path: str, line_number: int) -> dict:
    """
    Return the commit that last modified a specific line.

    Args:
        repo_path:   Local path to the repo.
        file_path:   Relative path of the file.
        line_number: 1-indexed line number.

    Returns:
        dict with {sha, author, timestamp, message}
    """
    # TODO(Person C): use git blame via GitPython repo.blame()
    raise NotImplementedError
