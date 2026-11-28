# Maintenance: SLOW since 2026-07-30: re-measured: times out at the 300s cap; JIT + full visualization pi

Type: maintenance
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Consequence: judge
Witness: the entry is gone from the repo's no_run.yaml and the script passes under the smoke cap
Review-minutes: 20
Lane: local-dev
Unattended: never
Source-key: no_run:autolens_workspace_test/imaging/visualization/modeling_visualization_jit

**Re-check first.** Filed from the `census` source (board census rows, 0.0 h old). Before any work, re-read the no-run census (`batch maintain --dry-run --sources census`) and the repo's `no_run.yaml`: if the entry is gone, close this draft as already fixed and stop.

Finding (`census`, key `no_run:autolens_workspace_test/imaging/visualization/modeling_visualization_jit`):
> SLOW since 2026-07-30: re-measured: times out at the 300s cap; JIT + full visualization pipeline

Evidence:
```json
{
 "date": "2026-07-30",
 "entry": "imaging/visualization/modeling_visualization_jit",
 "marker": "SLOW",
 "measured": false,
 "prompt": "Use the bug skill. no_run: autolens_workspace_test imaging/visualization/modeling_visualization_jit SLOW since 2026-07-30 with no measurement \u2014 retime against the real cap, then fix it or delete the marker",
 "reason": "re-measured: times out at the 300s cap; JIT + full visualization pipeline",
 "repo": "autolens_workspace_test"
}
```

Paths: `imaging/visualization/modeling_visualization_jit`, `no_run.yaml`

**Tier.** `Consequence: judge` is this finding's floor; never lower it.

Never: release, rehearse, dispatch a release or build workflow, force, or add a quarantine entry. A fix in a repo whose `main` CI is red needs the human's corrective exception to ship (AUTONOMY.md).

<!-- maint-key: no_run:autolens_workspace_test/imaging/visualization/modeling_visualization_jit -->
<!-- filed 2026-11-27 by the maintenance writer (PyAutoBrain#733) -->
