## cluster-simulator-jax-multiplane
- issue: https://github.com/Jammy2211/autolens_workspace/issues/89
- completed: 2026-04-27
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/91
- notes: Refactored `scripts/cluster/simulator.py` to (a) shrink to 2 main lens galaxies + 1 host halo (was 5), (b) move sources to distinct redshifts z=1.0 and z=2.0 for a true multi-plane lens, (c) JAX-jit the PointSolver via the pytree-registration pattern from `autolens_workspace_developer/jax_profiling/point_source/image_plane.py` (>5min → fast), (d) collapse 3 grids down to 2 (rendering grid shared between simulation and viz, PointSolver's internal grid kept separate), and (e) polish docstrings to match `scripts/imaging/simulator.py` tone with new `__Multi-Plane Setup__` and `__JAX JIT__` sections. Single-commit squash merge.
