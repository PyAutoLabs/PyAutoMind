# Heart: a weekly organ workflow's RED clears when the fix merges, not next Monday

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: glance
Witness: a PR that fixes a red `Workspace Smoke` run and merges to PyAutoHeart `main` triggers a fresh `Workspace Smoke` run within one hour (run id with event `push` or `workflow_run` shown), and the release verdict's organ-workflow reason clears on the next feed refresh; a test of the trigger filter shows an unrelated merge does not rerun it
Review-minutes: 10
Unattended: never
Lane: any

Source: REL-15 of the ecosystem review (2026-11-10), section B8. **Unverified by the review: re-check first.**

**Already done (M2.1, PyAutoHeart#342):** organ workflows are "shown, never blocking" in the dev-ship gate (`heart/readiness.py:79-84`). What is left is the **release** verdict: a red weekly run stays a RED reason until the next scheduled run.

**Anchors (Heart 00d979a):** `.github/workflows/workspace-smoke.yml:13` (`cron: "0 3 * * 1"`, Mondays only); `config/repos.yaml:119-126` and `:175` (Workspace Smoke as a release-gating organ workflow). The review also names PyAutoHands "Python Version Matrix".

**Re-check first:** `gh run list -R PyAutoLabs/PyAutoHeart --workflow workspace-smoke.yml --limit 10 --json conclusion,createdAt,event`, and for each red run, when the fix merged versus when the next run went green. Drop this draft if no red run outlived its fix by more than a day since 2026-10-01.

**Change (rerun, not expire):** trigger the weekly organ workflows on `push` to `main` touching their own paths (or on `workflow_dispatch` from the fix PR's merge), in addition to the cron. Do **not** expire the reason when the failing commit is no longer HEAD: that changes what the release gate accepts and would be a judge-tier ruling.

Tier glance: more runs, same gate.
Programme: M3 side lane; the keep-green lane (`shift_keeps_heart_green_lane.md`) would otherwise dispatch these reruns by hand.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
