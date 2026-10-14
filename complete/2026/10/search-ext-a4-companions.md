## search-ext-a4-companions
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/520
- completed: 2026-10-14
- epic: search-extensibility (A4 companions)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/522
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/111
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/33

**Shipped:** tier glance under the human's 2026-10-14 `--auto` launch; in-turn tiered merge by the shipping worker after the Witness passed. PyAutoBrain#522 (9e0ef6c1b, closes #520) → autofit_workspace_test#111 (26877bc69) → autofit_workspace_developer#33 (3df620e0d; no CI in that repo — merged last, fit proof quoted on the PR).
- Brain `skills/sampler_pipeline/reference.md` Stage 3 now describes the A4 anatomy: subclass `NonLinearSearch`, declare `posterior_kind` + `test_mode_budget`, defaults from `posterior_kind.{WEIGHTED,POINT,CHAIN}`, `samples_cls`, `run(ctx)` + `raw_samples_from`; no `apply_test_mode`/`is_test_mode`.
- Developer `searches/ultranest/search.py` (WEIGHTED, `SamplesNest`, `nested_initializer_for`, budget max_iters/max_ncalls 1) and `searches/pyswarms/abstract.py` (POINT, `clipper_for`, `initializer_for`, `rng=initializer_rng(self)`, budget iters 1) off the deprecated family bases; imports clean under `-W error::FutureWarning`; identifiers unchanged vs main.
- workspace_test graphical: `SeededDynestyStatic` deleted, `af.DynestyStatic(seed=)` used; `analytic_gaussian.py` PARITY PASS 41/41 twice.
- Gate: Brain pytest 1258 pass (+CI 3.12/3.13); awt smoke 15/15 (+CI); review CLEAN (independent subagent, same model family); Heart STALE (no rehearsal for current source); witness PASS except UltraNest at test mode 1, which fails with the environment's numpy-ABI ImportError identically on main.
- Revert, if needed: `git revert 9e0ef6c1b` (Brain), `git revert 26877bc69` (awt), `git revert 3df620e0d` (dev).

## Original prompt

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
