## jax-likelihood-datacube
- issue: none — Phase 4 of the datacube roadmap (followup to autolens_workspace#120)
- completed: 2026-05-15
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/96
- repos: autolens_workspace_test
- notes: Phase 4 closes the datacube roadmap. Adds autolens_workspace_test/scripts/jax_likelihood_functions/datacube/{rectangular,delaunay}.py — end-to-end JIT-correctness regression scripts for the cube likelihood path (the regression net the Phase 1 rewrite punted to this folder). Mirrors interferometer/{rectangular,delaunay}.py with N=4 identical-channel FactorGraph wiring (multi/delaunay.py is the structural analogue). Each script asserts vmap (against the 4× single-channel literal: rectangular=-12657.14500637, delaunay=-12661.69554044), Path A jit(log_likelihood_function) round-trip via instance_from_vector(xp=jnp), and Path B TransformerNUFFT cross-check. scripts/CLAUDE.md updated. Full datacube roadmap now complete: Phase 1 (autolens_workspace#149) user-facing pedagogical likelihood walkthrough, Phase 2 (autolens_workspace_developer#61) jit/interferometer/delaunay.py step-by-step profiling, Phase 3 (autolens_workspace_developer#62) jit/datacube/delaunay.py cube profiler with channel-invariant/variant taxonomy, Phase 4 (this) JIT regression scripts.
