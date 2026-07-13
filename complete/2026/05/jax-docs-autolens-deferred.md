## jax-docs-autolens-deferred
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/206 (CLOSED)
- completed: 2026-05-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/207
- notes: Phase 3c + 3e + 3f bundled. 10 scripts in autolens_workspace/scripts/{multi,group,cluster}/. Substantive change: cluster/simulator.py migrated from ~60-line manual ceremony (af.Collection mirror + _register_model_pytrees + register_instance_pytree) to single autolens.jax.register_tracer_classes(tracer) + PointSolver(use_jax=True) + @jax.jit pattern. Migration validated end-to-end with PYAUTO_TEST_MODE=1 (CPU JIT compile ~5 min for 800x800 grid, then runs; GPU much faster). Closes autolens side of jax_user_intro series.
