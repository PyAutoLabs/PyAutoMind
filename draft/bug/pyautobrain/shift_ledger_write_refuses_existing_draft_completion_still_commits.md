# A shift worker's edit to an existing Mind file is set aside, but its completion record still commits

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-16
Epic: autonomous-orchestrators
Consequence: notify
Lane: any

Seen in shift 2026-11-16-pm (18:21Z). Worker `dashboard_titles_two_drafts_by_their_filed_line` shipped as Mind ledger ops. Its three `op: write` edits to existing drafts were set aside ("write: <path> already exists", ledger `set_aside/`), raised as three NEEDS YOU lines, but its `complete/2026/11/dashboard-titles-filed-line.md` write committed. So Mind recorded the task shipped while the drafts were unchanged. The human applied the set-aside text by hand (cockpit, 2026-11-16).

1. Give the Mind writer an op that edits an existing file (a replace with an expected-base check, so it cannot clobber a concurrent change), and have the worker contract use it for edits; keep `write` create-only.
2. Make a worker's ledger ops land together: if any op is set aside, hold back its completion record (or mark the task not shipped) instead of committing it alone.
3. One NEEDS YOU line per worker for set-aside ops, naming the task, not one per file.
