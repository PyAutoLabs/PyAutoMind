# Resolve release-profile timeout scripts deliberately

## Context

Five scripts exceeded PyAutoBuild's 300-second per-script cap in release run
`28784914443`. A timeout is a release-surface policy decision, not automatically a code
bug. Stateful local reruns are not authoritative because completed search output can make
chained scripts resume quickly.

Owners: @autogalaxy_workspace, @autolens_workspace, @PyAutoFit, @PyAutoGalaxy,
@PyAutoLens, and @PyAutoBuild where runner evidence is needed.

## Scripts

- `autogalaxy_workspace/scripts/ellipse/multipoles.py`
- `autolens_workspace/scripts/cluster/start_here.py`
- `autolens_workspace/scripts/cluster/modeling.py`
- `autolens_workspace/scripts/imaging/features/advanced/double_einstein_ring/chaining.py`
- `autolens_workspace/scripts/multi/features/slam/simultaneous.py`

## Required work

1. Benchmark each script from a clean output tree with the exact release profile and
   record phase-level timing. Confirm whether it completes correctly beyond 300 seconds.
2. Investigate avoidable repeated compilation, plotting, search, dataset, and chaining
   costs without reducing the scientific/tutorial contract.
3. For each script choose explicitly between:
   - optimize it to fit reliably below the cap; or
   - add a documented `SLOW` entry to that workspace's `config/build/no_run.yaml` because
     it is unsuitable for automated release validation.
4. Do not silently raise the global cap. Do not use cached outputs as pass evidence.
5. Validate optimized scripts from clean state or validate that the runner reports the
   chosen scripts as skipped with their documented reasons.
