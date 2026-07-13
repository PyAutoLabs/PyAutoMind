## datacube-centre-and-4d
- issue: none — direct followup to autolens_workspace#120
- completed: 2026-05-14
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/148
- repos: autolens_workspace
- notes: Two polish items on top of the datacube tutorials. (1) Source centre now shifts linearly along y across channels (CENTRE_SHIFT_TOTAL = 0.12" end-to-end) to mimic a kinematic gradient; centres land at (0.04, 0.1), (0.08, 0.1), (0.12, 0.1), (0.16, 0.1) for the 4-channel reference cube. (2) Simulator now writes a third on-disk layout: a 4D CASA-like cube `{visibilities,noise_map,uv_wavelengths}_4d_cube.fits` of shape `(n_pol, n_chan, n_vis, 2)` matching what CASA gives users straight out of reduction. Polarisations are identical in the synthetic simulator (documented as pedagogical simplification). data_preparation.py now loads the simulator's actual 4D output rather than synthetic random arrays. README documents all three layouts (CASA-like 4D / 3D cube / per-channel folders).
