"""
ingestion/run_ingestion.py — One-shot ingestion orchestrator script.

OWNER: Person C (backend/ingestion/, backend/resolution/)
RESPONSIBILITY: Calls all parsers in the correct order and populates the Supabase
DB from scratch. Designed to be run once before a demo. Idempotent (all writes use
upsert). Progress is printed to stdout.

Run with:
    python -m ingestion.run_ingestion \
        --repo demo_data/chosen_repo \
        --slack demo_data/slack_export \
        --jira demo_data/jira_export.csv
"""

from __future__ import annotations
import argparse
from pathlib import Path

from ingestion import git_parser, pr_parser, jira_parser, slack_parser
from resolution import entity_linker, graph_builder
from db import models


def run(repo_path: Path, slack_dir: Path, jira_csv: Path) -> None:
    """
    Full ingestion pipeline:
    1. Parse git commits and entities
    2. Fetch PRs from GitHub (or skip if no GITHUB_TOKEN)
    3. Parse Jira CSV
    4. Parse Slack export
    5. Run entity linker to build links table
    6. Build graph (orphan scores etc.)

    Args:
        repo_path: Path to the local git repo clone.
        slack_dir: Path to the Slack export folder.
        jira_csv:  Path to the Jira CSV export file.
    """
    # TODO(Person C): implement step by step, print progress after each phase
    raise NotImplementedError


def main() -> None:
    """CLI entrypoint — parse args and call run()."""
    parser = argparse.ArgumentParser(description="Run full Code Archaeology ingestion pipeline")
    parser.add_argument("--repo", required=True, help="Path to local git repo clone")
    parser.add_argument("--slack", required=True, help="Path to Slack export folder")
    parser.add_argument("--jira", required=True, help="Path to Jira CSV export")
    args = parser.parse_args()

    run(
        repo_path=Path(args.repo),
        slack_dir=Path(args.slack),
        jira_csv=Path(args.jira),
    )


if __name__ == "__main__":
    main()
