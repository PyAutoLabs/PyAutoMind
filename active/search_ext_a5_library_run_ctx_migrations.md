# `@PyAutoFit` A5 (library): migrate every search onto `run(ctx)`, delete the legacy `_fit`/pool surface, ship the new-search template

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: A5-library
Witness: no search outside `abstract_search.py` overrides `_fit` (grep `def _fit(` under `autofit/non_linear/search` returns only the base); `make_pool`, `make_sneaky_pool` and the `number_of_cores` shim are gone from `execution.py` and nothing in PyAutoFit, PyAutoLens, PyAutoGalaxy, PyAutoCTI or the workspaces here references them; a toy search written from `autofit/non_linear/search/_template/search.py` passes both A0a conformance layers in ≤250 lines with the documented ~6 PyAutoFit touch points (search file, registry entry, export line, unit test, integration script, workspace section); the A0a golden identifier table is byte-identical for all 15 searches; `Emcee(seed=1)`, `DynestyStatic(seed=1)` and `Nautilus(seed=1)` fits produce `samples.csv` byte-identical to the same fits on main df6d218f1 (A4 merge); the per-search `autofit_workspace_test/scripts/searches/<Name>.py` (+`_jax`) scripts pass at `PYAUTO_TEST_MODE=1` and `=2` with the same pass set as main; `pyauto-heart smoke autofit autolens` clean.
Review-minutes: 45
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

Authority: epic report `draft/research/autofit/search_extensibility_epic_report.md` "#### A5", §3.5 (decomposition and the `run(ctx)` hook), §8.5 (D22: `FitLifecycle` only if the migrations show it is needed); `search_extensibility_epic_surveys/01_search_architecture.md` "Phase 5"; A1's frozen `docs/design/run_ctx.md`. A2 migrated Drawer and Nautilus, A3b NSS, A4 moved SMC to the weighted posterior kind and decomposed the base — do not redo those. This is the LIBRARY half of A5; the consumer half (Hands roster, assistants, Brain SamplerSurface, workspace CI anchors, al/ag guide collapse) is `search_ext_a5_consumers.md`, blocked on this.

## Shape: ONE task, stacked PRs merged in order

1. **PR 1 — simple searches onto `run(ctx)`:** Emcee, Zeus, BFGS/LBFGS. Each migration deletes the search's `_fit` override and implements `run(ctx)` against `FitContext` (fitness, pool via `PoolFactory`, `start_points`, resume state from its `Checkpointer`, `ctx.update`). Per-search unit tests and the A0a suite gate each.
2. **PR 2 — Dynesty (static, dynamic, pooled), BlackJAX NUTS and SMC** the same way; Dynesty's `_sampler_kwargs()` and the A4 `rstate` precedence stay.
3. **PR 3 — MultiStart** last; split its `_fit` internally regardless (survey 01 P5) and keep `_seed_for` + `child_seed` semantics from A4.
4. **PR 4 — framework close:** delete the legacy `_fit` surface in `execution.py` (`make_pool`, `make_sneaky_pool`, `number_of_cores`; `SneakyPool` itself stays as `PoolFactory.sneaky`); unknown-kwarg guard (warn, never raise) for kwargs no `__init__` in the MRO consumes; `SettingsSearch` filters `use_jax_vmap` to searches that accept it; `search/_template/search.py` with the contract in its module docstring, plus the template smoke (a toy search built from it, kept as a test fixture, passes both A0a layers); `docs/design/run_ctx.md` revision note; `docs/_generate_searches.py --check` clean. Introduce `FitLifecycle` ONLY if PRs 1–3 show duplicated lifecycle code that the mixins cannot host — say so in the PR body either way (D22).

## Invariants every PR must hold
- The A0a golden table (`test_autofit/non_linear/search/conformance_roster.py`), `hash_list`, `to_dict` and constructor-argument sets byte-identical to main for all 15 searches; `samples_cls` paths unchanged.
- Seeded runs bit-identical before and after each migration (compare `samples.csv` against main df6d218f1 for each migrated search with `seed=1`); unseeded runs keep fresh entropy.
- The review-05 and review-07 fixes stay (old `Fitness` pickle semantics, preflight resolved settings, `.completed` after the archive, pool close on success, old NUTS/SMC seed-42 identity, Dynesty `rstate` precedence, grid `child_seed`).
- JAX fork rule: no search forks under a JAX analysis; `PoolFactory` is the only pool source after PR 4.
- Old output folders (pre-A2, A4-era) still load through the Aggregator and resume; the disk-backed checks run in a writable environment and are quoted on the PR.
- `abstract_search.py` stays ≤600 lines (test guards it).

## Constraints
- Serial pytest (`-n auto` is broken on this suite); emulate `unittest-nojax` with the import-hook plugin (`nojax_plug` in the session scratchpad or rebuild it); Sphinx ≤30 warnings.
- Prior/Message design (#1500) untouched. No consumer repos in this task.
- Each PR body lists "Companion changes required" for anything outside PyAutoFit (expected: none beyond the A5 consumers task; the developer-tier searches are handled by `search_ext_a4_companions.md`).
