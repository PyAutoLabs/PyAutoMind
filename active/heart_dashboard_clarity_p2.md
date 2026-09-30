# Heart clarity PR B: structured reasons aligned with readiness, drift categories, score breakdown

Type: feature
Target: PyAutoHeart
Difficulty: medium
Autonomy: human-required
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/247
Priority: high

@PyAutoHeart. Parent intent, findings, design and the Fable review with its numbered amendments: `draft/feature/pyautoheart/heart_dashboard_clarity.md` in Mind. Human approved the amended plan on 2026-09-30; PR A merged as PyAutoHeart#246; see `complete/2026/09/heart-dashboard-clarity.md`.

Scope (parent detailed step 1 data model, the remainder of step 4, applicable step 5 validation):

- Structured entries in `sections[].entries` (stable id, subject, state, reason, evidence/source/age, action, `affects_release`); `_lib_row`/`_repo_section` keep the contributing observations instead of formatted strings. `affects_release` derives from the same rules as `readiness.py:302-315`: workspace behind/in_progress renders as advisory, not blocker-red; test a workspace with `behind=2` under a fresh verdict is not shown as blocking (amendment 1).
- Correct remedies: behind-origin → ff-pull canonical checkout + `pyauto-heart tick`; branch≠main/dirty → `fix dirty <repo>`; failing CI keeps its door; informational PRs are not failures. Row actions for Release validation and Test run via existing Brain doors. Notify PyAutoBrain that blocker prompts change, since the Brain board forwards them verbatim (amendments 2, 12).
- Drift: dirty task worktrees, missing claimed paths, clean orphan directories and dirty canonical checkouts with concrete paths, matching what `fix drift` already lists; freshness labelled independently of severity.
- Score: additive per-key `penalties` breakdown from `readiness.compute` (weights unchanged) and a “why this score” disclosure; dev-box vantage and age on the first screen (amendment 9).
- Fix-all prompt upgraded to consume the structured entries; CLI and dashboard stay in parity. Full md and terminal renderers adopt all-tier reasons; `--md-brief` stays one-tier.

Nothing new enters `blockers`; a `SCHEMA_VERSION` bump to 4 is optional. Preserve verdict/score. Dispatch `heart-health.yml` after merge.

Proposed branch `feature/heart-dashboard-reasons`. Follow start-dev → start-library → ship-library. Implementation approved on 2026-09-30; existing dependency and shipping gates still apply.
