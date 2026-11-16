## health-review-cloud-observation
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/636 (MERGED 2026-11-15, merge 421ef0f)
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/348 (MERGED 2026-11-15, merge 8df451c)
- completed: 2026-11-15
- merged-by: human-typed /prm (cloud session https://claude.ai/code/session_016nhQ8RkwYK9RzapmsQRGCj)
- summary:
  - PyAutoBrain: `health --scope dashboard` read "No cache yet" prose from a never-ticked local Heart (every cloud session) and reported "inventory missing" (exit 4). `dashboard.py --published-fallback` now reads the published board only when the local Heart printed no JSON object; a parseable local board without inventory stays explicitly unknown. JSON names its `source`. Suite 2017 passed / 2 skipped; CI 3.12 + 3.13 green.
  - PyAutoHeart: the Heart Health publish run listed itself (still running) as the newest `Heart Health` run, so `PyAutoHeart:ci` / `ci_status:PyAutoHeart*` read in_progress on every publish. `ci_status.observer_run_id` sets aside the run whose id is `GITHUB_RUN_ID` when Heart observes its own repo; all other in-progress runs unchanged. Suite 1463 passed; CI 3.12 + 3.13 green.
  - No thresholds, weights or gates changed.
- verify: the next Heart Health publish should show `PyAutoHeart:ci` from the previous completed run, not in_progress.

## Original prompt

# Health: cloud-session dashboard reads and Heart's own in-progress run

Type: bug
Target: PyAutoBrain, PyAutoHeart
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: medium
Status: in development
Issued: 2026-11-15
Consequence: judge

## Findings (2026-11-15 health review)

1. **PyAutoBrain — `health --scope dashboard` blind in a cloud session.** With a
   PyAutoHeart checkout present but never ticked, `vitals.sh dashboard --json`
   prints "No cache yet — run `pyauto-heart tick` first"; `health.sh` piped that
   prose into `dashboard.py`, which reported "Heart monitoring inventory is
   missing" (exit 4) while the published board held a full inventory
   (1297 checks / 153 findings). Anchors: `agents/conductors/health/health.sh`
   dashboard branch; `agents/conductors/health/dashboard.py` `main`.
2. **PyAutoHeart — permanent self-made "CI in progress".** The Heart Health
   publish run lists its own still-running run as the newest `Heart Health`
   run, so `ci_status:PyAutoHeart`, `ci_status:PyAutoHeart/workflows/Heart Health`
   (grey) and `PyAutoHeart:ci` (yellow) were raised by every publish and could
   never be cleared by a repair. Anchor: `heart/checks/ci_status.py`
   `build_sidecar`.

## Change

1. `dashboard.py --published-fallback` (passed by `health.sh`): when the local
   Heart prints no JSON object, read the published board. A local board that
   parses but lacks or mangles its inventory is never replaced (still exit 4).
   Output names the board read in `source` (`local` | `published`).
2. `ci_status.observer_run_id(name)`: inside GitHub Actions, when the observed
   repo is the observer's own repository, the run whose id is `GITHUB_RUN_ID`
   is set aside; the previous run of that workflow is the evidence. Every other
   in-progress run still reads as in progress. Runs keep their id in
   `normalize_runs`.

No thresholds, weights or gates changed.

Branch: claude/pyautolabs-health-review-oja0ir (both repos)
