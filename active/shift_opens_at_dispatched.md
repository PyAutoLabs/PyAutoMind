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
