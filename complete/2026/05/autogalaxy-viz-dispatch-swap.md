## autogalaxy-viz-dispatch-swap
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/389
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/390
- repos: PyAutoGalaxy
- notes: |
    Phase 0b of z_features/jax_visualization.md. Three call sites in PyAutoGalaxy
    visualizers swapped from analysis.fit_from(instance=...) to
    analysis.fit_for_visualization(instance=...) — imaging/model/visualizer.py
    (single visualize() + visualize_combined()) and interferometer/model/visualizer.py.
    PyAutoLens made the same swap in #443 (2026-04-19); the autogalaxy side was
    overdue. Pytree registration prerequisites for both imaging (#364) and
    interferometer (#376) had already shipped — this was the last piece.

    Library tests: 106/106 passed. Smoke verification: visualization.py NumPy and
    modeling_visualization_jit.py JIT-during-Nautilus both PASS; visualization_jax.py
    surfaced a pre-existing latent test-script bug (missing register_model /
    enable_pytrees) which also affects the autolens equivalent since #443. Filed
    a follow-up prompt: autolens_workspace_test/visualization_jax_pytree_registration.md.
    Neither failure breaks CI smoke (visualization_jax.py is not in smoke_tests.txt
    and env_vars.yaml defaults force PYAUTO_DISABLE_JAX=1 for any imaging/visualization
    path, so the script silently falls through to NumPy under CI).

    Phase 0c (ag ellipse + quantity pytree) and Phase 1A (autolens interferometer
    JAX viz coverage) are now unblocked from this PR's perspective.
