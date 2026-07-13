## jax-docs-autogalaxy-datasets
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/100 (CLOSED)
- completed: 2026-05-24
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/101
- notes: Phase 4a + 4b combined. 8 scripts in autogalaxy_workspace/scripts/{imaging,interferometer}/ now carry __JAX__ prose; the 2 simulator.py files carry runnable __JAX Variant__ blocks using post-Phase-2 ag.SimulatorImaging(use_jax=True) and ag.SimulatorInterferometer(use_jax=True). Mirror of autolens_workspace#202 / PR #203 (Phase 3a/b/d combined). Same Array2D.native @jax.jit limitation flagged in variants; eager JAX works. Phase 4c (multi) deferred per scope anchor. Worktree removed; feature branch deleted local + origin.
