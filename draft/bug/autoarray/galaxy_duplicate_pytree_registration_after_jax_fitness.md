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
