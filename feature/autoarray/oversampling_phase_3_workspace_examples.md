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
library PR (`oversampling_phase_2_core_api.md`) — start from its
`## API Changes` summary and run against the phase-2 worktree branches.

## Scope

1. **Numerical test**: extend
   `@autolens_workspace_test/scripts/imaging/convolution.py` with a numerical
   test of oversampled PSF convolution.
2. **Ground-truth test file**: build on that in a separate test script using a
   simple oversampled PSF, asserting the source code reproduces the phase-1
   numerical ground truth.
3. **Simulator example**: extend
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
