# PROGRESS.md
Update your own section at the end of every session, before switching device/account.

---

## Person A (API + DB + integration owner)
- Done:
  - `backend/main.py` — FastAPI app, CORS, lifespan startup validation, `/health` route
  - `backend/config.py` — full env var loading with `validate()` (Supabase + LLM check)
  - `backend/db/schema.sql` — verbatim from CONTRACTS.md, Postgres-ready (IF NOT EXISTS, BIGSERIAL)
  - `backend/db/models.py` — **REAL** Supabase implementation of all 12 DB functions (upsert, get, timeline, evidence, orphan scores)
  - `backend/db/seed_demo_repo.py` — **REAL** seeder: 3 entities, 5 commits, 2 PRs, 2 tickets, 5 Slack messages, 14 links, 3 orphan scores
  - `backend/api/routes_query.py` — Pydantic models + POST /query handler (delegates to orchestrator)
  - `backend/api/routes_dashboard.py` — GET /orphans handler
  - `backend/api/routes_entity.py` — GET /entity/{id}/timeline handler with :path param
  - `backend/requirements.txt` — all deps pinned (supabase==2.5.3, google-generativeai, etc.)
  - `.env.example`, `.gitignore`, `ARCHITECTURE.md` updated with Supabase/Gemini decisions
- In Progress:
  - ⏳ Waiting for `schema.sql` to be run in Supabase dashboard → then run seeder
- Next:
  - Run `pip install -r requirements.txt` and `uvicorn main:app --reload` → verify `/health` 200
  - Run `python -m db.seed_demo_repo` → verify all tables populated in Supabase
- Gotchas:
  - `.env` must have `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `GOOGLE_API_KEY` before startup
  - `schema.sql` must be run in Supabase dashboard BEFORE the seeder
  - `links` table delete is called at seed time to allow idempotent re-runs (safe in dev)

---

## Person B (Agents / core AI)
- Done:
  - `backend/agents/retriever_agent.py` — skeleton with correct signatures (Phase 3 target)
  - `backend/agents/synthesis_agent.py` — skeleton: LLM routing (Gemini/Ollama/Anthropic), confidence thresholds, system prompt
  - `backend/agents/orphan_detector_agent.py` — skeleton (Phase 6 target)
  - `backend/agents/contradiction_agent.py` — skeleton (Phase 5 stretch)
  - `backend/agents/orchestrator.py` — skeleton wiring all 3 pipeline steps
- In Progress: —
- Next (Phase 3):
  - Implement `retriever_agent.retrieve_evidence(entity_id)` — call `models.get_all_evidence_for_entity()`, map to CONTRACTS.md evidence shape
  - Implement `retriever_agent.resolve_entity_from_query(query)` — rapidfuzz against entity IDs
  - Implement `retriever_agent.build_evidence_context_string(evidence)` — LLM prompt formatter
- Next (Phase 4, after Phase 3 works):
  - Implement `synthesis_agent._call_gemini(prompt)` — real google-generativeai SDK call
  - Implement `synthesis_agent._call_ollama(prompt)` — ollama fallback
  - Implement `synthesis_agent.synthesize(...)` — full pipeline
- Gotchas:
  - GOOGLE_API_KEY must be in .env before synthesis agent can run
  - Test with seeded data first (Phase 2 must be done before Phase 3 can be verified)

---

## Person C (Ingestion + resolution)
- Done:
  - `backend/ingestion/git_parser.py` — skeleton (Phase 7 target)
  - `backend/ingestion/pr_parser.py` — skeleton
  - `backend/ingestion/jira_parser.py` — skeleton
  - `backend/ingestion/slack_parser.py` — skeleton
  - `backend/ingestion/run_ingestion.py` — CLI entrypoint skeleton
  - `backend/resolution/entity_linker.py` — skeleton with rapidfuzz imports
  - `backend/resolution/line_tracker.py` — skeleton
  - `backend/resolution/graph_builder.py` — skeleton with heuristic weights
  - `demo_data/chosen_repo/` — folder created (empty, needs repo clone)
  - `demo_data/slack_export/` — folder created (empty)
- In Progress: —
- Next (Phase 7 — starts after Phase 6 demo is working):
  - Pick demo OSS repo (suggest: `psf/requests` or `pallets/flask`) and clone to `demo_data/chosen_repo/`
  - Implement `git_parser.parse_repo(repo_path)` — PyDriller walk → upsert commits
  - Implement `git_parser.parse_functions_from_diff(diff, file_path)` — regex function extraction
  - Implement `entity_linker.link_commits_to_entities()` — fuzzy match commit messages
- Gotchas:
  - The seeder (Phase 2) already provides working data — Phase 7 adds real data on top
  - Links table delete-on-seed only clears the seeded links, real links can accumulate

---

## Frontend 1 (QueryPage, AnswerPage)
- Done: — (Frontend deferred, backend-first)
- In Progress: —
- Next: Build against `frontend/src/mocks/fixtures.json` once backend API is stable (after Phase 5)
- Gotchas: —

---

## Frontend 2 (OrphanDashboard, EntityTimeline)
- Done: — (Frontend deferred, backend-first)
- In Progress: —
- Next: Build against `fixtures.json` once `/orphans` and `/entity/{id}/timeline` are tested
- Gotchas: —

---

## Integration log (Person A fills after each merge)
- 2026-09-06: Scaffold complete — all backend files created with real implementations for Phase 1+2. Schema + seeder ready. Waiting for Supabase schema run + Gemini API key.

---

## Phase Status Tracker
| Phase | Status | Blocker |
|-------|--------|---------|
| 1 — FastAPI + Supabase live | ⏳ Ready to run | Need `schema.sql` in Supabase + `.env` keys |
| 2 — Seeder | ⏳ Ready to run | Needs Phase 1 done |
| 3 — Retriever agent | 🔲 Not started | Person B |
| 4 — Synthesis (Gemini) | 🔲 Not started | Person B, needs GOOGLE_API_KEY |
| 5 — /query end-to-end | 🔲 Not started | Person A + B |
| 6 — /orphans end-to-end | 🔲 Not started | Person A + B |
| 7 — Git ingestion | 🔲 Not started | Person C, needs demo repo chosen |
| 8 — Real orphan scoring | 🔲 Not started | Person B + C |
| 9 — PR/Jira/Slack ingestion | 🔲 Not started | Person C |