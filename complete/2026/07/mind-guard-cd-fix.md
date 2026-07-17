## mind-guard-cd-fix
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/130 (Phase 5, guard follow-up)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/138 (merged; live)
- summary: mind_commit_guard v1.2 — honour a leading `cd` away from Mind. v1.1 keyed is-Mind-commit off the ambient cwd the hook is handed, so a `cd .../PyAutoBuild && git commit` with session cwd still PyAutoMind was wrongly denied (bit its own author committing PyAutoBuild#165 step-3). check_command now walks clauses tracking effective cwd, resolves each commit's target repo (git -C wins else effective cwd), guards ONLY when under a PyAutoMind checkout. Dead _mind_root + unused re removed. 4 regression tests; 140 passed. This is the 2nd guard false-positive-on-its-author (v1.1 was the 1st) — refusals carry a measured FP cost, as the doc's §4 predicted.
