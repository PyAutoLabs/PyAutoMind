# HowToGalaxy small API drifts: ellipse kwargs + plot_grid_lines (parked NEEDS_FIX)

Type: bug
Target: howtogalaxy
Repos:
- HowToGalaxy
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Two independent, small stale-API call-sites in HowToGalaxy, both parked since 2026-04-10 and still
parked after the 2026-07-21 census:
- `ellipse/modeling` — `KeyError on 'ellipses.0.centre_0'` kwargs after API drift in ellipse modeling.
- `guides/advanced/over_sampling` — `plot_grid() got an unexpected kwarg 'plot_grid_lines'` after a
  plotter API change (find the current plotter kwarg name and update the call).

Reproduce each on clean main, update the call-sites (or the library if the drift was unintended),
remove both NEEDS_FIX markers from HowToGalaxy/config/build/no_run.yaml, regenerate notebooks.
Only edit scripts/, never notebooks/.
