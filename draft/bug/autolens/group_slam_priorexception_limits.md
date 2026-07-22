# group/slam PriorException: upper limit must be greater than lower limit (SUPERSEDED)

Type: bug
Target: autolens
Repos:
- autolens_workspace
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: superseded

SUPERSEDED 2026-07-22 by `draft/bug/autoarray/small_datasets_loader_pixel_scales.md`.
Do not start work from this file.

This prompt assumed the fault was a collapsed/inverted prior in the group SLaM pipeline,
in `autolens_workspace` and `HowToLens`. It is not. The root cause is in **PyAutoArray**:
`cap_array_2d_for_small_datasets` early-returns for data already at-or-below the 16x16
`PYAUTO_SMALL_DATASETS` cap, keeping the caller's uncapped `pixel_scales` (0.1) even though
a capped simulator wrote that data at 0.6. The frame is mislabelled 6x, the extra galaxies
fall outside it, their non-negative linear intensity solve correctly returns exactly 0.0,
and the `UniformPrior` upper limit collapses to 0.0. The `PriorException` is four steps
downstream of the fault.

Corrections to the assumptions recorded above:

- The prior construction and the group SLaM science are **correct**; no workspace script
  change is needed. `pixel_scales=0.1` is a true statement about the dataset in normal
  operation and belongs in a tutorial script.
- `HowToLens` has **no** `group/` scripts at all — its `no_run.yaml` entry is dead config.
- The only workspace work left is removing the `group/slam` NEEDS_FIX line from
  `autolens_workspace/config/build/no_run.yaml` and the dead one from
  `HowToLens/config/build/no_run.yaml`. Both are carried in the superseding prompt.
