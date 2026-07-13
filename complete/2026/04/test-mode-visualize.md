## test-mode-visualize
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/59
- completed: 2026-04-26
- workspace-pr:
  - https://github.com/PyAutoLabs/PyAutoBuild/pull/60
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/39
  - https://github.com/PyAutoLabs/autolens_workspace/pull/87
- notes: Workspace smoke runs of `fits_make.py` / `png_make.py` were silently producing no `.png` files even with `PYAUTO_SKIP_VISUALIZATION` unset. Root cause turned out to be `PYAUTO_FAST_PLOTS=1` (a smoke-runner default) short-circuiting `subplot_save` / `save_figure` in `autoarray/plot/utils.py` to `plt.close(fig); return` before any save. Fix: per-script env_vars override unsets both `PYAUTO_SKIP_VISUALIZATION` and `PYAUTO_FAST_PLOTS` for `fits_make` / `png_make` patterns, plus `n_like_max=300` cap on the three workflow scripts (csv_make / fits_make / png_make in both autogalaxy and autolens workspaces) so the Nautilus searches finish in seconds. PyAutoBuild side drops the `fits_make` / `png_make` skip entries from `no_run.yaml`. Pre-existing autogalaxy `imaging/start_here.py` smoke fail (missing `dataset/imaging/extra_galaxies/mask_extra_galaxies.fits`) is orthogonal — already broken on main, not caused by this task.
