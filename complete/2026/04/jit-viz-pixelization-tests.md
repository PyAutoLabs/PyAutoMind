## jit-viz-pixelization-tests
- issue: none — visualization-during-modeling for pixelized sources (follow-up to mge-jit-visualization)
- completed: 2026-04-20
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/48
- note: scripts use n_batch=10 (vs default 100) because rectangular/Delaunay inversion under JAX vmap × default n_batch has a genuine peak memory cost (~40GB for rectangular on the jax_test dataset) that exceeded the 15GB dev box. Not a library bug; n_batch is the right tuning knob for pixelized+JAX workloads on memory-constrained machines.
