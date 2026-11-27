Merged PyAutoBrain#725 (human /prm, 2026-11-27).

Shift worker, update and close-out sessions now get their shift variables through `claude --settings '{"env":{…}}'`. Those variables are the worker flag, ledger dir, this shift's brief, the Mind-commit hooks lock (appended after the caller's `GIT_CONFIG_*`) and the kick file. A guard refuses a ledger dir whose slot differs from `PYAUTO_SHIFT_BRIEF`'s slot. It lives in `_mind_writer.shift_ledger_dir` for the Python readers and in `_worktree_release_queued` in shell, which fails closed.

Root cause, proven live 2026-11-27: `claude --bg` runs sessions on daemon "spare" processes that keep the daemon-starter's env. A probe launched with `PYAUTO_PROBE=two` on a claimed spare printed `one`, but did receive a `--settings` env value.

Witness PASS on the branch: a claimed spare with a stale process env plus the branch's `settings_args()` printed the new shift's ledger, brief, `WORKER=1` and hooks path. The control without `--settings` printed the stale values. Full suite 2560 passed. Independent Opus review returned FINDINGS (minor): 4 fixed, 1 kept as intended. Heart dev-ship GREEN. CI was RED once, on the tenant firewall (a test URL named the instance); fixed in aa31774.

Also done: removed the stale `PYAUTO_SHIFT_BRIEF=…/2026-11-16-pm.md` override from `~/.config/pyauto/orchestrator.env` (human-approved). The "stranded" 2026-11-26-pm ledger op had been skipped and logged by the sweep, so nothing needed replaying.

Not fixed (CLI behaviour): a human `claude --bg` on a daemon that a worker started can still inherit worker variables.

## Original prompt

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
