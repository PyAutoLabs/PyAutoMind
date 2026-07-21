# SersicCore ZeroDivisionError on effective_radius=0 (numpy scalar-division robustness)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Split out from `slam-adapt-inversion-cascade` (autolens_workspace#300). Originally suspected as an
`alpha=0` bug; diagnosis (2026-07-21) proved otherwise — see below.

## Reproduction (clean main, real CI smoke env)

```
cd autolens_workspace
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
PYAUTO_DISABLE_JAX=1 PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_SKIP_FIT_OUTPUT=1 \
PYAUTO_SKIP_VISUALIZATION=1 PYAUTO_SKIP_CHECKS=1 PYAUTO_FAST_PLOTS=1 \
python scripts/multi/features/wavelength_dependence/modeling.py
```

Fails with `ZeroDivisionError: float division by zero` at
`PyAutoGalaxy/autogalaxy/profiles/light/standard/sersic_core.py:68` (`intensity_prime`).

## Root cause (corrected — NOT alpha)

`alpha` is `3.0` at runtime (Constant prior; verified via probe). The real division that raises is
`... / self.effective_radius` with **`effective_radius == 0.0`** (Python attributes the error to the
enclosing line 68). Two facts combine:

1. **Library:** `SersicCore.intensity_prime` computes a **Python scalar** and divides it with a plain
   `/`: `((2.0 ** (1.0 / self.alpha)) * self.radius_break) / self.effective_radius`. A scalar
   `float / 0.0` **raises `ZeroDivisionError`**. Every other profile (e.g. `Sersic.image_2d_via_radii`,
   `sersic.py:99/157`) divides a **numpy array** by `effective_radius`, which yields `inf` (a
   RuntimeWarning, then a resample) rather than crashing. `SersicCore` is the odd one out — same
   numpy-vs-jax raise-vs-resample lineage as PyAutoLens#607.
2. **Trigger:** the multi-wavelength model sets `effective_radius = wavelength*m + c` with
   `m ~ Uniform(-0.1, 0.1)` and `c ~ Uniform(-10, 10)` — both symmetric about 0 — so the test-mode
   **median instance** gives `m=0, c=0 → effective_radius=0`. (The script's own illustrative
   `source_effective_radius_from` uses `c=10`; the prior is centred on 0.)

## Chosen fix (approved): library robustness

Make `SersicCore.intensity_prime` divide via `xp` (`xp.divide(...)`) so `effective_radius <= 0` yields
`inf`/`nan` (which the sampler resamples) instead of a hard `ZeroDivisionError` — consistent with every
other profile and with the JAX path. This fixes the test-mode crash AND real-fit robustness for all
`SersicCore` uses, not just this one example. Thread `xp` (already the function's parameter). Not a
silent guard: it produces the same non-finite → resample signal the rest of the profile system uses.

- **Library (PyAutoGalaxy):** `profiles/light/standard/sersic_core.py` `intensity_prime` — `/` → `xp.divide`.
  Add a numpy-only unit test (`test_autogalaxy/.../test_sersic_core.py`): `SersicCore(effective_radius=0.0)`
  `intensity_prime()` returns non-finite (no raise). (Unit tests are numpy-only per repo rules.)
- **Workspace follow-up (autolens_workspace):** re-run `multi/features/wavelength_dependence/modeling`
  green under the smoke env, then drop its `# NEEDS_FIX` line from `config/build/no_run.yaml`.

HowToLens has **no** wavelength_dependence tutorial — the original prompt's HowToLens reference is a
dead path; no HowToLens change.
