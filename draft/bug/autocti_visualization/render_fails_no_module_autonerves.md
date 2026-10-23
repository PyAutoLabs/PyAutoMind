# autocti_visualization render.yml fails: No module named 'autonerves' under the released stack

Type: bug
Target: autocti_visualization
Repos:
- autocti_visualization
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Filed: 2026-10-23

`render.yml` on main (run 39996567008, 2026-10-23, dispatched as the GitHub-token
phase 3 proof) fails in "Render figures + rebuild GALLERY.md": both producers
(`scripts/dataset_1d/visualization.py`, `scripts/imaging_ci/visualization.py`)
raise `ModuleNotFoundError: No module named 'autonerves'` right after
"Install the released stack from PyPI". The previous render (36626066338,
2026-09-29) also failed. Find whether the released autocti wheel lacks an
`autonerves` dependency (library packaging, PyAutoCTI) or the workflow's install
step omits it (workspace fix), fix at the right layer, then re-dispatch
`render.yml` — that run also proves the phase 3 PyAutoEyes App-token leg for this
repo (record complete/2026/10/github-token-p3-dispatchers-app.md), which is still
unproven.
