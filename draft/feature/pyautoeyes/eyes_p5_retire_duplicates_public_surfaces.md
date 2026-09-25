# PyAutoEyes phase 5 — retire duplicate galleries + public surfaces

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
- autolens_workspace_test
- PyAutoBrain
- PyAutoScientist
- pyautolabs.github.io
Themes:
- visualization
- infrastructure
Difficulty: medium
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: `autolens_workspace_test/gallery/` deleted with no CI referencing it; RTD `docs/organs/eyes.md` full page builds; `repos_sync.py --check` green
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 5
Filed: 2026-09-25

Blocked on: phase 4 shipped.

## Task

Delete `autolens_workspace_test/gallery/` (no CI uses it) and decide, per
workspace_test, whether their `visualization*.py` scripts stay as smoke
scripts; RTD `docs/organs/eyes.md` full page; PyAutoScientist + hub prose;
`autolens_profiling`/`autolens_inference` unchanged (profiling stays
per-library by the pinned-timing argument).
