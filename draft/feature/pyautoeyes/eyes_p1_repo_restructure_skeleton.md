# PyAutoEyes phase 1 — repo restructure into lens/ + organ skeleton

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
- PyAutoBrain
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: high
Lane: local-dev
Status: draft
Consequence: judge
Witness: `pyauto-eyes check --all` green; hermetic tests green; lint.yml green on the PR; a manual `render.yml` dispatch for `lens` reproduces the 40 PNGs (byte-diff acceptable only in the version string)
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 1
Filed: 2026-09-25

Blocked on: phase 0 shipped.

## Task

- Move current root content into `lens/` (producers, simulators, dataset,
  config, instruments, GALLERY.md, hermetic test). Keep `dataset/imaging/hst`
  byte-identical to profiling (never re-simulate).
- Generalise the harness into `eyes/`: `build.py` from `gallery/gallery_build.py`
  (title + version string become instance parameters; keep `scan_images`,
  `render_html`, `render_markdown`, `check`); `run.py` from `gallery_run.sh`
  (instance root arg); `registry.py` reads `registry.yaml`
  (`name, path, library, import_name, title, domains`).
- `bin/pyauto-eyes`: `render <instance|--all>`, `build`, `check`, `survey`
  (calls `pyauto-brain eyes survey <instance root>` per instance), `board`.
- Organ prose: AGENTS.md (role, boundary: renders and holds figures; never
  judges — the Brain conductor judges; never edits library plot code — routes
  via intake), `repos_sync:map` markers, CLAUDE.md stub, REFERENCE.md,
  README with vision (from today's README) and per-library instance table.
  Remove profiling boilerplate (instruments README rows, `_viz_cli.py` name →
  `eyes/_cli.py`).
- Workflows: `lint.yml` (ruff, `pyauto-eyes check --all`, pytest, lychee,
  render of changed instances on PR); `render.yml` gains an `instance` input
  and per-library `repository_dispatch` events (`pyautolens-release` today;
  `pyautogalaxy-release` etc. as instances land) and commits only that
  instance's images + GALLERY.md.
- Tests: hermetic build test (moved), registry test, `--check` test; then
  replace the Brain `WITNESS_EXEMPT` entry with a `pyautoeyes:` row in
  `config/policy.yaml` witness map.
