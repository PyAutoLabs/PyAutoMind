## howto-tutorial-release-fixes
- issue: https://github.com/PyAutoLabs/HowToLens/issues/15
- completed: 2026-06-09
- workspace-prs:
  - https://github.com/PyAutoLabs/HowToGalaxy/pull/12 (merged 0605b56)
  - https://github.com/PyAutoLabs/HowToLens/pull/16 (merged 3ae228b)
- repos: HowToGalaxy, HowToLens
- notes: Fixed the unblocked HowTo tutorial release failures. HowToGalaxy's mapper tutorial now selects valid mapper pixel indexes dynamically for both full and small release datasets. HowToLens filters non-finite traced source-plane coordinates before plotting and keeps the intentionally bad annular mask non-empty under `PYAUTO_SMALL_DATASETS=1`. Verified targeted scripts, PyAutoBuild sections for HowToGalaxy chapter 4 and HowToLens chapters 1 and 2, and PR CI before merge.

## Original prompt

# HowTo Tutorial Release Fixes

## Original Request

ok, next fixes?

do it

## Context

After fixing and merging the first latent/JAX release failure group, the next unblocked release group is the HowTo tutorial failures. The Autofit database scrape group was rerun against the current stack and both scripts now pass, so it does not need an active fix.

## Failures

- `HowToGalaxy/scripts/chapter_4_pixelizations/tutorial_2_mappers.py`
  - `IndexError: list index out of range` in `mapper.slim_indexes_for_pix_indexes(...)`.
- `HowToLens/scripts/chapter_1_introduction/tutorial_3_more_ray_tracing.py`
  - `ValueError: Axis limits cannot be NaN or Inf` while plotting the traced source-plane grid.
- `HowToLens/scripts/chapter_2_lens_modeling/tutorial_6_masking_and_positions.py`
  - `ValueError: zero-size array to reduction operation minimum which has no identity` when applying a mask.

## Scope

Fix the tutorial scripts in `HowToGalaxy` and `HowToLens` so the release build scripts pass without touching the active Kaplinghat task or `autolens_workspace_test`.
