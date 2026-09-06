"""
db/schema.sql — Database schema, copied verbatim from CONTRACTS.md.

Run this once in the Supabase dashboard SQL editor to create all tables.
Do NOT modify without updating CONTRACTS.md first and notifying the team.

OWNER: Person A (backend/db/)
"""

-- Entities: code units we track (files, functions)
CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,          -- e.g. "src/invoice.py::parseInvoice"
  file_path TEXT NOT NULL,
  function_name TEXT,           -- NULL if entity is a whole file
  entity_type TEXT NOT NULL     -- 'function' | 'file'
);

-- Git commits
CREATE TABLE IF NOT EXISTS commits (
  sha TEXT PRIMARY KEY,
  author TEXT NOT NULL,
  author_email TEXT,
  timestamp TEXT NOT NULL,      -- ISO 8601
  message TEXT,
  diff_summary TEXT
);

-- Pull requests
CREATE TABLE IF NOT EXISTS prs (
  id TEXT PRIMARY KEY,          -- e.g. "gh-1234"
  title TEXT,
  description TEXT,
  author TEXT,
  merged_at TEXT,
  url TEXT
);

-- Jira tickets
CREATE TABLE IF NOT EXISTS tickets (
  id TEXT PRIMARY KEY,          -- e.g. "JIRA-1234"
  title TEXT,
  description TEXT,
  status TEXT,
  created_at TEXT
);

-- Slack messages
CREATE TABLE IF NOT EXISTS slack_messages (
  id TEXT PRIMARY KEY,
  channel TEXT,
  author TEXT,
  timestamp TEXT,
  text TEXT,
  thread_id TEXT
);

-- Links: entity ↔ evidence join table (the graph)
CREATE TABLE IF NOT EXISTS links (
  id BIGSERIAL PRIMARY KEY,
  entity_id TEXT REFERENCES entities(id),
  source_type TEXT NOT NULL,       -- 'commit' | 'pr' | 'ticket' | 'slack'
  source_id TEXT NOT NULL,         -- FK into the relevant table above
  relation TEXT                    -- 'introduced_by' | 'discussed_in' | 'resolves' | 'references'
);

-- Orphan risk scores (computed by orphan_detector_agent)
CREATE TABLE IF NOT EXISTS orphan_scores (
  entity_id TEXT PRIMARY KEY REFERENCES entities(id),
  risk_score REAL NOT NULL,        -- 0.0 - 1.0
  reason TEXT NOT NULL,            -- human-readable flag reason
  last_touched_by TEXT,
  last_touched_at TEXT,
  evidence_count INTEGER
);
