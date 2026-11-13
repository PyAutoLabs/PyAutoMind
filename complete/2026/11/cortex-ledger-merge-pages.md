Shipped in PyAutoCortex#91 (closes PyAutoCortex#90), merged 2026-11-13 by the human's `/prm`.

`ledger_merge.yml`'s merge push uses `GITHUB_TOKEN`, which triggers no workflows; the step after it re-dispatched `cortex_check.yml` but not `pages_dashboard.yml`, so the Pages board kept the previous render after every check-in. The step ("Run the check on main and publish the board") now dispatches both, warning rather than failing if a dispatch is refused — the pattern `dashboard_refresh.yml` already used after its heal push.

Tests: PyAutoCortex `tests/` 105 passed locally. The PR had no CI checks (Cortex's workflows do not trigger on a workflow-file-only change); the human was told and authorized the merge.

Shipped under the Heart RED development override (recorded on the issue, the PR, active.md and autonomy_log.md 2026-11-13); Heart remains RED for release purposes.

## Original prompt

# Ledger merge also publishes the Pages board

Targets: @PyAutoCortex
Type: bug
Filed: 2026-11-13
Issued: 2026-11-13
Issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/90
Consequence: judge

Verbatim user request (2026-11-13): "yes file it and fix it" — in reply to: ledger_merge.yml triggers cortex_check.yml after its GITHUB_TOKEN merge push but not pages_dashboard.yml, so the Pages board lags every check-in.

Tier: judge — merge mode: human /prm
