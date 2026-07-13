# Vendor `bessel_kve` into autoarray and drop the tensorflow-probability dependency

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised

Durable follow-up to the Matern-kernel tfp/jax incompatibility (PyAutoArray #385).
That bug was unblocked by pinning `tfp-nightly==0.26.0.dev20260713` in place of the
broken stable `tensorflow-probability==0.25.0` (0.25.0 references
`jax.interpreters.xla.pytype_aval_mappings`, removed from modern JAX). The nightly
works but is a **fragile dependency**: PyPI eventually prunes old nightlies, so the
pinned build may 404 for new installs in future, and an unpinned nightly makes
installs non-reproducible and can silently re-break on tfp drift.

The JAX Matern path (`autoarray/inversion/regularization/matern_kernel.py`, `kv_xp`)
needs `tensorflow_probability.substrates.jax.math.bessel_kve` **only** for the
modified-Bessel `K_v` term. `jax.scipy.special` has no `kv`/`kve` of arbitrary real
order, and `nu` is a continuous free prior (`Uniform(0.5, 5.5)`), so closed-form
half-integer Matern expressions are not sufficient.

**Goal:** vendor tfp's `bessel_kve` implementation into autoarray and remove the
entire `tensorflow-probability` / `tfp-nightly` dependency (a heavy dep — it drags
in the full TF-probability stack). This eliminates the whole version-incompatibility
class of bug permanently and drops a large optional dependency.

Scope / notes:
- Port `bessel_kve` and its interdependent helpers from
  `tensorflow_probability/substrates/jax/math/bessel.py`: `_temme_expansion`,
  `_temme_series`, `_continued_fraction_kv`, `_evaluate_temme_coeffs`,
  `_olver_asymptotic_uniform`, `_bessel_ive_shared`, `_sqrt1px2`,
  `_compute_general_continued_fraction`, plus the `custom_gradient`/`custom_jvp`
  plumbing (the JAX path is used with gradients — the port must stay
  differentiable). Translate the `tf`-on-jax shims (`tf.where`, `tf.math.exp`, …)
  to plain `jax.numpy`. Preserve the Apache-2.0 licence header / attribution.
- The vendored module is `xp`-threaded like the rest of autoarray; the NumPy path
  keeps using `scipy.special.kv` (unaffected).
- **Parity test** (the hard requirement): compare the vendored `kv`/`kve` against
  `scipy.special.kve` across a `(v, z)` grid spanning the prior range
  (`v ∈ [0.5, 5.5]`, a range of `z`) to a tight tolerance, plus a gradient check
  (`jax.grad` vs finite-difference). Lives in workspace_test (JAX), not
  `test_autoarray/`.
- On completion, remove `tfp-nightly` from `PyAutoArray/pyproject.toml` and update
  the `kv_xp` docstring/`ImportError` accordingly.

This is large and numerically delicate; keep it separate from the release-blocking
pin swap. See [[project_kernel_cdf_mesh_shipped]] and [[feedback_dependency_graph]].
