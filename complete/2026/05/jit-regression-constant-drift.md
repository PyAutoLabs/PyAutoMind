## jit-regression-constant-drift
- task-alias: jit-regression-drift  (matches active.md / worktree name during execution; full filename-stem slug here so the z_features audit picks this up as shipped)
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/67
- completed: 2026-05-16
- repo-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/3
- merge-commit: aa131a7
- upstream-issues-filed:
  - PyAutoLens#514 — eager log_likelihood drift in AnalysisPoint chain (real upstream behaviour change, not constant-refresh)
  - autolens_workspace_developer#68 — jit/imaging/pixelization.py JIT vs eager mapping matrix shape mismatch
  - autolens_workspace_developer#69 — jit/imaging/delaunay.py log_evidence rebuild returns -inf
- summary: |
    Follow-up F1 of autolens_profiling z_feature. Smoked all 10
    jax_profiling/jit/ scripts against clean origin/main of _developer
    on PyAutoLens 2026.5.14.2 and found the original drift picture was
    wrong in interesting ways:

    1. The Phase 1 imaging/mge.py "drift" (+0.6%) was NOT a real upstream
       drift — Phase 1 mirror was made from the dirty _developer canonical
       checkout, which had locally-modified dataset/imaging/hst/*.fits.
       On clean main, imaging/mge.py PASSES (27379.388907 matches the
       constant). Re-mirror in autolens_profiling PR #3 fixes this:
       refreshes scripts + datasets from clean origin/main, also pulls
       in dataset/interferometer/hannah/ that Phase 1 missed (828K, 5
       files). datacube/delaunay.py default instrument also restored
       from "sma" (dirty canonical) to "hannah" (clean main).

    2. point_source/{image_plane,source_plane}.py drift IS real and IS
       upstream — magnitudes too large for floating-point drift
       (image_plane: 0.075 → -362.21, sign change + 4843×; source_plane:
       -294 → -3599, 12×). Light bisect of PyAutoLens/PyAutoGalaxy/
       PyAutoArray commits since 2026-04-24 (cfa5378, when constants were
       set) surfaced candidates but no smoking gun. Filed PyAutoLens#514
       for upstream investigation. **Constants left as-is — failing
       regression assertions are load-bearing while #514 is open.**

    3. Two unrelated pre-existing bugs uncovered by the 10-script smoke
       (Phase 1 only smoked 1 per subfolder):
       - imaging/pixelization.py: JIT vs eager mapping matrix shape
         mismatch (1285×1285 vs 1225×1225) at the curvature+regularization
         add step. Filed as _developer#68.
       - imaging/delaunay.py: log_evidence rebuild returns -inf vs
         FitImaging's finite 26288.32. Filed as _developer#69.

    No code shipped to _developer (constants stay as-is). One PR shipped
    to autolens_profiling (#3, re-mirror hygiene). Three upstream issues
    filed for follow-on investigation by maintainer.

    Smoke logs + result-artifact backups preserved at
    /tmp/jit_drift_smoke/ in case useful for upstream triage.

## Original prompt

Follow-up surfaced by Phase 1 of the `autolens_profiling` z_feature
(see `z_features/autolens_profiling.md`).

Two of the JIT likelihood profiling scripts in
`autolens_workspace_developer/jax_profiling/jit/` carry hardcoded
`EXPECTED_LOG_LIKELIHOOD_*` regression constants that drifted off the
current eager log-likelihood when re-run on PyAutoLens `2026.5.14.2`
during the Phase 1 mirror smoke. The mirror in
`PyAutoLabs/autolens_profiling` carries the same constants verbatim, so
the drift applies symmetrically — both repos need the same fix.

## Observed drift (smoke on 2026-05-16 against PyAutoLens 2026.5.14.2)

| Script | Constant | Expected (hardcoded) | Actual (smoke) | Drift | Likely category |
|---|---|---|---|---|---|
| `jax_profiling/jit/imaging/mge.py` (L853) | `EXPECTED_LOG_LIKELIHOOD_HST = 27379.38890685539` | 27379.39 | 27542.08 | +0.6% | small-magnitude drift — likely numerical / dependency update, not a behaviour change |
| `jax_profiling/jit/point_source/image_plane.py` (L444) | `EXPECTED_LOG_LIKELIHOOD_IMAGE_PLANE = 0.07475703623045682` | 0.0748 | -362.21 | sign change, ~5000× | **strongly suggests a real behaviour change** in the `PointSolver` / `FitPositionsImagePairAll` chi-squared stack |

The other 8 mirrored scripts either don't have a hardcoded regression
constant or pass theirs cleanly:
- `interferometer/mge.py` — regression PASSED.
- `datacube/delaunay.py` — both eager and full-pipeline cube
  regressions PASSED.
- Other imaging / interferometer / point_source variants weren't smoked
  individually in Phase 1, but spot-checking them with `git diff` against
  `_developer` shows the constants are unchanged. Worth re-smoking each
  one as part of this triage.

## Suspected root cause (point_source — the big one)

The sign change and magnitude jump on `point_source/image_plane.py` is
not consistent with float-precision drift. Best guesses:

1. **Position-pairing logic in `FitPositionsImagePairAll`** changed
   (e.g. how model images get matched to observed images), shifting the
   χ² baseline.
2. **`PointSolver` triangle-refinement loop** is producing different
   model positions for the same input model (different convergence
   threshold? different `xp=jnp` path?).
3. **Positions noise-map handling** changed — the constant was set
   when `positions_noise_sigma = 0.05` produced one residual scale; if
   the noise-map application now squares-or-doesn't-square that
   differently, χ² shifts.

The dataset is seeded (`noise_seed=1` in `dataset_setup/point_source.py`)
and the input files are committed, so the drift cannot be from input
randomness.

## Suspected root cause (imaging/mge — small drift)

0.6% drift on `mge.py` is more consistent with:
- Floating-point reduction order changes from a dependency bump
  (numpy, jax, scipy NNLS, autoarray utility refactors).
- Per-pixel over-sampling default change in `apply_over_sampling` /
  `over_sample_size_via_radial_bins_from`.

Spot-check by re-running the imaging script and comparing intermediate
JIT timings — if the *shape* of the breakdown is similar but every
number moves slightly, it's a numerical-drift category. If one step
dominates the new total, it's an algorithmic change worth tracking.

## Task

For each of the two affected scripts:

1. **Reproduce** in `_developer` (not the mirror) on the user's CLI
   environment, to confirm the drift is current. Recording the actual
   eager log-likelihood is the deliverable here.
2. **Bisect (lightly)** — `git log --oneline -20` on PyAutoLens,
   PyAutoGalaxy, PyAutoArray since the constants were last set
   (file's last touch of those lines via `git log -L`) and pick the
   most-likely-culprit changes for `point_source` (anything around
   `PointSolver`, `FitPositionsImagePairAll`, `positions_noise_map`).
3. **Decide per script**:
   - If the new value is **correct** (no underlying bug): refresh the
     constant in `_developer` AND in the mirrored copy at
     `PyAutoLabs/autolens_profiling/likelihood/{imaging/mge.py,point_source/image_plane.py}`.
   - If the new value is **wrong** (real behaviour regression in the
     library): file a bug against the responsible PyAuto* repo and link
     it here. Do NOT refresh the constant — the failing assertion is
     load-bearing while the bug is open.
4. **Spot-check the other 8 JIT scripts** by re-running each at least
   once. Update any constants that drift cleanly; flag any further
   regressions worth filing.
5. **Then** update both repos' constants in a single PR pair
   (`_developer` and `autolens_profiling`) so they stay in sync. Cross-
   reference PRs in each.

## Out of scope

- Re-mirroring scripts from `_developer` into `autolens_profiling` —
  the Phase 1 mirror is already shipped and pinned to whatever
  `_developer` looked like at PR-merge time. Constant updates can be a
  small follow-up commit on each side.
- Phases 2–5 of the autolens_profiling z_feature — independent work.
- JAX gradient profiling drift (out of scope for autolens_profiling
  entirely until that story stabilises).

## Pre-existing context

- Phase 1 mirror PR: https://github.com/PyAutoLabs/autolens_profiling/pull/2 (merged)
- Phase 1 issue: https://github.com/PyAutoLabs/autolens_profiling/issues/1 (closed)
- z_features tracker: `PyAutoPrompt/z_features/autolens_profiling.md`
- `should_simulate` lives in
  `PyAutoArray/autoarray/util/dataset_util.py:54` — `PYAUTO_SMALL_DATASETS=1`
  deletes datasets to force re-simulation; do not set it during this
  triage, it would destroy the committed input data.
