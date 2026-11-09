# Fix plot_utils docstrings that call zero_contour the critical-curve default

Type: docs
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- critical-curves
- visualization
Difficulty: trivial
Autonomy: safe
Priority: low
Consequence: notify
Campaign: critical-curves
Filed: 2026-11-09

Found by autolens_profiling#521. `autogalaxy/util/plot_utils.py` docstrings for `_caustics_from` and `_critical_curves_from` say `"zero_contour"` is the default. The config default (`autogalaxy/config/visualize/general.yaml: critical_curves_method`) is `marching_squares`, and #521 recommends keeping it.

Change: mark `"marching_squares"` as the default in both docstrings. Say that `"zero_contour"` recompiles on every call today, and that its automatic seeds cover only ±3″ (it can miss group and cluster curves). Link the campaign wiki. No behaviour change.
