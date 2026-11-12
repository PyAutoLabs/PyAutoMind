# Cluster figures miss small member-galaxy critical curves

Type: research
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_profiling
Themes:
- critical-curves
- cluster
- visualization
Difficulty: small
Autonomy: supervised
Priority: low
Consequence: judge
Campaign: critical-curves
Filed: 2026-11-09
Lane: any

Found by autolens_profiling#521 (RAL 414456). Cluster point-source figures draw curves with `autolens/point/plot/point_sources.curves_for_planes`: a 400² grid (`CURVE_GRID_SHAPE`) over the ±50″ solver extent, so 0.25″ spacing. Against a 1600² reference, it misses the small member-galaxy tangential critical curves on the nearer source plane in every phase-4 posterior draw (11 of 22 plane-draws fail; the main curves match within 0.15″). It takes 0.11–0.13 s per figure.

Question: should figures show those member curves? If yes, decide how. Options: a finer grid only near member galaxies, a zoomed second pass around each member centre, or a larger `CURVE_GRID_SHAPE`, judged by cost per figure against the #521 harness (`modeling_viz_feasibility_scales.py`, cluster branch). If no, document that member curves below the grid resolution are not drawn. No change until the human rules.
