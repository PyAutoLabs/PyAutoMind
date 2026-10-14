# `@PyAutoFit` search-extensibility A4 companions: Brain sampler reference, developer-tier searches, workspace_test seeded Dynesty

Type: refactor
Target: autofit
Repos:
- PyAutoBrain
- autofit_workspace_developer
- autofit_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Epic: search-extensibility
Phase: A4-companions
Witness: `autofit_workspace_developer/searches/ultranest` and `pyswarms` (`globe`, `local`) import without a `FutureWarning`, construct and fit at `PYAUTO_TEST_MODE=1` and `=2`; `autofit_workspace_test/scripts/graphical/analytic_gaussian.py` passes parity 41/41 using `af.DynestyStatic(seed=)`; Brain `skills/sampler_pipeline/reference.md` no longer names a family base, `apply_test_mode` or `is_test_mode`.
Review-minutes: 10
Unattended: ready
Filed: 2026-10-14
Issued: 2026-10-14
Unblocked: PyAutoFit#1685/#1686/#1687 merged 2026-10-14 (record `complete/2026/10/search-ext-a4-decompose.md`)

Three external consumers of the family bases / old test-mode hooks that A4 deprecated for one release. Exact replacement text is in the PR bodies of PyAutoFit#1687 ("Companion changes required") and #1686 ("Companion changes required", the Dynesty case).

1. **PyAutoBrain `skills/sampler_pipeline/reference.md` ~129–136.** Subclass `NonLinearSearch` instead of a family base, declare `posterior_kind`, take defaults from `posterior_kind.{CHAIN,WEIGHTED,POINT}`, set `samples_cls`, implement `run(ctx)` with `test_mode_budget`. Drop the advice to call `apply_test_mode` / short-circuit on `is_test_mode`.
2. **`autofit_workspace_developer/searches/ultranest/search.py`.** Subclass `NonLinearSearch` with `samples_cls = SamplesNest` and the `WEIGHTED` posterior kind; initializer via `WEIGHTED.nested_initializer_for(...)`; replace the tail/override at ~:152/:157 with `test_mode_budget = {"max_iters": 1, "max_ncalls": 1}`.
3. **`autofit_workspace_developer/searches/pyswarms/abstract.py`.** Subclass `NonLinearSearch` with the `POINT` posterior kind; clipper via `POINT.clipper_for(...)`, initializer via `POINT.initializer_for(...)`; replace the tail/override at ~:123/:297 with `test_mode_budget = {"iters": 1}`; optionally pass `rng=initializer_rng(self)` at ~:171 so `seed=` reproduces start points.
4. **`autofit_workspace_test/scripts/graphical/analytic_autofit.py` (recommended, not required — the script works unchanged).** Delete `SeededDynestyStatic` (~206–219); line ~231 becomes `af.DynestyStatic(path_prefix="graphical", name=name, seed=seed, **kwargs)`; update the two docstring lines incl. `analytic_gaussian.py:50-51`.

Workspace-tier only; no PyAutoFit change. One PR per repo. autofit_workspace_developer has no CI — say so at ship.
