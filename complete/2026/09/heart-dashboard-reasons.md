# Heart dashboard reasons and remedies

Merged PyAutoHeart PR #248 on 2026-09-30 as `7c59414da12155b907415d05ecceb955bb0bc105`, from head `32ba3bd1b72f1b118efbfa2b070829b088b835f5`. Issue #247 closed. All claimed branch commits are ancestors of origin/main.

Repository rows now use authoritative readiness reasons, distinguish release blockers from advisory checkout state, and offer appropriate remedies. All drift categories and reasons remain accessible, with source/age disclosures and an explained score breakdown. Release validation and test-run findings have actions. Structured entries preserve Brain consumers and public-path privacy.

Validation: 1081 Heart tests, 53 Brain consumer tests, unchanged legacy verdict fields across 14 fixture/profile comparisons, and browser checks at 375/390/1280 pixels in both themes, including 200% zoom, keyboard disclosures, clipboard failure and touch targets. Exact-head CI run 36768359819 passed both Python 3.12 and 3.13 jobs and every executed step.

Dashboard publication dispatched after merge: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/36768598628 (completed successfully). No scientific release was performed. Existing release-validation integrate failure remains; same-session human override authorized this dashboard work only.

PR C is unblocked; the parent packet remains as the reference for its remaining timing scope.

## Original prompt

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

## Delivery (2026-09-30)

PR https://github.com/PyAutoLabs/PyAutoHeart/pull/248 at 32ba3bd. 1081 Heart tests, 53 Brain consumer tests, 14 readiness baseline comparisons and mobile/desktop light/dark browser checks passed. Current RED: release validation FAILED (stage integrate), covered by the same-session dashboard development override; no merge or release authority. Brain consumer notice is on issue #247 and docs/internals.md. After human merge, publish via heart-health.yml and continue PR C. Local evidence/previews are in the task worktree root.
