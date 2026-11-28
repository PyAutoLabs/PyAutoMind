# Maintenance: [red] ci_status: PyAutoNerves/workflows/Nerves Board — failure

Type: maintenance
Target: autonerves
Repos:
- PyAutoNerves
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
Source-key: ci:PyAutoNerves:Nerves Board

**Re-check first.** Filed from the `monitoring` source (published board, 0.0 h old). Before any work, re-read the Heart board (`batch maintain --dry-run --sources monitoring`): if the key is absent or green, close this draft as already fixed and stop.

Finding (`monitoring`, key `ci:PyAutoNerves:Nerves Board`):
> [red] ci_status: PyAutoNerves/workflows/Nerves Board — failure

Evidence:
```json
{
 "detail": {
  "conclusion": "failure",
  "created_at": "2026-11-27T15:41:10Z",
  "head_sha": "3af6de8",
  "on_head": true,
  "status": "completed",
  "url": "https://api.github.com/repos/PyAutoLabs/PyAutoNerves/actions/runs/46027093285"
 },
 "family": "ci_status",
 "fresh": true,
 "id": "ci_status:PyAutoNerves/workflows/Nerves Board:",
 "observed_at": "2026-11-27T22:32:07+00:00",
 "source": "snapshot.ci_status:PyAutoNerves/workflows/Nerves Board",
 "status": "red"
}
```

Paths: `workflows/Nerves Board`

**Tier.** `Consequence: judge` is this finding's floor; never lower it.

Never: release, rehearse, dispatch a release or build workflow, force, or add a quarantine entry. A fix in a repo whose `main` CI is red needs the human's corrective exception to ship (AUTONOMY.md).

<!-- maint-key: ci:PyAutoNerves:Nerves Board -->
<!-- filed 2026-11-27 by the maintenance writer (PyAutoBrain#733) -->
