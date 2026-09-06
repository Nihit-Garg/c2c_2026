"""
db/seed_demo_repo.py — Populates Supabase with realistic demo data for judging.

OWNER: Person A (backend/db/)
RESPONSIBILITY: One-shot seeder script. Run after schema.sql has been applied
in Supabase. Inserts fake-but-realistic commits, PRs, tickets, Slack messages,
entities, links, and orphan scores so the full UI demo works without real ingestion.

Run with:
    cd backend && python -m db.seed_demo_repo
"""

import sys
import os

# Make sure backend/ is on the path when run as __main__
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import models


# ── Demo entities ──────────────────────────────────────────────────────────────
DEMO_ENTITIES = [
    {
        "id": "src/billing/invoice.py::parseInvoice",
        "file_path": "src/billing/invoice.py",
        "function_name": "parseInvoice",
        "entity_type": "function",
    },
    {
        "id": "src/billing/invoice.py::applyLegacyDiscount",
        "file_path": "src/billing/invoice.py",
        "function_name": "applyLegacyDiscount",
        "entity_type": "function",
    },
    {
        "id": "src/auth/session.py",
        "file_path": "src/auth/session.py",
        "function_name": None,
        "entity_type": "file",
    },
]

# ── Demo commits ───────────────────────────────────────────────────────────────
DEMO_COMMITS = [
    {
        "sha": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "author": "Alice Nguyen",
        "author_email": "alice@example.com",
        "timestamp": "2022-03-15T09:14:00Z",
        "message": "feat: add parseInvoice to handle EU VAT edge cases (JIRA-4421)",
        "diff_summary": "+parseInvoice function, +47 lines in src/billing/invoice.py",
    },
    {
        "sha": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "author": "Marcus Webb",
        "author_email": "marcus@example.com",
        "timestamp": "2022-07-22T14:30:00Z",
        "message": "fix: applyLegacyDiscount must run before tax rounding (hotfix) - gh-1501",
        "diff_summary": "Modified order of operations in applyLegacyDiscount, -3+8 lines",
    },
    {
        "sha": "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
        "author": "Priya Kapoor",
        "author_email": "priya@example.com",
        "timestamp": "2023-01-09T11:05:00Z",
        "message": "chore: no-op refactor session.py, no logic change",
        "diff_summary": "Renamed variables for PEP8 compliance in src/auth/session.py",
    },
    {
        "sha": "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5",
        "author": "Alice Nguyen",
        "author_email": "alice@example.com",
        "timestamp": "2022-03-10T16:00:00Z",
        "message": "spike: rough prototype of EU VAT locale switching (WIP, see JIRA-4421)",
        "diff_summary": "Added draft parseInvoice skeleton, not wired up yet",
    },
    {
        "sha": "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6",
        "author": "Jordan Lee",
        "author_email": "jordan@example.com",
        "timestamp": "2021-11-03T10:00:00Z",
        "message": "init: add session.py for token-based auth",
        "diff_summary": "Created src/auth/session.py with double-validation loop for replay attack protection",
    },
]

# ── Demo PRs ───────────────────────────────────────────────────────────────────
DEMO_PRS = [
    {
        "id": "gh-1234",
        "title": "EU VAT compliance: parseInvoice overhaul",
        "description": (
            "Implements JIRA-4421. parseInvoice was hardcoded for US-only tax codes. "
            "This PR adds locale-aware parsing. cc @alice @marcus. "
            "Note: applyLegacyDiscount must NOT be removed — it handles pre-2020 contracts "
            "that finance still bills manually."
        ),
        "author": "Alice Nguyen",
        "merged_at": "2022-03-16T17:00:00Z",
        "url": "https://github.com/example/repo/pull/1234",
    },
    {
        "id": "gh-1501",
        "title": "Hotfix: discount ordering bug causes off-by-one on invoices >$10k",
        "description": (
            "Fixes silent bug found by QA. applyLegacyDiscount was being called after "
            "tax rounding, causing $0.01 discrepancies that accounting flagged. "
            "See Slack thread in #billing-eng from 2022-07-21."
        ),
        "author": "Marcus Webb",
        "merged_at": "2022-07-22T15:45:00Z",
        "url": "https://github.com/example/repo/pull/1501",
    },
]

