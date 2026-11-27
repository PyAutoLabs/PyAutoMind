# Shift workers inherit the previous shift's ledger and brief environment

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-27
Issued: 2026-11-27
Epic: autonomous-orchestrators
Consequence: judge
Witness: two shifts dispatched back to back from one watcher: every worker and close-out of the second shift sees `PYAUTO_SHIFT_LEDGER_DIR` and `PYAUTO_SHIFT_BRIEF` naming the second shift (checked from inside the spawned session, not only in `worker_env()`); a test fails on the base commit.
Review-minutes: 10
Unattended: never
Lane: local-dev

Seen in shift 2026-11-26-pm2 (PyAutoMind#610). Three of its workers had `PYAUTO_SHIFT_LEDGER_DIR` / `PYAUTO_SHIFT_BRIEF` pointing at earlier shifts. One Mind op, `set-header Verified` on the compound-prior prompt, was written to the 2026-11-26-pm ledger and is still stranded there. That task has since shipped (PyAutoFit#1810) and its prompt is in `complete/`, so nothing is lost. But a stranded op is a Mind write that silently never lands.

`worker_env()` (`agents/conductors/batch/_orchestrator.py`) does set `PYAUTO_SHIFT_LEDGER_DIR` from the current lease dir, so the stale value enters after it. **Hypothesis, not checked:** `claude --bg` starts the session through a long-lived background supervisor whose environment was captured when it first started, so the per-spawn env is ignored or partly ignored. If that holds, the fix is to pass the shift paths in the worker prompt (already templated: `ledger_dir`) and to have the Mind writer refuse an op whose ledger dir does not match the brief it names.

Also: move or drop the stranded op in the 2026-11-26-pm ledger once the cause is known.
