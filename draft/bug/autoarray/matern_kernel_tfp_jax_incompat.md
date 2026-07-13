# Matern-kernel regularization crashes: tensorflow-probability 0.25.0 incompatible with jax 0.10.2

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Any pixelization using **Matern-kernel regularization** crashes at import on the current
resolved stack (`jax`/`jaxlib` 0.10.2, `tensorflow-probability` 0.25.0). Surfaced by the
2026-07-13 release-validation Stage-3 run (PyAutoHeart workspace-validation
`run_id=29266305445`, TestPyPI `2026.7.13.1.dev65501`) — `autogalaxy` imaging
`scripts/imaging/features/pixelization/galaxy_reconstruction.py` FAIL, and the same import
almost certainly drives the autolens imaging + autolens/autogalaxy interferometer
pixelization failures in that run.

Root cause — `autoarray/inversion/regularization/matern_kernel.py:37` (`kv_xp`) lazily does
`import tensorflow_probability.substrates.jax as tfp`; TFP 0.25.0 then executes
`tensorflow_probability/.../internal/backend/jax/ops.py:681`:

```
jax.interpreters.xla.pytype_aval_mappings[onp.ndarray]
AttributeError: module 'jax.interpreters.xla' has no attribute 'pytype_aval_mappings'
```

`pytype_aval_mappings` was removed from `jax.interpreters.xla` in a JAX version newer than
what TFP 0.25.0 targets — so `jax 0.10.2 + tfp 0.25.0` is a broken combination. This ships
broken to real users on the current stack; it is NOT gated by the curated smoke subset
(only the full release-fidelity set exercises Matern pixelization), so the nightly release
would not catch it. Scoped to the Matern path — `pixelization/likelihood_function.py`
passed; only the TFP-importing regularization fails.

Resolution options to weigh (do NOT assume one): (a) add/lower a dependency cap so
`jax`/`jaxlib` resolve to a version TFP 0.25.0 supports; (b) bump `tensorflow-probability`
to a release compatible with jax 0.10.x, if one exists; (c) remove the TFP dependency from
`matern_kernel.py` by computing the modified-Bessel `kv` term via `jax.scipy`/`scipy`
directly (drops a heavy dep). First find where the jax/tfp caps are declared (autoarray vs
autoconf) — see [[feedback_dependency_graph]] and the parked `astropy_cap_bump` cap work —
then reproduce on a clean env with the pinned versions before choosing. Add a regression
test that imports/exercises Matern-kernel regularization under JAX.
