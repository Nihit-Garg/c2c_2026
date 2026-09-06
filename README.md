# Code Archaeology

A multi-agent system that reconstructs the institutional memory behind legacy code.
Instead of explaining *what* code does, it explains *why* it exists — mining git
history, PR discussions, Jira tickets, and Slack archives to reconstruct the
decisions, constraints, and trade-offs behind a given function or file.

It also proactively flags **orphaned knowledge**: critical logic whose reasoning
lives only in scattered historical discussion, or was understood primarily by
engineers no longer on the project.

## Why this exists

Codebases outlive the people who understood them. Tools like Copilot explain code
by reading the code itself — they can't tell you a workaround exists because of a
production incident three years ago that's only documented in a Slack thread and
a since-closed Jira ticket. This project correlates code with that scattered
historical record and surfaces it as a searchable, cited, risk-scored asset.

## What it does

- **Ask why**: query a function/file/decision, get a historical narrative answer
  with confidence level and every claim cited back to its source (commit, PR,
  ticket, or Slack message)
- **Orphan detection**: a ranked dashboard of code that's high-risk to maintain —
  undocumented, rarely touched, or last understood by someone no longer involved
- **Evidence trail**: every answer is fully inspectable — click into the actual
  commit diff, PR comment, or Slack message it was built from
- **No hallucinated history**: if no evidence exists, the system says so rather
  than fabricating a plausible-sounding reason

## Architecture

- **Ingestion**: parses git history, GitHub/GitLab PR threads, Jira CSV exports,
  and Slack JSON exports into a unified timeline
- **Entity resolution**: links commits, PRs, tickets, and Slack messages to the
  specific code entities (functions/files) they relate to
- **Multi-agent pipeline**: retriever agent pulls evidence → synthesis agent
  builds a cited narrative → orphan-detector agent runs batch risk scoring
- **Storage**: SQLite/Postgres relational schema (see `backend/db/schema.sql`)
- **Frontend**: React + Tailwind — query interface, answer view with evidence
  trail, and orphaned-knowledge dashboard

See `ARCHITECTURE.md` for the reasoning behind these choices.

## Project structure

See repo tree in `CONTRACTS.md` / project docs — key folders:
- `backend/ingestion/` — data extraction from git/PR/Jira/Slack
- `backend/resolution/` — links raw data to code entities
- `backend/agents/` — the AI pipeline (retrieve, synthesize, detect orphans)
- `backend/api/` — FastAPI routes
- `frontend/src/pages/` — Query, Answer, Orphan Dashboard, Entity Timeline

## Running locally

\`\`\`bash
# Backend
cd backend
pip install -r requirements.txt
python db/seed_demo_repo.py      # one-time ingestion of demo repo + exports
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
\`\`\`

## Demo data

This runs against a pre-ingested snapshot of a real open-source repository plus
its linked issue tracker and (synthetic, GDPR-safe) Slack export — no live API
calls happen during the demo.

## Team

Built at [hackathon name] by a team of 5 — 2 frontend, 3 backend/AI.