# `subhalo/sensitivity/slam_source_parametric.py` fails: `'Model' object has no attribute 'centre'` in `base_model_narrow_priors_from`

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- subhalo
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: `scripts/imaging/features/advanced/subhalo/sensitivity/slam_source_parametric.py` runs to completion in test mode (`MPLBACKEND=Agg PYAUTO_TEST_MODE=2`).
Review-minutes: 10
Unattended: no
Lane: any
Filed: 2026-11-25

## Context

Found by the 5F PR2 worker. It fails on unedited HEAD too, at line ~786 in `base_model_narrow_priors_from`, with `AttributeError: 'Model' object has no attribute 'centre'`. It is likely an API drift in how a model component is read (a Model vs an instance). Coordinate with the `sensitivity_slam_source_pixelized_mappervalued` task, which owns the sibling `slam_source_pixelized.py`.
