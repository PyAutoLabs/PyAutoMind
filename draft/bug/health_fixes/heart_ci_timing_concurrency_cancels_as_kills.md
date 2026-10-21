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
