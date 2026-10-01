# Lensing catch-up: structured freshness and a safe manual action

Type: feature
Target: PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

@PyAutoMemory only. Follow-up to PyAutoBrain#434 (Brain PR #435 and website PR #22).

## Original user request (verbatim)

ok go

## Approved conversational scope

User asked whether there was a follow-up. Proposed applying the new structured fields to paper-ingestion freshness: last successful ingestion and expected interval, why attention is needed, the existing catch-up command and whether human judgement is needed. User's “ok go” authorizes this implementation. No new agent or automatic ingestion.

## Plan

1. Use the existing seven-day rule and lensing-specific evidence, avoiding a recent non-lensing activity masking lensing staleness.
2. Expose a structured workstream with last verified ingestion, last recorded reading activity, freshness reason, threshold, evidence links and the existing manual `/catch_up lensing` action.
3. Render Memory's HTML/Markdown banner and cockpit attention item from the same model; healthy work creates no attention noise, missing/invalid evidence remains unknown.
4. Verify boundary dates, provenance, scope isolation, uncertainty and feed compatibility; run Memory validation/tests and browser smoke.

## Detailed implementation

- `scripts/board.py`: collect `catch_up.ingest_evidence("lensing", root)` alongside legacy all-scope last_ingested; preserve legacy fields. Build a pure `lensing_catch_up` model against the snapshot's clock. Use the helper's existing cutoff semantics (latest scoped DONE or bib+sources ingestion); explicitly distinguish recorded activity from actual ingestion so DONE is not labelled last success. Publish cutoff, age, seven-day threshold, last_ingestion date/commit, last_read date, source links and canonical healthy/stale/unknown.
- `_catch_up_md`/`_catch_up_html` consume this model for a scoped and honestly worded banner; `to_state` publishes the model even when healthy, plus an optional attention item when stale/unknown using the newly shipped v1 id/state/reason/actions/recommended_action_id fields. Catch-up is a prompt handoff, safety scientific_judgement; link its actual skill/runbook. Do not invent a scientific decision before candidates are harvested; explain selection's human gate without fabricated decision text.
- Missing, malformed or future evidence is unknown, not fresh. Do not clamp future dates to age zero. Preserve existing all-scope fields for consumers. A top-level feed deadline is not appropriate to a single workstream among other Memory queues; publish its deadline in the workstream model instead.
- `tests/test_board.py`: cases at days 6/7/8, absent/bad/future dates, DONE versus actual ingest distinction, lensing vs interests, render/feed parity and action/evidence metadata. Validate against Brain's existing feed validator without changing the shared contract.
- Update the existing README board section with the structured workstream and freshness semantics. No science/wiki/bibliography writes, catch-up execution, new workflow scheduling, Brain changes or website changes.

Branch survey: Memory main clean, behind origin/main by 1; helper fetched current origin/main for the new isolated feature/memory-cockpit-catch-up worktree. No active claims. Mind isolated branch codex/memory-cockpit-catch-up.

Acceptance: a stale lensing cutoff yields one clear attention row with date, reason, seven-day threshold, evidence and manual action; recent activity in another domain cannot suppress it; healthy/unknown remain distinguishable without pixels.