# ── Demo tickets ───────────────────────────────────────────────────────────────
DEMO_TICKETS = [
    {
        "id": "JIRA-4421",
        "title": "EU VAT compliance for invoice generation",
        "description": (
            "Finance reports that EU customer invoices are being generated with incorrect VAT "
            "(20% applied flat instead of country-specific rates). parseInvoice needs to be "
            "locale-aware. Priority: P1."
        ),
        "status": "Done",
        "created_at": "2022-03-10T08:00:00Z",
    },
    {
        "id": "JIRA-5003",
        "title": "Remove legacy discount code path",
        "description": (
            "applyLegacyDiscount was supposed to be removed after Q4 2022 migration, "
            "but finance confirmed on 2023-02-01 that pre-2020 contracts are still active. "
            "Ticket CLOSED — do not remove."
        ),
        "status": "Closed (Won't Fix)",
        "created_at": "2022-12-01T09:00:00Z",
    },
]

# ── Demo Slack messages ────────────────────────────────────────────────────────
DEMO_SLACK_MESSAGES = [
    {
        "id": "billing-eng-S001",
        "channel": "#billing-eng",
        "author": "Marcus Webb",
        "timestamp": "2022-07-21T16:45:00Z",
        "text": "Hey @alice, found a nasty bug — applyLegacyDiscount runs AFTER tax rounding in the prod path. Any reason that was intentional? Invoices over $10k are off by a cent.",
        "thread_id": "billing-eng-S001",
    },
    {
        "id": "billing-eng-S002",
        "channel": "#billing-eng",
        "author": "Alice Nguyen",
        "timestamp": "2022-07-21T17:02:00Z",
        "text": "Oh no, that's my fault from the VAT PR. The ordering was intentional on staging but I didn't account for the rounding path in prod. Hot-fix ASAP — but DO NOT remove applyLegacyDiscount itself, finance still uses it for legacy contracts.",
        "thread_id": "billing-eng-S001",
    },
    {
        "id": "eng-all-S003",
        "channel": "#eng-all",
        "author": "Jordan Lee",
        "timestamp": "2023-06-15T10:00:00Z",
        "text": "Does anyone know why session.py has that weird double-validation loop? Original author is gone and no PR explains it.",
        "thread_id": "eng-all-S003",
    },
    {
        "id": "billing-eng-S004",
        "channel": "#billing-eng",
        "author": "Alice Nguyen",
        "timestamp": "2022-03-09T14:30:00Z",
        "text": "Starting work on JIRA-4421 today. The parseInvoice function doesn't exist yet — need to build it from scratch. The old invoiceParser() was a mess.",
        "thread_id": "billing-eng-S004",
    },
    {
        "id": "billing-eng-S005",
        "channel": "#billing-eng",
        "author": "Marcus Webb",
        "timestamp": "2023-03-01T09:00:00Z",
        "text": "FYI — applyLegacyDiscount is still active for about 200 enterprise accounts on pre-2020 contracts. Finance said we can't migrate them until Q3 at earliest. Do not deprecate.",
        "thread_id": "billing-eng-S005",
    },
]


