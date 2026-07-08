# Oversampled PSF convolution — phase 3: workspace tests + simulator example

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 of 4 of `feature/autoarray/oversampling.md`. Depends on the phase-2
library PRs — all merged or open as of 2026-07-08: 2a PyAutoArray#355
(merged), 2b PyAutoArray#357 (merged), 2c PyAutoGalaxy#481 (includes linear
light profile support via `operated_mapping_matrix_override`). **Start only
after #481 merges** (the light-profile and linear-light legs need it).

## Scope

1. **Numerical test**: extend
   `@autolens_workspace_test/scripts/imaging/convolution.py` with a numerical
   test of oversampled PSF convolution.
2. **Ground-truth test file**: build on that in a separate test script using a
   simple oversampled PSF, asserting the source code reproduces the phase-1
   numerical ground truth (`oversampling_design.md` §7 reference values).
3. **Coverage across all supported model surfaces** (user requirement,
   2026-07-08) — each fitted at `convolve_over_sample_size=2` through the full
   `FitImaging` flow, with s=1 parity checks:
   - **standard light profiles** (2c consumer switch),
   - **linear light profiles** (`operated_mapping_matrix_override` fine path),
   - **operated light profiles** (added at image resolution, unblurred — by
     definition; assert unchanged behaviour alongside blurred components),
   - **pixelized sources** via the mapping formalism (2b wiring; rectangular
     + delaunay). Also assert the loud-guard surfaces: sparse formalism
     (`sparse_operator`), the `data_linear_func_matrix` preload, and adaptive
     over sampling all raise under an oversampled PSF.
4. **Simulator example**: extend
   `@autolens_workspace/scripts/imaging/simulator.py` to show how to use
   oversampled PSFs in a real simulation.

## Notes

- Uniform over sampling only — adaptive sub-sizes are out of scope (the
  library raises on that combination; the example should say so briefly).
- Check `.gitignore` covers any new output/image directories before shipping
  (pre-flight `git diff --stat` for binary leaks).
- Mirror any new library config keys into the workspace configs if phase 2
  introduced them.

## Acceptance

- Both test scripts run clean against the phase-2 branches and pass.
- Simulator example runs end-to-end and its prose explains the
  `convolve_over_sample_size` choice.
- Workspace PR sits behind the library-first merge gate (phase-2 PR merges
  first).

Parent: `feature/autoarray/oversampling.md`.
Previous: `oversampling_phase_2_core_api.md`. Next: `oversampling_phase_4_docs.md`.
