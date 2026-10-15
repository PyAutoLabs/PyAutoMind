- summary: Phase 1 of the human-approved Cortex Projects redesign (#521). Brain's Cortex conductor (`agents/conductors/cortex/_cortex.py` `_card_html`/`_card_md`) renders each project as a collapsed card (name, short purpose, running/open counts, newest ledger date) that opens to status/partition/issue, the ledger's current position, the unchanged resume chip, an aligned runs table (job, state pill, partition, date, clipped description with full-text disclosure; rows stack with labels below 34rem), a collapsed recent log and collapsed locations; the markdown page mirrors it with `<details>` folds. Every field comes from the parsed ledger; resume/check-in payloads, the counts table `collect_cortex` parses, the Summary table, `state.json` and freshness/drift semantics are unchanged. Ledger prose inside folds is entity-escaped. Tests extended (1269 Brain tests pass). Validated at 390px and 1280px on a scratch render of the real ledgers. PyAutoBrain#526 merged 2026-10-15 by human /prm under the recorded Heart RED development override (tier undeclared). No Cortex PR: PyAutoCortex was claimed by ral-category-paths-phase2 and its pages self-heal from Brain main via Cortex's Dashboard Refresh (nightly 03:35 UTC or next Cortex push).
- follow-up: phase 2 output accounting stays in `draft/feature/cortex/output_summary.md`; four pre-existing ruff errors in the touched files (same on main; CI runs no ruff) left as found.

## Original prompt

# Cortex Projects readability — phase 1

Targets: @PyAutoBrain @PyAutoCortex
Type: feature
Issued: 2026-10-14
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/521

Parent request and verbatim user text: draft/feature/cortex/human_readable_projects_dashboard.md.

Implement the parent's presentation plan: collapsed project disclosures, compact overview, structured runs with full details, collapsed history and locations, preserved resume actions and source meaning. Update _card_html/_card_md in Brain's Cortex conductor, relevant tests, and generated Cortex pages. Follow shared board standards. Do not require output metrics for this phase. Validate keyboard/mobile access, escaping and renderer drift. Plan approved in session. Await resolution of Brain's search-ext-a4-companions and Cortex's search-ext-b5a-wave2 claims before worktree setup.

Tier: undeclared — merge mode: human /prm
