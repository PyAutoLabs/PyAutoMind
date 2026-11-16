# Brain board: keep a hygiene ledger and show its trend

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: after two board runs on different days the published `board.json` carries a non-empty `history` with one point per day per hygiene row; each hygiene row on the Brain board shows a sparkline; a test shows a run appends exactly one ledger line per day (idempotent on re-run)
Review-minutes: 10
Unattended: ready
Lane: any

Source: SIG-3 from the ecosystem review, **re-checked 2026-11-12 and holds** (during PyAutoHeart#338): `board/_board.py:647` sets `data["history"] = []`; `brain_board.yml` has `contents: read` and no commit step; Brain has no hygiene ledger file; the published `board.json` has `history: []` and 15 hygiene rows with counts that are never kept, though Brain Board has run 176 times since 2026-08-24. The SIG-2 half (unit-test trends on the Heart board) shipped in PyAutoHeart#338.

Change: an append-only hygiene ledger in Brain (one line per day: date, sha, each hygiene row's count), written by `brain_board.yml` (needs `contents: write` and a ledger-only commit step, or the Pulse/Heart pattern of a published sidecar if a commit is unwelcome — decide and say why); `_board.py` fills `history` from it and the board renders a sparkline per hygiene row.

<!-- filed 2026-11-12 by the programme lead session (split from PyAutoHeart#338) -->
