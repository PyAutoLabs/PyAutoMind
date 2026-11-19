## galaxy-duplicate-pytree-registration
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/693
- completed: 2026-11-18
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/702

Building a JAX `Fitness` registers `Galaxy` through `autofit.jax.register_model`. A later `autolens.jax.register_tracer_classes` in the same process then hit `autoarray.abstract_ndarray.register_instance_pytree(Galaxy)`, and JAX raised `Duplicate custom PyTreeDef type registration`. Both autoarray registration helpers now go through `_register_pytree_node_once`, which keeps an existing registration (the first route wins, matching autofit's own tolerance) and still raises any other `ValueError`. The merge commit is `5815019d`.

- History: a shift worker started the task on 2026-11-14 (2026-11-14-pm2) and committed the fix locally, then crashed before pushing. The stale claim on PyAutoArray blocked other tasks, which surfaced as questions.md Q5 (numba_wtilde_validation_legs_stall_nautilus). A live session on 2026-11-18 rebased the commit onto main, verified it and shipped it.
- Evidence: autoarray 2461 passed. Direct reproduction with real JAX (`register_model`, then `register_tracer_classes`, then `tree_leaves`) raises on the old `main` and passes on the branch. PyAutoLens `test_analysis_point_gradient_mode` + `test_static_lattice_jax` + `test_solver_spurious_core` in one session: 32 passed. Those also pass on main, because the gradient-mode test never registers `Galaxy` through `register_model`, so the direct reproduction is the real control. Workspace smoke all passed (autofit 10, autogalaxy 16, autolens 44, autolens_workspace_test 39, euclid 9, HowToLens 41). autocti and autocti_test did not run because the laptop has no GSL headers (`libgsl-dev`). Heart dev gate GREEN. CI GREEN.
- PyAutoFit (listed in the prompt) needed no change: `register_model` already tolerated the duplicate.

## Original prompt

# Building a JAX Fitness then calling register_tracer_classes raises "Duplicate custom PyTreeDef type registration for Galaxy"

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- PyAutoFit
Themes:
- jax
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: in one Python process, construct a JAX `af.Fitness` for an `al.AnalysisPoint` model (which calls `autofit.jax.register_model` and registers `Galaxy` as a pytree), then run the autoarray/autolens `register_tracer_classes` path used by `test_autolens/.../test_static_lattice_jax.py`; it no longer raises, and the 16 static-lattice JAX tests pass when run after a JAX-Fitness test in the same session.
Filed: 2026-09-27
Updated: 2026-09-27
Lane: any
Verified: 2026-11-14 102f0249 (PyAutoArray), 362ee746 (PyAutoFit)

## Finding

Found while shipping PyAutoFit#1649 / PyAutoLens#752 (phase 2d of the source-plane point-source
campaign, record `complete/2026/09/point-source-gradient-mode.md`). Two independent pytree
registration paths do not know about each other:

- `autofit.jax.register_model(model)` (PyAutoFit `autofit/jax/pytrees.py`) registers the model's
  classes, including `Galaxy`, when a JAX `Fitness` is built;
- autoarray's `register_instance_pytree`, reached via `register_tracer_classes` (static-lattice JAX
  path), registers `Galaxy` again and JAX raises
  `ValueError: Duplicate custom PyTreeDef type registration for Galaxy`.

It is test-order dependent: running the new PyAutoLens gradient-mode tests in-process before
`test_static_lattice_jax.py` failed 16 tests. PyAutoLens#752 works around it by running its JAX
checks in a subprocess. Any user script that builds a JAX `Fitness` and then uses the static-lattice
path in the same process would hit it too.

## Fix direction

Make registration idempotent across both paths — one shared "already registered" check (e.g. a
single registry both helpers consult, or catching the duplicate and verifying the existing
flatten/unflatten is compatible). Then drop the subprocess workaround in
`test_autolens/point/model/test_analysis_point_gradient_mode.py` as the regression test.
