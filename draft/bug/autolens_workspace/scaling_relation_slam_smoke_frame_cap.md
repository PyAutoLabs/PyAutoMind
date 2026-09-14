# scaling_relation/slam smoke failure: small-dataset cap crops two scaling-tier galaxies out of frame

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- workspace-smoke
- scaling-relation
Difficulty: easy
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: scripts/imaging/features/scaling_relation/slam.py runs green under the smoke profile (both legs, full_datasets declared) in < 300 s, every scaling-tier luminosity positive; guard message no longer mentions PYAUTO_TEST_MODE or no_run.yaml
Review-minutes: 10
Filed: 2026-09-14

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(follow-up "continue" → diagnose and fix the remaining Heart YELLOW reasons; plan approved 2026-09-14.)

## Context

Heart workspace-smoke cloud run 34824535982 fails `notebooks/imaging/features/scaling_relation/slam.ipynb`
with `ValueError: Measured luminosity is 0.0, but the scaling relation needs a positive value` while the
sibling `.py` passed in the same run. Diagnosis (read-only, 2026-09-14):

- Notebooks are regenerated from scripts in CI; code is identical. Both jobs installed the same numeric stack.
- Under `PYAUTO_SMALL_DATASETS=1` the 130x130 @ 0.1" simulator output becomes a 16x16 @ 0.6" frame
  (pixel centres ±4.5"). Two scaling-tier galaxies at (5.0, -1.0) and (-1.0, 5.0) fall outside it
  (image sum 7e-9). Their intensity is solved from noise; `use_positive_only_solver: true` clamps a
  non-positive draw to exactly 0.0. PyAutoArray documents this consequence of the cap
  (`autoarray/util/dataset_util.py:68-73`, PyAutoArray #430).
- `simulator.py:106` builds `al.SimulatorImaging(...)` with no `noise_seed`, and `dataset/` is gitignored,
  so each CI job simulates its own noise: a per-run lottery, not a regression. Runs 33378525604 (08-31) and
  34099198772 (09-07) executed the notebook and passed.
- The guard text in `slam.py` (`luminosity_from`, ~lines 27-33 and 101-110) blames PYAUTO_TEST_MODE and
  claims the script "is listed in config/build/no_run.yaml"; the park was removed 2026-08-29 (883d1e2f).

## Fix

1. Add a bottom-of-file `__Env__` docstring section to `scripts/imaging/features/scaling_relation/slam.py`
   declaring `ENV: full_datasets` (releases the cap for both legs; `_declaration_source_path` maps the
   notebook back to the script). Measured: 109 s wall at full resolution vs the 300 s smoke cap; every
   tier then sits far from the noise floor (anchor 2809, bounded 272/540, scaling 192/421/91/33/51).
2. Rewrite the guard message to name the frame cap and drop the PYAUTO_TEST_MODE / no_run.yaml sentences.
3. Regenerate the notebook per the workspace convention if the repo tracks generated notebooks.
Do not re-park in no_run.yaml; do not move the galaxy centres (changes the published example's geometry
and leaves (1.5, -4.5) at 65x below its peers as the next knife-edge).
