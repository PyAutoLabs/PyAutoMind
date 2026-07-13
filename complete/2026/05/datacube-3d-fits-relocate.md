## datacube-3d-fits-relocate
- issue: none — direct followup to autolens_workspace#120
- completed: 2026-05-08
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/140 (3D-FITS layout + data_preparation.py + relocated likelihood_function.py)
  - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/51 (deletes the relocated likelihood walkthrough and prototype simulator)
- repos: autolens_workspace, autolens_workspace_developer
- notes: Hannah's ALMA visibilities arrive from CASA as a single 4D FITS (n_pol, n_chan, n_vis, 2). The original Phase 1 datacube tutorials only supported per-channel folders, which would have forced her to split her cube before loading. Updated simulator.py to additionally write `{visibilities,noise_map,uv_wavelengths}_cube.fits` at the cube root (each shape `(n_chan, n_vis, 2)`). New data_preparation.py walks through polarisation collapse (average vs concatenate) and ships a self-contained `dataset_list_from_3d_fits()` loader function — verified to match the per-channel-folder loader to rtol=1e-12. Also relocated the JAX likelihood walkthrough from the (private) autolens_workspace_developer to the (public) autolens_workspace so external collaborators can actually read it. Per-channel-folder layout kept for backward compatibility; both layouts coexist.
