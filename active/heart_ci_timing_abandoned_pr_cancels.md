# Heart ci_timing: PR runs cancelled when their PR closes are flagged as kill suspects

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

After PyAutoHeart#313 (superseded cancels), two red `suspect_cancelled` ci_timing
rows remain: autolens_workspace_test Smoke Tests 35438871780 and
autogalaxy_workspace_test Smoke Tests 35438870386 (branch
`feature/workspace-organs-regroup`, 2026-09-19). Both are `pull_request` runs
cancelled ~20 s after their PRs closed unmerged (autolens_workspace_test#323
closed 11:05:51, run ended 11:06:13; autogalaxy_workspace_test#124 closed
11:05:47, run ended 11:06:08), with no successor run. GitHub empties a run's
`pull_requests` once its PR closes, so the collector cannot see the closure.

Primary repository: @PyAutoHeart (`heart/checks/ci_timing.py`, `ci_timing.sh`).

## Ask

Classify a cancelled `pull_request` run with no successor as abandoned (benign,
counted, not an event) when its PR closed no later than the run's end +
`SUPERSEDE_SLACK_S`. Feed closures from one `pulls?state=closed&per_page=50`
fetch per polled repo, matched on head branch; a failed fetch degrades to
today's behaviour. No threshold/weight/slack changes; main/push cancels and PR
cancels with an open or much-later-closed PR stay suspects.

User request (verbatim): "do 1 yes bug fix"
