## jax-docs-core-datasets
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/202 (CLOSED)
- completed: 2026-05-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/203
- notes: Phase 3a + 3b + 3d combined. 11 scripts in autolens_workspace/scripts/{imaging,interferometer,point_source}/ now carry __JAX__ prose; the 3 simulator.py files carry runnable __JAX Variant__ blocks using post-Phase-2 SimulatorImaging(use_jax=True), SimulatorInterferometer(use_jax=True), PointSolver(use_jax=True) + autolens.jax.register_tracer_classes. point_source/simulator.py's variant is the only one where @jax.jit works end-to-end (PointSolver doesn't go through Array2D.native autoarray limitation that blocks image/interferometer simulators under jit). Dataset binary leakage from local smoke run was reset before commit per [[feedback_ship_workspace_binary_leak]]. Phase 3c/3e/3f deferred per scope anchor. Worktree removed; feature branch deleted local + origin.
