# Maintenance: [red] ci_status: PyAutoHands/workflows/Dashboard — failure

Type: maintenance
Target: pyautohands
Repos:
- PyAutoHands
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-27
Consequence: judge
Witness: the key is absent, or green, on a fresh Heart board read
Review-minutes: 20
Lane: any
Unattended: never
Source-key: ci:PyAutoHands:Dashboard

**Re-check first.** Filed from the `monitoring` source (published board, 0.0 h old). Before any work, re-read the Heart board (`batch maintain --dry-run --sources monitoring`): if the key is absent or green, close this draft as already fixed and stop.

Finding (`monitoring`, key `ci:PyAutoHands:Dashboard`):
> [red] ci_status: PyAutoHands/workflows/Dashboard — failure

Evidence:
```json
{
 "detail": {
  "conclusion": "failure",
  "created_at": "2026-11-27T15:26:32Z",
  "head_sha": "38a7eef",
  "on_head": false,
  "status": "completed",
  "url": "https://api.github.com/repos/PyAutoLabs/PyAutoHands/actions/runs/46024939750"
 },
 "family": "ci_status",
 "fresh": true,
 "id": "ci_status:PyAutoHands/workflows/Dashboard:",
 "observed_at": "2026-11-27T22:32:06+00:00",
 "source": "snapshot.ci_status:PyAutoHands/workflows/Dashboard",
 "status": "red"
}
```

Paths: `workflows/Dashboard`

**Tier.** `Consequence: judge` is this finding's floor; never lower it.

Never: release, rehearse, dispatch a release or build workflow, force, or add a quarantine entry. A fix in a repo whose `main` CI is red needs the human's corrective exception to ship (AUTONOMY.md).

<!-- maint-key: ci:PyAutoHands:Dashboard -->
<!-- filed 2026-11-27 by the maintenance writer (PyAutoBrain#733) -->
