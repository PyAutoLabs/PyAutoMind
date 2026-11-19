## matern-vendor-bessel-kve
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/694
- completed: 2026-11-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/695
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/137, https://github.com/PyAutoLabs/autolens_workspace_test/pull/366
- summary:
  - Vendored tfp's `bessel_kve` K-branch (Temme series z<=2, Steed continued fraction z>2, forward recurrence, Olver asymptotics nu>=50) as pure `jax.numpy`/`lax` in `autoarray/inversion/regularization/bessel.py` (Apache-2.0 header + modification list kept); `jax.custom_jvp` with tfp's z-derivative rule. `kv_xp`'s JAX branch uses it; `tfp-nightly` dropped from `autoarray[optional]`. The I_v branch, `bessel_iv_ratio`, `_compute_general_continued_fraction` and log-space variants were not needed and not ported.
  - Parity: max rel err vs `scipy.special.kve` 9e-14 over nu in [0.5, 5.5], 2.3e-13 over nu 0-60 x z 1e-8..1e3 (independent review); z-gradient and second derivative vs closed forms 2.3e-13. Near the float64 overflow edge (nu>=50, tiny z) the port returns finite values where scipy returns inf.
  - Library tests: kv_xp JAX vs scipy spot check (both sides of z=2, half-integers, Olver), dK/dz vs closed form, Matern scale-gradient FD. Workspace: `autogalaxy_workspace_test/scripts/misc/jax_assertions/bessel_kve_parity.py` (added to smoke; 7/7 mutation probes caught); tfp prose removed from agwt/alwt scripts and smoke_install.sh.
  - Gotcha: float32 inputs must avoid numpy float64 scalars (`np.log(2.0)`) in the loop carries or `lax.while_loop` rejects the dtype change. The JAX Matern path is only accurate to ~7e-4 in float32 near r=0 (clamped 1e-8); workspace profiles run x64.
  - Known limitation (preserved from tfp, documented in `kv_xp`): no derivative in the Bessel order, so the Matern gradient w.r.t. nu is wrong (not zero). Follow-up candidate if nu is ever sampled with gradients. Started under a human repo-claim override alongside galaxy-duplicate-pytree-registration (#693).
  - Follow-up: the same outdated tfp `smoke_install.sh` comment remains in autolens_workspace, autogalaxy_workspace, HowToGalaxy, HowToLens and euclid_strong_lens_modeling_pipeline.

## Original prompt

# Vendor `bessel_kve` into autoarray and drop the tensorflow-probability dependency

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
Themes:
- pixelization
- hygiene
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: The vendored `kve`/`kv` match `scipy.special.kve` to rtol 1e-10 on a (v in [0.5, 5.5]) x z grid with `jax.grad` matching finite differences (workspace_test), the existing Matern-kernel tests pass unchanged, and `tensorflow-probability`/`tfp-nightly` appear in neither `pyproject.toml` nor any import.
Review-minutes: 3
Unattended: ready
Lane: any
Filed: 2026-07-13 (backfilled from git)
Issued: 2026-11-15
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/694

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
