# PointSolver guide: oracle, usage, assumptions and limitations

- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/801

Issue autolens_workspace#599. Merged 2026-10-24 via /prm. Epic `cluster-pointsolver-speed`.

## What shipped
- **PyAutoLens#801** (`c6927eeb3`): docstring only. The `residual_threshold` docstring now says:
  - the Newton distance |A⁻¹r| fails at steep power-law (slope > 2) and point-mass centres, at about one triangle edge;
  - the cut's margin is about 1.3× at precision 0.005, and core candidates survive at 0.01;
  - the central-image false rejection only matters when `magnification_threshold` is below about 0.02.
- **autolens_workspace#600** (`4270d6555`): move only, `guides/point_source_pairing.py` → `guides/point_solver/pairing.py`, with every reference and the catalogue updated.
- **autolens_workspace#601** (`c7a7329a9`): the new `guides/point_solver/limitations.py` and its notebook.
  - An inline 30-line oracle.
  - The solver's settings, including h = `scale / 2**(n_steps-1)`.
  - Two assumptions: the magnification cut (deliberate, per the human), and positions being triangle centres.
  - Limitations a–g: starting grid, extent, singular-centre spurious points, near-member completeness, duplicates, JAX, multi-plane. Each says whether it applies at the defaults.
  - Added to `smoke_tests.txt`. It takes about 3.3 s end to end, about 1.4 s of which is the import.
- **HowToLens#101** (`79967d893`): the tutorial_5 path fix, plus a navigator catalogue regeneration after the first CI run failed the staleness check.

## Decisions
- The Newton-distance filter (residual AND |A⁻¹r| > 4h) was **not** adopted, after adversarial reviews by Claude and Codex gpt-6-astra. It is re-scoped to `draft/research/autolens/point_solver_root_refinement.md`.
- `magnification_threshold` dropping demagnified images is a modelling **assumption**, not a limitation (human, 2026-10-24).
- The guide keeps `ENV: full_datasets`. `PYAUTO_SMALL_DATASETS` short-circuits every solve, so the smoke test would check nothing.

## Validation
- PyAutoLens point tests: 319 passed, 1 xfailed.
- Both guides run cleanly, and the printed numbers match the prose.
- CI was green on every leg of all four PRs at merge.
- Heart was YELLOW at ship (manifest drift; PyAutoLens release validation stale), acknowledged by the human.

## Original prompt

# `@autolens_workspace` guides/point_solver: a human-facing guide to the PointSolver's oracle, use and limitations

Type: docs
Target: autolens_workspace
Repos:
- @PyAutoLens
- @autolens_workspace
Themes:
- point-source
- cluster
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Epic: cluster-pointsolver-speed
Related: PyAutoLens#799/#800; research prompt `draft/research/autolens/point_solver_root_refinement.md`
Filed: 2026-10-24
Issued: 2026-10-24
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/599

## Request (verbatim)

> This all sounds good, I agree we should putt his as research for the future so do the things you said. However, can we also make a human facing python script plus Jupyter notebook which explains the Oracle (maybe with a preloaded result if its slow), shows the PointSolver being used and then explicitly documents this bug / issue and any others? I.e. lets have a resource that makes it reeally easy for any human to check in on every limitation and assumption of the PointSolver. I think this belongs in autolens_workspace as I reckon users may be interest, I think the guides package could have a package called "point_solver" with this, with the other point specific guides being located in there. Keep it concise and succient.

## Deliverables

1. `@PyAutoLens` docstring-only fix: the `residual_threshold` docstring in `autolens/point/solver/shape_solver.py`. The |A⁻¹r| claim holds for steep cusps and point masses but not for zero-core dPIE. Also note the known false rejection at low `magnification_threshold`.
2. `@autolens_workspace`, move-only: `scripts/guides/point_source_pairing.py` moves into the new `scripts/guides/point_solver/` package, plus its notebook and references.
3. `@autolens_workspace`, new guide (human 2026-10-24: `magnification_threshold` is a deliberate **assumption**, not a limitation. Demagnified images are not observed, so modelling should drop them. Every limitation states whether it applies at the default threshold.) `scripts/guides/point_solver/limitations.py` plus a notebook: explain the oracle, show the PointSolver, and document every known limitation and assumption. Keep it concise.
