# Interferometer Delaunay intermittent FitException (qhull NaN vertices + non-PD inversion)

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced 2026-07-21 while un-parking the Delaunay cluster (autolens_workspace#307, follow-up to
#300/#301). The **imaging** Delaunay is fixed and now smoke-gated; the **interferometer** Delaunay
is genuinely green *most* of the time but **flaky**: CI ran the identical commit (dce04672) twice and
py3.12 smoke FAILED on the push event with

    ValueError: Points cannot contain NaN   (scipy.spatial.Delaunay / qhull)
    [FAIL (exit 1)] interferometer/features/pixelization/delaunay.py

while PASSING on the pull_request event. Locally it passes 4/4 full-script runs and 20/20 random
prior-instance `fit_from` draws, so the failure rate is low (~1-in-N) and RNG/data/float-sensitive.

The old `(2,2) vs (1032,1032)` broadcast (the original 2026-04-10 symptom) is **gone** — this is a
distinct, intermittent NaN. It is currently parked in
`autolens_workspace/config/build/no_run.yaml` with an accurate note; HowToLens has no interferometer
Delaunay script.

## Hypothesis / where to look

A traced + border-relocated source-plane mesh vertex is occasionally NaN, which
`scipy.spatial.Delaunay` (qhull) rejects. The mesh vertices come from the image-plane `Overlay`
grid ray-traced by the mass model, then passed through `BorderRelocator`. Under
`PYAUTO_SMALL_DATASETS=1` the real-space mask is capped to 15x15, so heavily demagnified /
edge points near the mass centre may trace to inf/NaN for a small fraction of configs.

Likely loci:
- `PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py` — the `scipy.spatial.Delaunay`
  call (guard/clean NaN vertices, or fail loudly with a diagnostic).
- `PyAutoArray/autoarray/inversion/mesh/border_relocator.py` — relocation producing NaN.
- `PyAutoLens` tracing of demagnified points to NaN in the interferometer path.

## Two masked signatures — both surface as `FitException` (reconcile before fixing)

The `FitException` at `analysis.py:182` masks the true error (`analysis.py:175-182`, numpy path,
wraps ANY exception → `af.exc.FitException`; PR#607 parity guard so the sampler resamples). In
`TEST_MODE=2` there is no sampler, so a single bad-eval instance hard-fails the script. Two distinct
underlying errors have now been observed for this same script — determine whether they share one
root (a degenerate Delaunay mesh) or are independent:

1. **qhull NaN vertices (this prompt's CI evidence, autolens_workspace#307):** `ValueError: Points
   cannot contain NaN` from `scipy.spatial.Delaunay` — a traced/relocated source-plane mesh vertex
   is NaN, *before* the inversion. Intermittent (~50% CI py3.12, `dce04672`).
2. **non-PD / singular inversion (closed #309's diagnosis):** numpy cholesky raises where JAX
   NaN-resamples — a non-PD/singular matrix in the interferometer Delaunay inversion (candidate:
   `log_det_regularization_matrix_term` for `ConstantSplit` at fixed `coefficient=1.0`, or the
   linear solve). This is the interferometer tail of the pix-NaN lineage (imaging half resolved:
   autogalaxy_workspace#140, PyAutoArray#391/#392 opt-in `slogdet`).

**Prime-suspect debunk:** PyAutoArray#396 (SMALL_DATASETS grid even-cap 15→16) was already merged
(`656be94b`) and *in* the failing #307 CI run, so it does NOT fully fix this — the failure persists
with the even cap. (#308 closed the marker as "stale/green" on local runs; CI overturned that, and
the no_run entry stayed parked with an accurate intermittent-NaN note.)

## Fix tiers (from #309 — choose by what reproduction shows; do NOT silently swallow the FitException)

- **T1 workspace:** opt the script into `log_det_method="slogdet"` (already in `al.Settings`) —
  cleanest if the non-PD is the log-det term and slogdet yields finite; default path unchanged.
- **T2 PyAutoLens** (`interferometer/model/analysis.py`): make the `TEST_MODE` bypass tolerate a
  single-eval `FitException` as a resample signal (sentinel low FOM) instead of hard-failing.
- **T3 PyAutoArray:** if the `ConstantSplit` reg matrix is genuinely degenerate on the Delaunay
  mesh (zeroed edge points → exact-zero rows) or the mesh has NaN vertices, fix conditioning /
  the NaN at the producer.

## First step

Reproduce **both** signatures deterministically: run the interferometer Delaunay modeling fit many
times (or sweep many mass-model instances) under `PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1
PYAUTO_DISABLE_JAX=1` until (1) a NaN vertex and (2) a non-PD cholesky both appear; trace which
grid/relocation step introduces the NaN and whether the non-PD is the reg log-det or the solve.
Prefer fixing the producer (no silent None/NaN guards). Once robust, un-park the no_run entry and
add the script to the smoke gate (alongside the imaging Delaunay already added in #307).

Refs (all closed): autolens_workspace#300 (re-park), #307 (imaging added + interferometer kept
parked w/ CI flake evidence), #308 (drop-marker, closed), #309 (non-PD re-diagnosis, closed as dup).
Related: pixelization-inversion-not-PD, pix-NaN lineage (reg log-det slogdet fix).
