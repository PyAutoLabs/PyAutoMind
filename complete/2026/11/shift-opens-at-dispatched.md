- epic: autonomous-orchestrators (pilot 4c follow-up; issue PyAutoBrain#589)
- summary: PyAutoBrain#590. `_orchestrator.brief_open` treats a brief before its `dispatched:` as not yet open: the tick is idle ("not yet open: opens at dispatched …") and creates or touches nothing, so a brief may be landed early. `batch watch` says "not yet open — opens in …". Batch AGENTS.md documents the window `dispatched:` → `review-at:`. This narrows the watcher; no doctrine change.
- trigger: pilot shadow shift 1 opened on landing (2026-11-04 13:17Z), a day before its dispatched: (2026-11-05T09:00Z). Required before the first live shift.
- witness: PASS. New watcher test (idle before dispatched, no slot created; plans at dispatched) with a control (fails with `_orchestrator.py` reverted); watch header test; Brain 1575 passed; tenant firewall OK.
- heart: STALE (8 h old; Array/Galaxy/Lens monitoring red) acknowledged by the human at ship; glance tier, in-turn merge.

## Original prompt

# A shift opens at `dispatched:`, not when its brief lands

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-11-05
Issued: 2026-11-05
Epic: autonomous-orchestrators
Consequence: glance
Witness: a watcher tick before a brief's `dispatched:` is idle with "not yet open" and creates no slot directory; the first tick at or after `dispatched:` plans as before; `batch watch` shows "opens in"; the full Brain suite passes
Review-minutes: 5
Unattended: never
Lane: local-dev

Found in pilot shadow shift 1 (PyAutoBrain#574): the watcher opened brief 2026-11-05-am on landing (2026-11-04 13:17Z), not at its `dispatched:` (2026-11-05T09:00Z). Must be fixed before the first live shift. Human approved starting it on 2026-11-05 ("yes").

<!-- filed by hand 2026-11-05; headers mirror intake's -->
