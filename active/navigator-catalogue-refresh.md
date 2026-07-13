# autofit_workspace Navigator Check RED on main — stale catalogue

Type: maintenance
Target: autofit_workspace
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

## Original request (verbatim)

Fix autofit_workspace Navigator Check RED on main: the navigator catalogue
(llms-full.txt, workspace_index.json) is stale after the EP #85 merge —
graphical_models.py cross-refs features/expectation_propagation.py but the
catalogue was never regenerated. Regenerate with regenerate_navigator.py autofit
and commit the result. --auto

## Context

Surfaced by the 2026-07-11 morning `/health` sweep ("workspace validation weekly
— CI is broken"). The `Navigator Check` reusable workflow (PyAutoBuild) has two
jobs; the **Catalogue staleness** job is RED on `autofit_workspace` `main`
(commit `831b08b`, the `feature/ep-statistics-completion` #85 merge):

```
llms-full.txt / workspace_index.json are stale.
Regenerate with 'generate.py autofit' and commit the result.
```

Root cause: the EP statistics-completion work added
`scripts/features/expectation_propagation.py` and a cross-ref from
`scripts/features/graphical_models.py`, but the generated navigator catalogue
(`llms-full.txt`, `workspace_index.json`) was never regenerated and committed.
Reproduced on clean `main`: source references EP, catalogue had **0** references.

autolens_workspace / autogalaxy_workspace Navigator Check are GREEN (they
self-healed on 2026-07-10) — this is autofit_workspace only.

## High-level plan

- Branch `feature/autofit-navigator-catalogue-refresh` off `origin/main`.
- Run `regenerate_navigator.py autofit` (Phase 2, no notebook rebuild — matches CI).
- Commit **only** the two regenerated catalogue files; open a pending-release PR.
- Merge stays human (`--auto` ends at PR-open).

## Detailed plan

- **Files changed:** `llms-full.txt`, `workspace_index.json` (generated
  artifacts only — no scripts, notebooks, or config touched).
- **Command:** from the workspace root,
  `python ../PyAutoBuild/autobuild/regenerate_navigator.py autofit`.
- **Diff:** +28/-1 — a new `expectation_propagation.py` catalogue entry (title,
  summary, cross_refs → graphical_models) and `graphical_models.py`'s `cross_refs`
  gains `features/expectation_propagation.py`.
- **Verification (all green locally):** `check_navigator.py --root . --banners=fail`
  passes; a second `regenerate_navigator.py autofit` is idempotent (no further
  drift) — so the CI "Catalogue staleness" diff-check will pass.
- **Conflict note:** `autofit_workspace` is co-claimed by the parked
  `markdown-renderings-workspaces` task, but that branch touches only
  `README.md`, `config/build/markdown_examples.yaml`, and `markdown/**` — it does
  **not** touch the catalogue, so the two branches are file-disjoint. Verified
  and human-approved to proceed in parallel (2026-07-11).
