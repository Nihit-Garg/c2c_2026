"""
ingestion/pr_parser.py — Fetches PR threads from GitHub REST API.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Pull PR metadata and review comments for a configured repo using
GITHUB_TOKEN. Output rows matching the `prs` schema in CONTRACTS.md.

Auth:    GITHUB_TOKEN from config (read-only, public repo access)
Output:  calls db.models.upsert_pr for each PR fetched
"""

from __future__ import annotations
from config import settings


def fetch_all_prs(repo: str | None = None) -> list[dict]:
    """
    Fetch all merged PRs from the configured GitHub repository.

    Args:
        repo: "owner/repo" string. Defaults to settings.GITHUB_REPO.

    Returns:
        List of PR dicts matching the `prs` schema:
        [{id, title, description, author, merged_at, url}]
        id is formatted as "gh-<number>" per CONTRACTS.md.

    Raises:
        ValueError:   if no GITHUB_TOKEN or repo is configured.
        RuntimeError: on non-200 GitHub API response.
    """
    # TODO(Person C): GET https://api.github.com/repos/{repo}/pulls?state=closed&per_page=100
    # paginate, filter merged_at is not None, map to PR dict shape
    raise NotImplementedError


def fetch_pr_comments(pr_number: int, repo: str | None = None) -> list[str]:
    """
    Fetch all review comments for a specific PR, concatenated as a single
    discussion thread string for use in entity linking.

    Args:
        pr_number: GitHub PR number (integer).
        repo:      "owner/repo" string. Defaults to settings.GITHUB_REPO.

    Returns:
        List of comment body strings in chronological order.
    """
    # TODO(Person C): GET /repos/{repo}/pulls/{pr_number}/comments
    raise NotImplementedError
