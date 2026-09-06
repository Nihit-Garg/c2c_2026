code-archaeology/
├── README.md
├── PROGRESS.md
├── ARCHITECTURE.md
├── CONTRACTS.md
├── .env.example
├── .gitignore
│
├── backend/
│   ├── requirements.txt
│   ├── main.py                          # FastAPI entrypoint
│   ├── config.py
│   │
│   ├── ingestion/                       # OWNER: Person C
│   │   ├── git_parser.py                # PyDriller/GitPython → commits, blame, diffs
│   │   ├── pr_parser.py                 # GitHub/GitLab API → PR threads
│   │   ├── jira_parser.py               # CSV export → tickets
│   │   ├── slack_parser.py              # Slack export JSON → messages
│   │   └── run_ingestion.py             # one-shot script, populates DB
│   │
│   ├── resolution/                      # OWNER: Person C
│   │   ├── entity_linker.py             # regex/fuzzy match: commit↔PR↔ticket↔slack
│   │   ├── line_tracker.py              # blame-through-renames for function history
│   │   └── graph_builder.py             # builds join tables / graph
│   │
│   ├── agents/                          # OWNER: Person B (core AI feature)
│   │   ├── retriever_agent.py           # pulls evidence for a queried entity
│   │   ├── synthesis_agent.py           # builds cited causal narrative
│   │   ├── orphan_detector_agent.py     # batch risk scoring
│   │   ├── contradiction_agent.py       # stretch: conflicting-sources flag
│   │   └── orchestrator.py              # sequential pipeline, no heavy framework
│   │
│   ├── api/                             # OWNER: Person A (auth/user + supporting APIs)
│   │   ├── routes_query.py              # POST /query
│   │   ├── routes_dashboard.py          # GET /orphans
│   │   ├── routes_entity.py             # GET /entity/{id}/timeline
│   │   └── routes_auth.py               # if needed at all — keep minimal/skip
│   │
│   ├── db/
│   │   ├── models.py                    # entities, commits, prs, tickets, slack_messages, links
│   │   ├── schema.sql
│   │   └── seed_demo_repo.py
│   │
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/
│   │   │   └── client.js                # matches CONTRACTS.md exactly
│   │   ├── mocks/
│   │   │   └── fixtures.json            # mocked responses so frontend never blocks on backend
│   │   ├── pages/
│   │   │   ├── QueryPage.jsx            # OWNER: Frontend Person 1
│   │   │   ├── AnswerPage.jsx           # OWNER: Frontend Person 1
│   │   │   ├── OrphanDashboard.jsx      # OWNER: Frontend Person 2
│   │   │   └── EntityTimeline.jsx       # OWNER: Frontend Person 2
│   │   └── components/
│   │       ├── EvidenceCard.jsx
│   │       ├── ConfidenceBadge.jsx
│   │       └── ContradictionCallout.jsx
│   └── tailwind.config.js
│
└── demo_data/
    ├── chosen_repo/                     # real messy OSS repo clone
    ├── jira_export.csv
    └── slack_export/