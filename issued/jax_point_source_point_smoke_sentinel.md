Smoke regression surfaced during the `fast-viz-zero-contour-perf` task
(workspace PR https://github.com/PyAutoLabs/autolens_workspace_test/pull/111).

`autolens_workspace_test/scripts/jax_likelihood_functions/point_source/point.py`
fails its hardcoded `assert_allclose(np.array(result), -83.38049778, rtol=1e-4)`
check on canonical `main` of all three libraries — `fitness._vmap(parameters)`
returns the `-1e99` sentinel (the chi-squared "non-finite likelihood" reject
value used by `FitPositionsImagePairAll`) instead of the expected -83.38.

Reproduces identically on canonical main with no workspace-PR changes applied,
so this is a library-side regression, not anything from the current task.

## Observed symptom

| Script | Expected (hardcoded) | Actual (vmap) | Notes |
|---|---|---|---|
| `jax_likelihood_functions/point_source/point.py` (L234-239) | `-83.38049778` | `-1e99` (sentinel) | Pre-existing on `main` 2026-05-21 |

The -1e99 value is the standard `FitPositionsImagePairAll` sentinel for
"position-pairing rejected this model" — the JAX vmap path is treating every
sampled parameter set as a reject, which means either every position is
failing to be paired or every solver call is returning `inf`/`nan` rows.

## Last known good

The literal `-83.38049778` was set on **2026-05-08** in
`autolens_workspace_test@362cfa8` ("rebaseline JAX point-source likelihood
literals after noise-scale change"). At that commit the smoke passed
end-to-end against the libraries-of-the-day. Something in PyAutoLens /
PyAutoGalaxy / PyAutoArray between 2026-05-08 and 2026-05-21 has broken the
JAX vmap path through `FitPositionsImagePairAll` for the seed point-source
dataset committed under `dataset/point_source/simple/`.

## Relationship to PyAutoLens#514

`PyAutoPrompt/issued/jit_regression_constant_drift.md` already tracks a
drift in `autolens_workspace_developer/jax_profiling/jit/point_source/image_plane.py`
filed as https://github.com/PyAutoLabs/PyAutoLens/issues/514. That ticket
exercises the **same JAX code path** (`PointSolver` + `FitPositionsImagePairAll`)
but a different symptom (constant drifted 0.07 → -362, not a -1e99 sentinel)
on a different file (the profiling script in `_developer`, not the smoke
script in `_test`).

Two hypotheses worth holding in tension during triage:

1. **Same root cause, different manifestation.** A change in `PointSolver`
   triangle refinement or `FitPositionsImagePairAll` position-pairing could
   produce a drifted-but-finite value on `image_plane.py`'s seeded inputs
   and a clean-reject sentinel on `point.py`'s seeded inputs, if the latter
   is closer to a pairing-threshold edge case. If so this prompt and #514
   resolve together.
2. **Two independent regressions.** The -1e99 sentinel is qualitatively
   different from a sign-flip drift — it could be a separate JAX-path bug
   (e.g. a tracer-typed quantity being compared with a NumPy threshold,
   forcing the whole batch into the reject branch). If so this needs its
   own library-side fix.

Either way the symptom is severe enough to warrant a separate triage line.

## Task

1. **Reproduce** on canonical main of all three libraries:
   ```bash
   cd ~/Code/PyAutoLabs/autolens_workspace_test
   git checkout main && git pull --ff-only
   git -C ../PyAutoLens checkout main && git -C ../PyAutoLens pull --ff-only
   git -C ../PyAutoGalaxy checkout main && git -C ../PyAutoGalaxy pull --ff-only
   git -C ../PyAutoArray checkout main && git -C ../PyAutoArray pull --ff-only
   python scripts/jax_likelihood_functions/point_source/point.py
   ```
   Confirm the AssertionError and capture the actual vmap output.

2. **Bisect across the three libraries** since 2026-05-08:
   ```bash
   git -C ../PyAutoLens   log --oneline --since=2026-05-08 -- autolens/point/
   git -C ../PyAutoLens   log --oneline --since=2026-05-08 -- autolens/analysis/
   git -C ../PyAutoGalaxy log --oneline --since=2026-05-08
   git -C ../PyAutoArray  log --oneline --since=2026-05-08
   ```
   Prime suspects (matching the #514 candidate-list):
   - `PointSolver.solve` and the triangle-refinement loop
   - `FitPositionsImagePairAll` chi-squared assembly
   - Anything touching `positions_noise_map` application or `xp`
     propagation through the point-source stack

3. **Diagnose where -1e99 enters.** Drop a `jax.debug.print` (or eager
   NumPy-path run) inside `FitPositionsImagePairAll.log_likelihood_function`
   to see whether:
   - every pair distance is `inf`/`nan` (solver returning bad positions);
   - the pair-permutation `argmin` is selecting the wrong index;
   - the χ² → log-likelihood reduction is hitting an inf/nan that triggers
     the sentinel branch.

4. **Decide per finding**:
   - If the new behaviour is **a library bug** → file against the responsible
     PyAuto* repo, cross-reference both this prompt and #514, leave the smoke
     literal as-is (the failing assertion is load-bearing while the bug is
     open).
   - If the new behaviour is **a deliberate change** (noise-map convention,
     pairing semantics) → rebaseline the literal in `point.py`. Also re-run
     `image_plane.py` and `source_plane.py` from `jax_likelihood_functions/point_source/`
     since they share the seed dataset and may need matching updates.

5. **Spot-check the sibling JAX smoke scripts** in
   `autolens_workspace_test/scripts/jax_likelihood_functions/point_source/`
   (`image_plane.py`, `source_plane.py`) — they share the seed dataset and
   may exhibit the same regression, in which case the fix is unified.

## Out of scope

- Re-running the full `autolens_workspace_test` smoke suite — only the
  three point-source JAX scripts need verifying for this triage.
- The constant drift in `autolens_workspace_developer/jax_profiling/jit/point_source/image_plane.py`
  tracked by #514 — share findings, but don't expand this prompt into that
  one. Update #514 with whatever the bisect surfaces.
- Regenerating the seed dataset under `dataset/point_source/simple/` — the
  files are committed, the literals were set against them on 2026-05-08, so
  the dataset is *not* the moving variable here. Do not run
  `PYAUTO_SMALL_DATASETS=1` during triage — it would delete the committed
  seed data.

## Pre-existing context

- Last known-good rebaseline: `autolens_workspace_test@362cfa8` (2026-05-08)
- Related JIT profiling drift: `PyAutoPrompt/issued/jit_regression_constant_drift.md` → PyAutoLens#514
- Smoke philosophy: workspace `scripts/CLAUDE.md` documents that the
  hardcoded literals in `jax_likelihood_functions/` are intentional
  absolute-regression markers — don't relational-rewrite them away.
- Surfaced by: workspace PR https://github.com/PyAutoLabs/autolens_workspace_test/pull/111
  (fast-viz-zero-contour-perf), noted in that PR body.
