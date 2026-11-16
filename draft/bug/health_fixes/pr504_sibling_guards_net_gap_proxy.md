# Harden the sibling PR #504 non-vacuity guards (net fom−logL gap proxy)

Type: bug
Target: autolens_workspace_test
Repos: @autolens_workspace_test @autogalaxy_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-11-11
Lane: any

Split out of autolens_workspace_test#362 (the corrective fix to
`scripts/interferometer/model_fit.py`). These scripts carry the same "within 1
nat … log-det terms are zero" guard wording and may use the same net-gap
proxy, which crossed zero for the interferometer script after PyAutoArray#683:

- autolens_workspace_test: `scripts/imaging/model_fit.py`,
  `scripts/imaging/visualization/modeling_visualization_delaunay_jit.py`,
  `scripts/imaging/visualization/modeling_visualization_rectangular_jit.py`
- autogalaxy_workspace_test: `scripts/imaging/visualization/visualization.py`

They pass today. Check each; where it uses the net gap, assert the inversion's
log-det terms directly, matching #362. Ideally share one helper.
