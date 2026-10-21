## Summary
`heart/checks/ci_timing.py::classify_cancelled` flagged every cancelled `main` run as a kill-timer/hang suspect, so concurrency-group cancellations during merge bursts became red `suspect_cancelled` rows (8 on the board, some for weeks). A cancelled run of any event is now superseded when a newer same-workflow, same-branch run was created no later than its end (`updated_at` + `SUPERSEDE_SLACK_S` = 60 s); no successor, or one long after, stays suspect. PR runs keep their original rule; supersession is judged against every run of the workflow (the canceller is often in flight). No threshold/weight changes.

## PRs
- PyAutoLabs/PyAutoHeart#313

## Validation
test_ci_timing 43 passed, Heart suite 1281 passed; scratch collector 8 → 2 events (remaining 2: workspace_test PR runs cancelled ~20 s after the PR closed, no successor — left for a separate decision). First CI run failed the tenant firewall (instance names in a comment/docstring); fixed in 089f8fa, firewall check verified locally with a negative control. Shipped under a human Heart RED development override (2026-10-21).

## Original prompt

# Heart ci_timing flags superseded (concurrency-cancelled) runs as kill-timer reds

Type: bug
Target: health_fixes
Themes:
- heart
- ci
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Filed: 2026-10-21
Issued: 2026-10-21

## Context

Eight red `ci_timing:<repo>/<gate>:<run_url>` findings on the Heart dashboard are
`suspect_cancelled` events, e.g. PyAutoFit Tests runs 39064925733 and 39064933625
(2026-10-17 20:01:07/13) cancelled seconds before 39064940041 on the next push
succeeded; PyAutoArray 37002625195/37002707936 (10-02), and workspace_test Smoke
runs from 09-08/09-19. These look like ordinary concurrency-group cancellations,
not hangs or kill-timer hits, yet they hold the monitoring inventory red for weeks.

Primary repository: @PyAutoHeart (`heart/checks/ci_timing.py`).

## Ask

Confirm from the run metadata whether these were superseded by a newer run in the
same concurrency group; if so, classify them as superseded (not red) without
loosening real hang/kill detection. No threshold or weight changes.
