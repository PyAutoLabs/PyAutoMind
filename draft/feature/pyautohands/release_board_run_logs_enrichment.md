# Release board: local run_logs enrichment

Type: feature
Target: pyautohands
Repos:
- PyAutoHands
Themes:
- dashboard
- release
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-19 (backfilled from git)

Follow-up to the release board (PyAutoHands#239, shipped 2026-08-19). The v1
board is API-first because `run_logs/` (the rich local run history written by
@PyAutoHands/autohands/run_all.py) is gitignored, machine-local, and often
absent. Mirror the Heart's devbox pattern (`pyauto-heart publish` →
`state/devbox_board.json`, age-stamped merge): distill `run_logs/index.md`'s
row data (run type, pass/fail/skip/timeout counts, per-project) into a small
committed JSON the board merges as a "local validation runs" section, stamped
with its observation age and expiring honestly. Local paths scrubbed; the
Heart's `run_logs/latest` consumers untouched.
