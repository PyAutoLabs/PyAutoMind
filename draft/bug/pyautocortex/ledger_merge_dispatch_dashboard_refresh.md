# Cortex ledger auto-merge leaves main red after a project birth — ledger_merge.yml never dispatches dashboard_refresh.yml

Type: bug
Target: pyautocortex
Repos:
- PyAutoCortex
Themes:
- cortex
- ci
Difficulty: easy
Autonomy: safe-capped
Priority: high
Status: draft
Consequence: glance
Witness: After a `claude/birth-*` ledger branch auto-merges via `ledger_merge.yml`, `dashboard_refresh.yml` runs on main without a human dispatch, heals `dashboard.md`/`dashboard.html`/`state.json`, and the Cortex Check on the resulting main tip is green — shown by the run links of one real or test birth after the change.
Review-minutes: 2
Unattended: ready
Lane: any
Filed: 2026-11-26
Updated: 2026-11-26

## Request (verbatim)

"Draft a start_dev prompt to make ledger_merge.yml trigger dashboard_refresh" — the permanent fix
for the Cortex main-red found in the 2026-11-26 orchestrator PR sweep.

## Finding

2026-11-26 17:27, PyAutoCortex `09a0de6` ("cortex: auto-merge ledger branch
claude/birth-sdssj0946_subhalo_v2") added `projects/sdssj0946_subhalo_v2.md` and its
`projects.yaml` row, but did not re-render the board. Cortex Check on main then failed:

    FAILED tests/test_cortex.py::test_the_committed_board_files_each_project_under_its_folders_kind
    AssertionError: sdssj0946_subhalo_v2 is not in its active section

The same thing happened at 17:14 after the `erc_angular_structure` birth (`23ec5b5`); a later
push happened to heal it. While main is red, later ledger merges and PRs (e.g. Cortex#102) inherit
the failure.

## Cause

`ledger_merge.yml` pushes the merge with `GITHUB_TOKEN`, which triggers no workflows. Its final
step ("Run the check on main and publish the board") explicitly dispatches `cortex_check.yml` and
`pages_dashboard.yml` — but not `dashboard_refresh.yml`. So a ledger merge that changes the board
(a birth, retirement or status move) leaves `dashboard.md` stale until the 03:35 cron or another
push. Manual heal used on 2026-11-26: `gh workflow run dashboard_refresh.yml --ref main`, then
`gh workflow run cortex_check.yml --ref main` (the heal push is also `GITHUB_TOKEN`, so it does
not trigger Cortex Check either).

## Fix sketch

- In `ledger_merge.yml`'s final step, dispatch `dashboard_refresh.yml` on main (it already
  dispatches Pages after its own heal push).
- Ordering: `cortex_check.yml` dispatched at the same moment would check the stale tip and fail.
  Either have `dashboard_refresh.yml` dispatch `cortex_check.yml` after its heal push (it has
  `actions: write` semantics to add if missing), or drop the direct check dispatch from
  `ledger_merge.yml` and let the refresh own "check main after heal". Keep the no-op path: when
  the board is already fresh, the refresh should still dispatch the check so the merge commit is
  checked.
- Confirm `dashboard_refresh.yml` declares `workflow_dispatch` (it does, line ~48) and the
  `actions: write` permission it needs to dispatch.
