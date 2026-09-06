# CONTRACTS.md — Source of Truth
Do not deviate from this without updating this file first and notifying the team.

## Folder Ownership (exclusive — do not edit outside your own folder)
- Person A: backend/api/, backend/db/, integration owner (merges to `dev` every 45-90 min)
- Person B: backend/agents/ (retriever, synthesis, orphan detector, orchestrator)
- Person C: backend/ingestion/, backend/resolution/
- Frontend 1: frontend/src/pages/QueryPage.jsx, AnswerPage.jsx
- Frontend 2: frontend/src/pages/OrphanDashboard.jsx, EntityTimeline.jsx

## DB Schema (SQLite for hackathon; Postgres-compatible SQL)

```sql
CREATE TABLE entities (
  id TEXT PRIMARY KEY,          -- e.g. "src/invoice.py::parseInvoice"
  file_path TEXT NOT NULL,
  function_name TEXT,           -- NULL if entity is a whole file
  entity_type TEXT NOT NULL     -- 'function' | 'file'
);

CREATE TABLE commits (
  sha TEXT PRIMARY KEY,
  author TEXT NOT NULL,
  author_email TEXT,
  timestamp TEXT NOT NULL,      -- ISO 8601
  message TEXT,
  diff_summary TEXT
);

CREATE TABLE prs (
  id TEXT PRIMARY KEY,          -- e.g. "gh-1234"
  title TEXT,
  description TEXT,
  author TEXT,
  merged_at TEXT,
  url TEXT
);

CREATE TABLE tickets (
  id TEXT PRIMARY KEY,          -- e.g. "JIRA-1234"
  title TEXT,
  description TEXT,
  status TEXT,
  created_at TEXT
);

CREATE TABLE slack_messages (
  id TEXT PRIMARY KEY,
  channel TEXT,
  author TEXT,
  timestamp TEXT,
  text TEXT,
  thread_id TEXT
);

CREATE TABLE links (               -- the graph, as a join table
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_id TEXT REFERENCES entities(id),
  source_type TEXT NOT NULL,       -- 'commit' | 'pr' | 'ticket' | 'slack'
  source_id TEXT NOT NULL,         -- FK into the relevant table above
  relation TEXT                    -- 'introduced_by' | 'discussed_in' | 'resolves' | 'references'
);

CREATE TABLE orphan_scores (
  entity_id TEXT PRIMARY KEY REFERENCES entities(id),
  risk_score REAL NOT NULL,        -- 0.0 - 1.0
  reason TEXT NOT NULL,            -- human-readable flag reason
  last_touched_by TEXT,
  last_touched_at TEXT,
  evidence_count INTEGER
);
```

## API Routes (FastAPI, base URL `http://localhost:8000`)

### POST /query
Request:
```json
{ "query": "why is parseInvoice written this way", "entity_id": "src/invoice.py::parseInvoice" }
```
`entity_id` optional — if omitted, backend resolves it from free text.

Response:
```json
{
  "answer": "string — the causal narrative",
  "confidence": "high | medium | low",
  "evidence": [
    {
      "source_type": "commit | pr | ticket | slack",
      "source_id": "string",
      "snippet": "string",
      "author": "string",
      "timestamp": "ISO 8601",
      "url": "string or null"
    }
  ],
  "contradictions": [
    { "claim_a": "string", "source_a": "string", "claim_b": "string", "source_b": "string" }
  ]
}
```
If no evidence found: `"answer": "No historical evidence found.", "confidence": "low", "evidence": []`

### GET /orphans
Response:
```json
{
  "entities": [
    {
      "entity_id": "string",
      "risk_score": 0.0,
      "reason": "string",
      "last_touched_by": "string",
      "last_touched_at": "ISO 8601",
      "evidence_count": 0
    }
  ]
}
```
Sorted by `risk_score` descending.

### GET /entity/{entity_id}/timeline
Response:
```json
{
  "entity_id": "string",
  "events": [
    { "type": "commit | pr | ticket | slack", "id": "string", "timestamp": "ISO 8601", "summary": "string", "author": "string" }
  ]
}
```
Sorted chronologically ascending.

## Frontend API client contract
`frontend/src/api/client.js` must expose exactly:
```js
export async function queryEntity(query, entityId)   // -> POST /query
export async function getOrphans()                     // -> GET /orphans
export async function getTimeline(entityId)             // -> GET /entity/{id}/timeline
```
`frontend/src/mocks/fixtures.json` must contain sample responses matching the shapes above, keyed by route name, so Frontend 1/2 never block on backend.

## Naming/schema freeze
Anyone changing a table column, route shape, or the entity_id format MUST update this file in the same commit and post in team channel. No silent breaking changes.