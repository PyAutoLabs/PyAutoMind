# Known issue (not yet reproducible): JAX visualization inversion blow-up

**Status:** information only — a documented, *not currently reproducible* bug.
No feature/code attached. Pick up if it crops up again on an HPC run.

**Discovered:** 2026-05-29, debugging Sam's SLaM run (`slacs0936+0913`,
`mass_EPL` phase). Repro/diagnostic harness left at `z_help/sam/`
(`remake_fit.py`, `settings_stress_test.py`, `jax_test.py`, `warm_jax_test.py`).

## Symptom

A completed search reports a healthy maximum log-likelihood, but the
visualization it writes to disk (`image/fit.png`, `image/fit.fits`,
`image/galaxy_images.fits`) shows a **pathological inversion**: the model
over-predicts the data at *every* pixel (residuals ≤ 0 everywhere), with
normalized residuals up to ~−700σ and a source reconstruction ~70× too bright.

The saved outputs are **internally inconsistent**, which is the smoking gun:

| Quantity | Saved `fit.fits` | Reported in `model.results` |
|---|---|---|
| reduced χ² (from `CHI_SQUARED_MAP`) | **~5,800** | ~0.4 (consistent with the reported log-L) |
| `NORMALIZED_RESIDUAL_MAP` | −693 … 0 (one-sided) | — |
| log-likelihood | implied ≈ −5.8×10⁷ | **−31,536** |

A clean rebuild of the *same* max-likelihood tracer + dataset gives the healthy
fit (log-L ≈ −31,145, residuals ±3.3σ). So the lens model is fine; the
visualization step solved the inversion's linear algebra differently from the
likelihood function.

## Jam's framing

Historically the likelihood function used JAX while visualization was
numpy-only. Visualization was recently switched to JAX too. The hypothesis:
under JAX, visualization obtains a different (broken) linear-algebra solution
than the likelihood function — some setting not threaded through, or a
JIT/precision/caching difference. Recent pytree-registration and
`cached_property` work around visualization may already have fixed it.

## What was investigated and RULED OUT (current checkout 2026.5.29.4)

The blow-up could **not** be reproduced post-hoc. All of these are healthy and
agree to ~1e-12:

- **Settings** — every toggle of the inversion `Settings`
  (`use_positive_only_solver`, `no_regularization_add_to_curvature_diag_value`,
  `use_edge_zeroed_pixels`, `use_border_relocator`, `use_mixed_precision`),
  including library defaults. Not a dropped setting.
- **numpy** path — healthy.
- **eager JAX** (`FitImaging(xp=jax.numpy)`, x64) — healthy, identical to numpy.
  This is *exactly* what the visualizer runs:
  `perform_quick_update`/`visualize` → `analysis.fit_for_visualization` →
  `fit_from` → `FitImaging(xp=jnp)`, which passes `settings=self.settings` and
  `xp=self._xp` identically to the likelihood path (`fit_for_visualization`
  just delegates to `fit_from`).
- **Warm JAX cache across instances** — warmed the process-global per-method JIT
  caches on a *different* instance (lens Einstein radius ×1.4 → genuinely
  different source-plane Delaunay geometry, verified), then evaluated the final
  instance. Still matches numpy to 2.75e-12. So the
  `_warmup_visualization()` (warms on `instance_from_prior_medians()`) →
  final-instance ordering does not, by itself, corrupt the result here.

Mechanisms checked and found *not to apply* in current code:
- **`pure_callback` constant-fold** (the Delaunay scipy triangulation in
  `@PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py` uses
  `jax.pure_callback`). This only bakes a constant under
  `jax.jit(...).lower().compile()` — and the visualization path **never** wraps
  the fit in jit/compile (`.lower().compile()` appears only in `print_vram_use`).
- **`cached_property` staleness** (the live-visual-update work added
  `cached_property` to fit classes). autoconf `cached_property` caches on the
  instance `__dict__`, and every quick_update/visualize builds a *fresh* fit via
  `instance_from_vector`, so nothing leaks between instances.

## Leading conclusion

Almost certainly **already fixed** by the recent pytree/JAX-visualization work,
OR the artefact requires a transient sampling state that the final saved
outputs don't capture (so it can't be reproduced from the end-of-run files).

## How to catch / confirm it next time

When it recurs on an HPC run:

1. Set `iterations_per_quick_update=None` (disables the warm-up at
   `@PyAutoFit/autofit/non_linear/fitness.py` ~line 172) **or**
   `PYAUTO_DISABLE_JAX=1` for visualization on a run that reproduces it. If
   `fit.png` then comes out healthy, the JAX visualization path is confirmed as
   the culprit.
2. Better: have the run dump, at the moment it blows up, the visualized
   instance's parameter vector **and** the `fit.fits`, so we capture the
   *actual* bad state rather than the final good one. Then feed that parameter
   vector into `z_help/sam/remake_fit.py` (build the tracer from it) and compare
   numpy vs JAX vs the search's compiled (`jax.jit(jax.vmap(fitness.call))`)
   path — the one path not yet exercised post-hoc.

## Reproduction harness

`z_help/sam/` (built during the investigation; self-contained, reloads the saved
result with no HPC dataset needed):
- `remake_fit.py` — rebuild the exact `FitImaging` from `files/tracer.json` +
  `image/*.fits`; `build_fit(settings=, xp=, mass_einstein_radius_scale=)`.
- `settings_stress_test.py` — sweep every inversion setting (numpy).
- `jax_test.py` — numpy vs eager JAX.
- `warm_jax_test.py` — warm JIT cache on instance A, evaluate final instance B.

Note: reloading a Delaunay+zeroed-edge-pixel fit from `tracer.json` is itself
broken — `Delaunay.__init__` does `pixels = int(pixels) + zeroed_pixels`, but
the JSON stores the resolved `zeroed_pixels` index array, so on reload `pixels`
becomes an array and `int(mesh.pixels)` crashes. `remake_fit.py` repairs this
(restore integer `pixels`/`_zeroed_pixels`, re-append the circle-edge points to
the saved Hilbert grid). Separate, smaller bug worth fixing on its own.
