## Summary
The last two red `suspect_cancelled` ci_timing rows were workspace-test Smoke Tests PR runs cancelled ~20 s after their PRs closed unmerged, with no successor; GitHub empties `pull_requests` on close, so the collector could not see why. `ci_timing.sh` now fetches one best-effort page of closed PRs per repo; `classify_cancelled` marks a non-superseded PR-event cancel as **abandoned** (benign, counted in a new additive per-gate `abandoned` key) when a closed PR on its branch has `created_at ≤ closed_at ≤ updated_at + SUPERSEDE_SLACK_S`. No threshold/weight/slack changes.

## PRs
- PyAutoLabs/PyAutoHeart#315

## Validation
57 targeted + 1295 full-suite tests passed; tenant firewall OK locally; live scratch collector 2 → 0 events. Heart YELLOW acknowledged by the human (recorded after PR-open; ship-time ask was missed).

## Original prompt

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
