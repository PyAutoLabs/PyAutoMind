# PyAutoEyes phase 3 — birth autogalaxy_visualization (PyAutoGalaxy figures)

Type: feature
Target: autogalaxy_visualization
Repos:
- autogalaxy_visualization
- PyAutoEyes
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: active
Consequence: judge
Witness: `pyauto-brain eyes survey galaxy/autogalaxy_visualization` reports no gaps/orphans; its `gallery/gallery_build.py --check` green and tracked `gallery/viz_manifest.yaml` committed; `pyauto-eyes check` green with the galaxy registry row; the PyAutoEyes dashboard shows a galaxy section; `repos_sync.py --check` clean
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 3
Filed: 2026-09-25
Issued: 2026-09-29

Blocked on: human repo creation (`gh repo create PyAutoLabs/autogalaxy_visualization --public`); phase 2 shipped 2026-09-28 (`complete/2026/09/eyes-board-conductor-registry.md`).

## Task

Human first: `gh repo create PyAutoLabs/autogalaxy_visualization --public`.
Agent, local checkout at `galaxy/autogalaxy_visualization`, mirroring the
`autolens_visualization` project-repo layout from phase 1a:

- Port `autogalaxy_workspace_test/scripts/{imaging,interferometer,ellipse}/visualization/`
  to flat producers `scripts/<domain>/visualization.py` (HST-scale imaging +
  SMA interferometer presets copied from `autolens_visualization/instruments`),
  all-true `config/visualize/plots.yaml`, datasets simulated into `dataset/`
  with simulators under `scripts/misc/simulators/`.
- Render harness (`gallery/gallery_build.py` + `gallery_run.sh`), tracked PNGs,
  `GALLERY.md`, tracked `gallery/viz_manifest.yaml`; `lint.yml` + `render.yml`
  on the `pyautogalaxy-release` dispatch, which also fires `eyes-refresh` at
  PyAutoEyes.
- Registration, as phase 1a: Mind `repos.yaml` project row + `repos_sync
  --write`, `ROUTING.md` target, Brain `clean_slate.sh` exclusion, Heart drift
  exclusion.
- PyAutoEyes `registry.yaml` galaxy row; PyAutoGalaxy's release workflow fires
  the `pyautogalaxy-release` dispatch (as PyAutoLens does for lens).
