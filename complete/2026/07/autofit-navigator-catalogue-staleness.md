## autofit-navigator-catalogue-staleness (regenerate — MERGED)
- completed: 2026-07-13 (filed + fixed same session; no GH issue — trivial)
- pr: autofit_workspace#93 — MERGED (squash) 2026-07-13.
- summary: autofit_workspace `navigator / Catalogue staleness` CI was red on main (surfaced merging Group B #151). Cause: a stale `Search: NSS` entry in `workspace_index.json`/`llms-full.txt` left after the NSS sampler removal. Fix: `PyAutoBuild/autobuild/regenerate_navigator.py autofit` → only the 2 catalogue files changed (no incidental churn). CI green post-merge (navigator staleness + smoke). Recurrence note (from the prompt): consider auto-regenerating the catalogue in pre_build/pre-commit so it can't drift on main again.
