# Interferometer Delaunay intermittent "Points cannot contain NaN" (qhull triangulation)

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

## First step

Reproduce the intermittent NaN deterministically: run the interferometer Delaunay modeling fit many
times (or sweep many mass-model instances) under `PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1
PYAUTO_DISABLE_JAX=1` until a NaN vertex appears, then trace which grid/relocation step introduced
the NaN. Decide guard-and-clean vs. fix-the-producer (prefer fixing the producer — no silent
None/NaN guards). Once robust, un-park the no_run entry and add the script to the smoke gate
(alongside the imaging Delaunay already added in #307).

Related: pixelization-inversion-not-PD, pix-NaN lineage (reg log-det slogdet fix).
