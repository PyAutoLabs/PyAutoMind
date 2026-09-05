# Smoke-timings ingester: per-script CI timing rows on the Heart performance board

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoHands
Difficulty: large
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 1
Issued: 2026-09-05

Build the smoke-timings ingester: per-script CI timing rows on the Heart performance board.

Every gate run in all ten workspace/_test/HowTo repos already uploads a
`smoke-timings-<py>` artifact (`test-results/smoke_timings.json`, schema `smoke_timings/1`:
entry, kind, status, seconds, cap_s, exit_code — emitted by
`PyAutoHands/autohands/result_collector.py`, PyAutoHands#265), and the weekly
`workspace-validation.yml` uploads `smoke-timings-scripts-*` / `smoke-timings-notebooks-*`.
Nothing reads them: `workspace-validation.yml:389` calls this "the deferred Heart-board
timing ingester" and there are zero references to `smoke_timings` under `PyAutoHeart/heart/`.

Add the ingester to the daily `heart-health.yml` cloud run (which already runs `ci_timing`
at 05:00 UTC): fetch the latest smoke-timings artifacts per repo via the Actions API, fold
per-script rows into the board's performance surface next to the existing workflow-level
gates. Board rendering: most-recent per-script times with the slowest scripts highlighted
(per-repo top-N), status/cap context, and drift marking against the previous observation
consistent with ci_timing's existing warn thresholds. Design reference: Plane B of
`PyAutoMind/docs/pyautoheart/test_performance_board_assessment.md`. Follow the existing
check pattern (`heart/checks/ci_timing.py` + sidecar/aggregate split) so the dashboard
section renders from `board.json` like the current performance block.

Scope guard: this phase is read-and-render only — durable history is phase 2 of the epic
(`Epic: ci-timing-fast-tests`); do not build storage here beyond what the board already
self-carries.
