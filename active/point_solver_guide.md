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
