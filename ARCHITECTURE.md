# ARCHITECTURE.md
Records WHY, not what. Code/CONTRACTS.md already show what.

## Decisions made so far

- **SQLite over Neo4j/Postgres** *(original rationale)*: no ops overhead, judges don't see
  the DB layer, join tables are enough for demo-scale graph queries.
- **OVERRIDE — Supabase (Postgres) instead of SQLite** *(decided 2026-09-06)*: team
  already has a Supabase project; the free tier gives us a hosted DB accessible
  across devices without passing around a .db file. `supabase-py` client SDK is
  used — no raw psycopg2 dependency. `schema.sql` is run once via the Supabase
  dashboard SQL editor. The `db/models.py` layer wraps the SDK for testability.
- **Sequential Python calls over CrewAI/AutoGen**: the "multi-agent" pipeline is
  really retrieve → synthesize → verify. A framework adds config/debugging
  overhead with no visible benefit at this scale.
- **Google Gemini (AI Studio) as primary LLM, Ollama as local fallback** *(decided 2026-09-06)*:
  Gemini free tier via `google-generativeai` SDK avoids rate-limit cost during the
  hackathon sprint. Ollama (`mistral` or `llama3`) runs locally for offline/fallback
  so the demo never hard-fails. Model is selected by env var `LLM_PROVIDER`
  (`gemini` | `ollama`).
- **Slack/Jira via static export, not live API**: OAuth setup burns hours for
  zero demo value; live calls also risk failing mid-demo.
- **Citation-required prompting**: every synthesis agent output must attach a
  source ID per claim; "no evidence found" is a valid and preferred answer over
  a fabricated one — hallucination during a live demo is the single biggest
  credibility risk for this project.
- **Orphan scoring is rule-based + LLM hybrid, not pure LLM**: cheaper, faster,
  and judges trust a visible heuristic (bus factor, evidence density, fan-in)
  more than an opaque LLM judgment call.

## Open decisions (fill in as made)
- Which demo repo? —
- Confidence scoring thresholds (what evidence count = high/medium/low)? —
- How do we simulate "departed engineer" without real HR data? (proposal: treat
  any author with zero commits in last N days of repo history as "departed")