# Maintenance: [red] ci_status: PyAutoInsight/workflows/Pages Dashboard — failure

Type: maintenance
Target: pyautoinsight
Repos:
- PyAutoInsight
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-27
Consequence: glance
Witness: the key is absent, or green, on a fresh Heart board read
Review-minutes: 3
Lane: any
Unattended: ready
Source-key: ci:PyAutoInsight:Pages Dashboard

**Re-check first.** Filed from the `monitoring` source (published board, 0.0 h old). Before any work, re-read the Heart board (`batch maintain --dry-run --sources monitoring`): if the key is absent or green, close this draft as already fixed and stop.

Finding (`monitoring`, key `ci:PyAutoInsight:Pages Dashboard`):
> [red] ci_status: PyAutoInsight/workflows/Pages Dashboard — failure

Evidence:
```json
{
 "detail": {
  "conclusion": "failure",
  "created_at": "2026-11-27T13:16:53Z",
  "head_sha": "604960d",
  "on_head": true,
  "status": "completed",
  "url": "https://api.github.com/repos/PyAutoLabs/PyAutoInsight/actions/runs/46005747314"
 },
 "family": "ci_status",
 "fresh": true,
 "id": "ci_status:PyAutoInsight/workflows/Pages Dashboard:",
 "observed_at": "2026-11-27T22:32:07+00:00",
 "source": "snapshot.ci_status:PyAutoInsight/workflows/Pages Dashboard",
 "status": "red"
}
```

Paths: `workflows/Pages Dashboard`

**Tier rule (Phase 14.1).** `Consequence: glance` is this finding's floor and holds only while the fix stays on its own surface (the code the red workflow runs in PyAutoInsight), which excludes `.github/workflows/`, dependency pins and public names. If your diff touches any of those, or another repo, raise `Consequence:` to `judge` before shipping and say why in the PR; never lower it.

Never: release, rehearse, dispatch a release or build workflow, force, or add a quarantine entry. A fix in a repo whose `main` CI is red needs the human's corrective exception to ship (AUTONOMY.md).

<!-- maint-key: ci:PyAutoInsight:Pages Dashboard -->
<!-- filed 2026-11-27 by the maintenance writer (PyAutoBrain#733) -->
