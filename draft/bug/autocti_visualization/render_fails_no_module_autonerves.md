# autocti_visualization render.yml fails: No module named 'autonerves' under the released stack

Type: bug
Target: autocti_visualization
Repos:
- autocti_visualization
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
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

## Decision (human, 2026-10-23): render from the library mains

Cause: `render.yml` installs `autocti[optional]` from PyPI, whose newest release is
`2024.11.13.2` (autocti is not in the Hands release train — `release.yml` says
"the CTI release train is not yet wired"). That wheel predates `autonerves`; the
producers import `from autonerves import conf`. So the render cannot pass from PyPI.

Fix in `cti/autocti_visualization/.github/workflows/render.yml`, mirroring `lint.yml`:
when no version is given (manual dispatch with blank input — the default), check out
PyAutoNerves, PyAutoFit, PyAutoArray and PyAutoCTI mains into sub-folders, install
each `./<repo>[optional]` in dependency order and put them on `PYTHONPATH`; keep the
PyPI path for an explicit `autocti_version` input or a `pyautocti-release` dispatch
(for when the CTI train is wired). The bot commit message names the source
(`PyAutoCTI main@<sha>`, not `autocti.__version__`, which is a stale stamp from a
source checkout). Update the header comment and the `AGENTS.md` Testing paragraph.
Out of scope: changing `gallery_build.py`'s `rendered_with:` (PR notes it).

Witness (post-merge): one `render.yml` dispatch on main succeeds end to end — render,
bot commit, App mint, `eyes-refresh` dispatch — and a PyAutoEyes Dashboard Refresh run
appears. That also closes the GitHub-token phase 3 proof for this repo.
Consequence: judge (CI behaviour change; proof is post-merge).