# ── Link associations: entity ↔ evidence ───────────────────────────────────────
DEMO_LINKS = [
    # parseInvoice ↔ all its evidence
    ("src/billing/invoice.py::parseInvoice", "commit", "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2", "introduced_by"),
    ("src/billing/invoice.py::parseInvoice", "commit", "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5", "references"),
    ("src/billing/invoice.py::parseInvoice", "pr",     "gh-1234",    "introduced_by"),
    ("src/billing/invoice.py::parseInvoice", "ticket", "JIRA-4421",  "resolves"),
    ("src/billing/invoice.py::parseInvoice", "slack",  "billing-eng-S004", "discussed_in"),

    # applyLegacyDiscount ↔ all its evidence
    ("src/billing/invoice.py::applyLegacyDiscount", "commit", "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3", "references"),
    ("src/billing/invoice.py::applyLegacyDiscount", "pr",     "gh-1501",    "discussed_in"),
    ("src/billing/invoice.py::applyLegacyDiscount", "ticket", "JIRA-5003",  "references"),
    ("src/billing/invoice.py::applyLegacyDiscount", "slack",  "billing-eng-S001", "discussed_in"),
    ("src/billing/invoice.py::applyLegacyDiscount", "slack",  "billing-eng-S002", "discussed_in"),
    ("src/billing/invoice.py::applyLegacyDiscount", "slack",  "billing-eng-S005", "discussed_in"),

    # session.py ↔ minimal evidence (this is the orphan!)
    ("src/auth/session.py", "commit", "c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "references"),
    ("src/auth/session.py", "commit", "e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6", "introduced_by"),
    ("src/auth/session.py", "slack",  "eng-all-S003", "discussed_in"),
]

# ── Orphan scores (pre-computed for demo) ─────────────────────────────────────
DEMO_ORPHAN_SCORES = [
    {
        "entity_id": "src/auth/session.py",
        "risk_score": 0.85,
        "reason": "Bus factor 1 (Jordan Lee, departed 2023-07-01). No PR or ticket evidence. Only 1 Slack mention expressing confusion about the double-validation loop.",
        "last_touched_by": "Priya Kapoor",
        "last_touched_at": "2023-01-09T11:05:00Z",
        "evidence_count": 3,
    },
    {
        "entity_id": "src/billing/invoice.py::applyLegacyDiscount",
        "risk_score": 0.42,
        "reason": "Function kept alive by pre-2020 finance contracts — context only exists in Slack (not in code or ticket). If those Slack messages are lost, the reason for keeping this is gone.",
        "last_touched_by": "Marcus Webb",
        "last_touched_at": "2022-07-22T14:30:00Z",
        "evidence_count": 6,
    },
    {
        "entity_id": "src/billing/invoice.py::parseInvoice",
        "risk_score": 0.10,
        "reason": "Well-documented: JIRA-4421, PR gh-1234, multiple Slack threads, and clear commit messages all explain the EU VAT origin.",
        "last_touched_by": "Alice Nguyen",
        "last_touched_at": "2022-03-16T17:00:00Z",
        "evidence_count": 5,
    },
]


def seed() -> None:
    """
    Insert all demo data into Supabase. Idempotent — upsert everywhere.
    Run after applying schema.sql in Supabase dashboard.
    """
    print("🌱 Seeding demo data into Supabase...")

    print("  → Upserting entities...")
    for entity in DEMO_ENTITIES:
        models.upsert_entity(entity)
    print(f"     ✅ {len(DEMO_ENTITIES)} entities")

    print("  → Upserting commits...")
    for commit in DEMO_COMMITS:
        models.upsert_commit(commit)
    print(f"     ✅ {len(DEMO_COMMITS)} commits")

    print("  → Upserting PRs...")
    for pr in DEMO_PRS:
        models.upsert_pr(pr)
    print(f"     ✅ {len(DEMO_PRS)} PRs")

    print("  → Upserting tickets...")
    for ticket in DEMO_TICKETS:
        models.upsert_ticket(ticket)
    print(f"     ✅ {len(DEMO_TICKETS)} tickets")

    print("  → Upserting Slack messages...")
    for msg in DEMO_SLACK_MESSAGES:
        models.upsert_slack_message(msg)
    print(f"     ✅ {len(DEMO_SLACK_MESSAGES)} Slack messages")

    print("  → Inserting entity links (graph edges)...")
    # Note: links table has AUTOINCREMENT so we use insert, not upsert
    # Check for duplicates by clearing first in dev
    client = models.get_client()
    client.table("links").delete().neq("id", 0).execute()   # clear links (idempotent re-run)
    for entity_id, source_type, source_id, relation in DEMO_LINKS:
        models.insert_link(entity_id, source_type, source_id, relation)
    print(f"     ✅ {len(DEMO_LINKS)} links")

    print("  → Upserting orphan scores...")
    for score in DEMO_ORPHAN_SCORES:
        models.upsert_orphan_score(score)
    print(f"     ✅ {len(DEMO_ORPHAN_SCORES)} orphan scores")

    print("\n✅ Demo seed complete! All tables populated.")
    print("   You can now test:")
    print("   curl http://localhost:8000/orphans")
    print("   curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' \\")
    print("     -d '{\"query\": \"why does parseInvoice exist\", \"entity_id\": \"src/billing/invoice.py::parseInvoice\"}'")


if __name__ == "__main__":
    seed()
