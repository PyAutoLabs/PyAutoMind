# Fix release-profile numerical inversion failures

## Context

Two interferometer scripts fail in inversion paths with non-positive-definite matrices.
The Autolens test failure reproduces on current `main`; the Autogalaxy script passed in a
stateful local checkout and needs a clean confirmation.

Owners: @PyAutoArray, @PyAutoGalaxy, @PyAutoLens, @autogalaxy_workspace, and
@autolens_workspace_test.

## Scripts

- `autogalaxy_workspace/scripts/interferometer/features/pixelization/galaxy_reconstruction.py`
- `autolens_workspace_test/scripts/interferometer/model_fit.py`

## Required work

1. Reproduce in clean output/worktrees with deterministic seeds and release settings.
2. Capture the curvature and regularization matrix properties at failure: symmetry,
   conditioning, eigenvalue range, dtype, backend, and mapper configuration.
3. Identify whether the defect is invalid sampled parameters, regularization construction,
   numerical stabilization, or a script model that permits an undefined inversion.
4. Fix the owning library for valid inputs. Do not catch `LinAlgError` or alter the script
   to hide a genuine inversion failure.
5. Add numerical regression tests and rerun both scripts repeatedly under the profile.
