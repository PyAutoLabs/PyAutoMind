## eyes-galaxy-instance
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/452
- completed: 2026-09-29
- epic: pyautoeyes-birth (phase 3)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/430
- library-pr: https://github.com/PyAutoLabs/autogalaxy_visualization/pull/1
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/453
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/243
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/4
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/179
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/15
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/48

### What shipped
- **autogalaxy_visualization#1** (merge a0b0177a) — the new project repo:
  - Three flat producers rendering 41 tracked PNGs: imaging 11, interferometer 13, ellipse 17.
  - Simulators on copied HST/SMA presets; the SMA dataset is re-simulated on the masked grid with over_sample 1.
  - An all-true `plots.yaml`, the gallery builder and a schema-1 `gallery/viz_manifest.yaml`.
  - `lint.yml` + `render.yml`, listening for `pyautogalaxy-release` and firing `eyes-refresh` at PyAutoEyes.
- **PyAutoEyes#4** (merge dab4550f) — the galaxy registry row; dashboard regenerated with both instances (`pyauto-eyes check` OK: lens 40, galaxy 41 figures).
- **PyAutoMind#453** (merge 86e72516) — body-map row, ROUTING and epics updates, plus three drafts filed:
  - `draft/feature/pyautohands/release_fires_visualization_dispatch.md`
  - `draft/bug/autogalaxy/ellipse_plotter_fit_ellipse_overwrites.md`
  - `draft/maintenance/pyautomind/session_start_hook_copies_regen.md`
- **PyAutoHeart#243** (merge 92f9752a) — drift exclusion for the new repo.
- **PyAutoBrain#430** (merge 33eee267) — conductor / skill prose for the second instance.
- **PyAutoNerves#179, PyAutoGut#15, PyAutoCortex#48** (merges b248a974, 994fc6e1, f205fcab) — `repos_sync` map blocks.

### Witness evidence
- Delivered: `pyauto-brain eyes survey` on the galaxy repo, `gallery_build.py --check` green with the tracked manifest, `pyauto-eyes check` green with the galaxy row, and the dashboard's galaxy section.
- **Not delivered:** `repos_sync.py --check` "clean". It still reports 28 pre-existing hook-copy drifts and the `.github` profile table (draft `draft/maintenance/pyautomind/session_start_hook_copies_regen.md` filed).

### Traps / notes
- Nothing sends `pyautolens-release` / `pyautogalaxy-release` yet, so `render.yml` never fires from a release (draft `release_fires_visualization_dispatch.md` filed).
- The Eyes survey is non-recursive, so the galaxy repo uses a flat producer layout.
- `repos_sync.py --write` spills into the canonical organ checkouts; the spilled patches became the sibling Nerves/Gut/Cortex map-block PRs.
- The intake dashboard regen honours `PYAUTO_MIND=<worktree>`.
- Mind `test_repos_sync_root_default` fails under a sourced `activate.sh`.
- The auto-mode classifier denied `gh pr merge` until a `Bash(gh pr merge *)` allow rule was added and the command was run bare (unchained).
- The Eyes PR had to merge last (its check HEADs the galaxy PNGs on main) and needed a board regen after the galaxy merge.
- PyAutoGalaxy was untouched (claimed by workspace-config-cleanup).
- Gut and Cortex have no PR CI.

### Not verified / human follow-ups
- Grant `PAT_PYAUTOLABS` to autogalaxy_visualization (or make the org secret all-repos), then `gh workflow run render -R PyAutoLabs/autogalaxy_visualization`, then confirm PyAutoEyes `Dashboard Refresh` runs.
- Apply the `.github` profile README patch pasted on issue #452.

## Original prompt

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
