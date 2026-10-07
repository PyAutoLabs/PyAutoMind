## eyes-organ-skeleton
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/448
- completed: 2026-09-28
- epic: pyautoeyes-birth (phase 1b)
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/2
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/428
- summary: PyAutoEyes is stripped to the cross-project dashboard skeleton. The lens scripts, dataset and GALLERY.md are gone; their history now lives on PyAutoLabs/autolens_visualization (PR #1). What is left is `registry.yaml` (one lens instance), the `eyes/` package (registry, manifest reader, board builder, check), `bin/pyauto-eyes`, `dashboard.md/.html`, hermetic tests and lint/pages/refresh workflows. The organ renders nothing, judges nothing and copies nothing: it reads each project's tracked `viz_manifest.yaml` from its raw GitHub URL and links to its PNGs. Brain#428 adds the PyAutoEyes `test_witness` row to `config/policy.yaml`.
- verification: after the merge, `bin/pyauto-eyes check` on main printed `check: OK` (registry 1 instance; lens manifest schema 1, 40 figures; all 40 raw URLs resolve; dashboard current). `lint` on the merge commit passed.
- human-steps: (1) enable GitHub Pages on PyAutoEyes with source "GitHub Actions". The merge-commit `Pages Dashboard` run 36480443757 failed at configure-pages with "Resource not accessible by integration" because Pages is not enabled; re-run it after enabling. (2) In a later PR, remove the lychee `pyautolabs.github.io/PyAutoEyes` exclusion in `.github/workflows/lint.yml`. (3) PAT_PYAUTOLABS must be granted to autolens_visualization and must cover PyAutoEyes, or render.yml's `eyes-refresh` dispatch warns and skips.
- traps: the canonical PyAutoEyes checkout still holds untracked and ignored render leftovers from the old layout (`scripts/**/*.fits`, `dataset/interferometer/sma/lensed_source.fits`, `output/`, `gallery/`, `instruments/`). They are not tracked on main. The ff-pull left them behind, so a local `ls` still shows `scripts/`, `dataset/` and `output/`.
- next: phase 2 — `draft/feature/pyautoeyes/eyes_p2_board_and_conductor_registry.md`

## Original prompt

# PyAutoEyes phase 1b — strip the organ to its dashboard skeleton

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
Witness: `pyauto-eyes check` green against the lens registry row (manifest resolves, every listed PNG URL resolves); hermetic tests green (registry, manifest reader, board builder on a fabricated manifest, check); lint.yml green on the PR; `pyauto-eyes board` writes `dashboard.md/.html` with a lens row linking into `PyAutoLabs/autolens_visualization`
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 1b
Filed: 2026-09-28
Issued: 2026-09-28

Blocked on: phase 1a shipped (history confirmed on `PyAutoLabs/autolens_visualization`).

## Task

PyAutoEyes becomes the cross-project dashboard of the layered design (human
decision 2026-09-28): it reads each `<lib>_visualization` project repo's
tracked manifest and links to its PNGs. It renders nothing, copies no
figures, never judges (the Brain Eyes conductor does), never edits library
plot code (critiques route through intake).

- **Strip, in one PR.** Delete from the organ everything phase 1a moved to
  `autolens_visualization`: `scripts/` producers + simulators, `dataset/`,
  the tracked PNGs, `GALLERY.md`, `instruments/`, `config/`, `gallery/`,
  `_viz_cli.py`, `activate.sh`, `render.yml`. History stays in git and in
  the project repo.
- **`registry.yaml`** — one row per instance: `name, path, github, library,
  import_name, manifest` (tracked path in the project repo, e.g.
  `gallery/viz_manifest.yaml`), `images_base_url` (raw.githubusercontent
  base), `dispatch` (the library release event the project repo re-renders
  on). Lens row only.
- **Manifest contract** — `REFERENCE.md` specifies the fields the project
  repos commit (figure list + rendered stack version) and what the organ
  reads; versioned so project repos and organ can move independently.
- **`eyes/` package** — `registry.py` (read + validate `registry.yaml`),
  `manifest.py` (read a manifest from a local checkout or its GitHub raw URL),
  `board.py` (build `dashboard.md/.html` from registry + manifests; phase 2
  fills the content).
- **`bin/pyauto-eyes`** — `board`, `check` (registry valid, every manifest
  reachable and parseable, every PNG URL resolves), `survey` (runs
  `pyauto-brain eyes survey <instance root>` per registered instance).
- **Organ prose** — AGENTS.md / README.md / REFERENCE.md / CLAUDE.md stub
  stating the layering (project repos make, store and track figures; the
  organ is where the human checks in on visualization across all projects;
  same layering as `autolens_profiling` / `autolens_inference` under the
  Brain board), `repos_sync:map` markers kept.
- **Workflows** — `lint.yml` (ruff, pytest, `pyauto-eyes check`, lychee);
  `pages_dashboard.yml` + `dashboard_refresh.yml` on `repository_dispatch`
  (`eyes-refresh`, fired by each project repo's `render.yml`) and a daily
  cron (Cortex pattern).
- **Tests** — hermetic: registry, manifest reader, board builder on a
  fabricated manifest, `check`. Then replace the Brain `WITNESS_EXEMPT`
  entry (`tests/test_policy_seams.py`) with a `pyautoeyes:` row in
  `config/policy.yaml`'s witness map.

## Ship policy

PyAutoBrain (witness row) merges after PyAutoEyes. While Heart is RED the PRs
ship only under a contemporaneous human RED override. Merge stays human.
