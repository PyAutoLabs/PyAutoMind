# Select a distinct prior run for unit timing comparisons

Type: bug
Priority: high
Difficulty: small
Autonomy: human-required
Target: @PyAutoHeart

## Original request

Check why heart is red, fix it, and then do anything else to make whole dashboard green

Follow-up: Yes merge prm and continue

## Approved parent scope

Continuation of #274's approved timing-evidence repairs. Parent collector PR #275 merged; this is a distinct phase, not a scoring-policy change. Proposed branch: feature/unit-timing-distinct-baseline. Tier: undeclared — merge mode: human /prm.

## Reproduced cause

After refreshing unit timing artifacts, all 300 observations lack a comparison even though committed history includes older runs. `heart.timings.previous_unit_rows` selects the latest recorded row per Python leg without the current observation's identity. That row is often the same run; `classify_drift` correctly rejects self-comparison, but the reader never selects the actual prior run.

## Plan

- Pass current per-repository/Python run identity and observation time into baseline selection.
- Select the latest distinct prior recorded run within the current epoch; never use the current or future run as its baseline. Preserve existing cache-state guards and missing-evidence semantics.
- Keep unchanged callers compatible; restrict changes to heart/timings.py, heart/checks/unit_timings.py, their focused tests and relevant contract documentation.
- Add regression coverage for current run already recorded, older valid baseline, future/out-of-order records, per-Python legs, epoch exclusion and truly absent baselines. Run focused and full Heart tests and compare real snapshot output without claiming every timing becomes green.
