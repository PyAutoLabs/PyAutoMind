- summary: |
    Cleared the PyAutoHeart workspace-smoke failure on
    `notebooks/imaging/features/scaling_relation/slam.ipynb` (cloud run 34824535982, leg
    `run_notebooks (3.12, autolens, imaging)`), which raised
    `ValueError: Measured luminosity is 0.0, but the scaling relation needs a positive value`
    while the sibling `.py` passed in the same run. Under the smoke profile's
    `PYAUTO_SMALL_DATASETS=1` frame cap the simulated 130x130 @ 0.1" image is relabelled
    16x16 @ 0.6" (extent +/-4.8"), which puts the scaling-tier companions at (5.0, -1.0) and
    (-1.0, 5.0) outside the data; their MGE intensities are then linear-solved from noise and
    `use_positive_only_solver: true` clamps a non-positive draw to exactly 0.0, tripping the
    script's own luminosity guard. `simulator.py` passes no `noise_seed` and `dataset/` is
    gitignored, so every CI job draws its own noise - the clamp is a per-run lottery, not a
    regression (the same notebook passed in runs 33378525604 and 34099198772).
- shipped: |
    - `scripts/imaging/features/scaling_relation/slam.py` - bottom-of-file `__Env__`
      (Developer Only) section declaring `ENV: full_datasets`, releasing the frame cap for
      this script; `_declaration_source_path` maps the `.ipynb` back to the `.py`, so the one
      line also covers the notebook leg that actually failed.
    - The `luminosity_from` `ValueError` message and the docstring paragraph that echoes it
      rewritten to name the real cause (frame cap + positive-only solver) instead of the stale
      `PYAUTO_TEST_MODE` / `config/build/no_run.yaml` claim - that park was removed on
      2026-08-29 (883d1e2f) and `no_run.yaml` carries no `scaling_relation` entry today. The
      `raise` itself is unchanged.
    - `notebooks/imaging/features/scaling_relation/slam.ipynb` regenerated from the script
      (`generate.py autolens`); the `__Env__` section is stripped from the notebook by design.
- validation: |
    Control (capped, pre-declaration): five fresh draws all PASS (19-29 s), confirming the
    lottery diagnosis, but deterministically showing the knife-edge - the two out-of-frame
    companions measured 7.80e-05 and 7.01e-05 against truths of 1.494 and 1.086, four orders
    of magnitude below their in-frame peers. Witness (declaration honoured): script leg PASS
    77.0 s, notebook leg PASS 73.6 s, both simulating at (130, 130); every tier far from the
    noise floor. `validate_env_profiles.py` 0 errors / 0 warnings;
    `check_dataset_allowlist.py` OK; `check_sizes.sh` OK.
    CI on the merged head: Navigator Check (3 jobs), Smoke Tests (changes, smoke 3.12,
    smoke 3.13) and Script Size Guard - every run and every leg success.
- not-done: |
    The script is deliberately not re-parked in `no_run.yaml`, the galaxy centres are not
    moved (that would change the published example's geometry and leave the (1.5, -4.5)
    companion as the next knife-edge), and `simulator.py` is untouched (no `noise_seed`
    added).
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/545 (merge commit 4e367b6b)
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/544 (closed)

## Original prompt

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
Issued: 2026-09-14

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
