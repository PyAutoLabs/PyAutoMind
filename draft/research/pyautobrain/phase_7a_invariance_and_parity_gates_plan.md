# Phase 7a plan: golden-number invariance and numpy/JAX/numba parity gates (planning only)

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: a written plan, approved by the human, that inventories the existing golden and parity scripts and tests, proposes one Heart check and its run cadence, and states the `notify` rule an invariance-guarded refactor would earn
Review-minutes: 15
Lane: any
Unattended: never

Slice 14.6 of `draft/feature/pyautobrain/maintenance_orchestrator.md`: phase 7a runs inside phase 14. No build.

## What the 2026-11-27 survey found

Nothing exists as a gate. There are scattered pieces:
- PyAutoFit `test_autofit/non_linear/samples/golden/`;
- `autofit/export/parity.py`;
- the `scripts/misc/jax_assertions/*parity*.py` workspace-test scripts;
- `imaging/simulator/use_jax_parity.py`;
- `graphical/ep_parity.py`;
- two `autolens_workspace_test` likelihood-value scripts.

There is no numpy/JAX/numba three-way parity anywhere.

## The plan must settle

- **What counts as a golden number**, and where the goldens live.
- **Tolerance policy per backend**, including fp64 vs mixed precision.
- **Where the gate runs:** a Heart check, CI or nightly, at what cost.
- **What earns `notify`:** how a refactor's PR proves it left every golden number unchanged, which makes it `notify`-tier work.
