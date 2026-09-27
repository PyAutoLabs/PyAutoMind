# fnnls warm-start memo: stop it slowing scattered evaluation streams (interferometer CPU, autolens_profiling#332)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- interferometer
- numba-cpu
- nnls
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: on a recorded real-sampler evaluation sequence (Nautilus, alma Delaunay-1500 and rect 39², NumPy numba route), the memo-on fnnls solve is no slower than memo-off on every phase of the run (early live points and late phase), while keeping >= 80 % of the local-walk gain measured in #332 (rect solve 0.13×, Delaunay 0.68×); figure of merit unchanged (Δ 0 nat).
Review-minutes: 10
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

## Context

The NNLS passive-set memo is **on by default** (PyAutoArray `autoarray/config/general.yaml:12`,
#498). The positive-only solve seeds from the previous evaluation's final passive set
(`autoarray/inversion/inversion/nnls_memo.py`; used in `reconstruction_positive_only_from`,
`autoarray/inversion/inversion/inversion_util.py:291`).

autolens_profiling#332's lever arm (`levers.memo` in
`results/breakdown/interferometer/{delaunay,pixelization}_numba_hpc_ral_cpu_fp64_levers.json`,
alma r3.5, 16 instances per stream) measured:

| Stream | Delaunay solve off → on | rect solve off → on |
|---|---|---|
| local walk (unit step 0.002) | 163 → 111 ms (0.68×) | 324 → 41 ms (**0.13×**) |
| iid (central 20 % of each prior) | 164 → 356 ms (**2.17× slower**) | 329 → 356 ms (1.08× slower) |

The solve is 17 % (Delaunay) / 22 % (rect) of the alma call, and 54 % / 76 % at sma. So the memo is
worth −15 % of the rect call on a walk, but +15 % on the Delaunay call on an iid stream.

The fallback guard (`inversion_util.py:598-630`) judges a seed only **after** the seeded solve has
run. It drops the entry when `error_fraction > nnls_warm_start_error_tolerance ×
dense_error_fraction`. The next solve restarts dense and re-seeds, so on a scattered stream about
every other solve pays for a bad seed.

## What

1. Record the evaluation sequence (unit vectors) of a short Nautilus run on the alma interferometer
   Delaunay / rect models. Replay it through the #332 harness's memo lever
   (`_lever_memo`, `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`), phase by
   phase.
2. If the iid-phase regression reproduces, prototype in-cell (no library edit) two guards and
   measure both on the replay:
   - a pre-solve seed check (e.g. KKT residual of the seed on the new system);
   - a per-key back-off after k consecutive fallbacks.
3. Report the imaging HST Delaunay control too (the #498 fiducial), so the fix does not undo the
   imaging gain.
4. If a guard wins, draft the PyAutoArray change.

## Out of scope

The JAX solvers (memo is NumPy-only).
