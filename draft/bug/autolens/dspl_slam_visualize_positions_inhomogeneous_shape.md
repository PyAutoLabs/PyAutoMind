# Double-source-plane SLaM fails in `visualize_before_fit`: `image_with_positions` gets inhomogeneous multi-plane positions

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- visualization
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: `scripts/{imaging,group}/features/advanced/double_source_plane_lens/slam.py` in autolens_workspace run to completion in test mode (`MPLBACKEND=Agg PYAUTO_TEST_MODE=2`). `autolens/analysis/plotter.py` `image_with_positions` handles positions from several planes (ragged lists) without `ValueError: setting an array element with a sequence … inhomogeneous shape`. Includes a unit test with ragged multi-plane positions.
Review-minutes: 15
Unattended: no
Lane: any
Filed: 2026-11-25

## Context

Found by the 5F PR2 worker (autolens_workspace#688). It fails on unedited HEAD too, so it is pre-existing. The error is raised from `PyAutoLens/autolens/analysis/plotter.py:100 image_with_positions` in `visualize_before_fit` of stage `source_pix_1_source_1`, where multi-plane positions reach the visualizer. These scripts are excluded from smoke, which is why it went unnoticed.
