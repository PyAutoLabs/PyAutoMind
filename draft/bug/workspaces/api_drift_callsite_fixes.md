# Workspace API-drift call-site fixes (kwargs / Prior / interpolator / plotter) (parked NEEDS_FIX)

Type: bug
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- autolens_workspace_test
- HowToGalaxy
- HowToLens
- HowToFit
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

A set of independent "script uses stale API after a library change" NEEDS_FIX markers. Each is a
targeted call-site (or small library) fix; some pairs share one bug across repos. Reproduce each on
clean main; remove its NEEDS_FIX marker when green. Split into separate PRs if they touch different libs.

- **InstanceInterpolator IndexError** (likely a PyAutoFit bug, not just call-site): autofit_workspace `features/interpolate` (__getitem__ at time==1.5) + HowToFit `chapter_1_introduction/tutorial_5_results_and_samples` (same family).
- **`ell_comps` kwargs KeyError** on `('galaxies','galaxy','bulge','ell_comps'...)`: autogalaxy_workspace `imaging/modeling` + HowToGalaxy same.
- **ellipse kwargs KeyError** `'ellipses.0.centre_0'`: HowToGalaxy `ellipse/modeling`.
- **plotter kwarg drift** `plot_grid() unexpected 'plot_grid_lines'`: HowToGalaxy `guides/advanced/over_sampling`.
- **group/slam PriorException** (upper<=lower): autolens_workspace `group/slam` + HowToLens `group/slam`.
- **`__hash__` returns non-int TypeError** in `linear_light_profile_intensity_dict` during subplot: autolens_workspace_test `database/scrape/general` (PyAutoGalaxy light-profile __hash__).

First step: triage the interpolator one first (library, 2 repos) — likely the highest-value single fix.
