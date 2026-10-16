## search-ext-a4-decompose
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1684
- completed: 2026-10-14
- epic: search-extensibility (phase A4)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1685
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1686
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1687

**Shipped:** three stacked PyAutoFit PRs, merged in order by human `/prm` on 2026-10-14 (tier judge): #1685 A4a decompose (8e5487ae9), #1686 A4b seed (5bf057f28), #1687 A4c family bases (df6d218f1). Pre-merge Codex gpt-6-astra adversary review 07 (`draft/research/autofit/search_extensibility_epic_reviews/07_codex_astra_a4_stack_premerge.md`, FINDINGS 4) was enacted on the branches before merge; all four reproduced.
- A4a: `abstract_search.py` 2102 → 585 lines; `TestModeBypass`, `SearchFactorOptimiser` moved out, `SearchRuntimeSettings`/`paths_from`, paths capabilities; non-lifecycle method groups in `__init__`-less mixins (`execution.py`, `internal_state.py`, `updates.py`, test-mode mixin) because `FitLifecycle` is deferred to A5 (D22). Pool shims and `SneakyPool` kept deprecated until A5. All 15 default identifiers, `hash_list`, `to_dict` and constructor-argument sets byte-identical to main.
- A4b: search-level `seed` with `SeedSequence` fan-out (initializer on stream 0 from a numpy `Generator`; Emcee/Dynesty backend on stream 1; Nautilus/NSS/NUTS/SMC/MultiStart take the raw seed so existing seeded runs are bit-identical; Zeus initial points only). `seed` enters the identifier via the conditional walk when not None; `search.json` gains `seed` (null by default). Grid children get child streams through a spawn key that is never hashed or serialized. NUTS/SMC sentinel is None with `backend_seed` 42. Human rulings: the MultiStart explicit-seed re-key ACCEPTED (no override); the explicit-seed NUTS/SMC re-key as in report §8.6.
- A4c: family bases out of the MRO, deprecated thin subclasses warn (`FutureWarning`, stacklevel 3) for one release; per-`posterior_kind` defaults (CHAIN/WEIGHTED/POINT) for plotter, initializer, clipper, auto-correlation settings; SMC uses the weighted plotter and drops `auto_correlation_settings`; chain auto-correlation defaults built at construction (the four strict xfails now pass). Drawer names `clipper` explicitly.
- Review 07 fixes: (1) old default NUTS/SMC `search.json`/pickles recorded `seed: 42` and would have re-keyed through the aggregator's recompute — a NUTS/SMC seed of 42 now loads as the default None (sampling unchanged; an explicit `seed=42` shares the default identity, documented) and `SearchOutput.id` prefers the saved `.identifier`; (2) Dynesty resolves `rstate` once (`_sampler_kwargs`; a subclass's own `rstate` wins), so `SeededDynestyStatic` in autofit_workspace_test keeps working; (3) `seed.child_seed` gives grid children of Nautilus/NSS/NUTS/SMC/MultiStart distinct backend seeds (standalone seeded runs unchanged; grid cells of default-seeded searches no longer replay identical randomness); (4) Drawer's `clipper` moved after the existing positional slots and SMC takes old positional calls behind a deprecated `*legacy_positional` (conformance signature set for SMC gains it).
- Follow-up red leg: #1686's initializer change made `test_autofit/interpolator/test_covariance.py::test_single_variable` nondeterministic again (fixture seeded stdlib `random`, which the initializer no longer reads); fixed test-only by patching `seed.seed_sequence` in the fixture; 20/20 deterministic.
- Tests at merge: full serial suite 3776 passed / 1 skipped / 0 xfailed; nojax emulation 3459 / 180 skipped; Sphinx 30 warnings (limit 30); `docs/_generate_searches.py --check` clean; CI green on unittest 3.12, 3.13, nojax, generated-search-docs, Docs for every PR. autofit + autolens workspace smoke clean on PR 1 and PR 3; `autofit_workspace_test` graphical parity 41/41.
- Decisions the human may want to revisit: grid children of default-seeded searches now have independent backend randomness; `SearchOutput.id` prefers the persisted identifier for every output.
- Companion changes (filed as `draft/refactor/autofit/search_ext_a4_companions.md`): PyAutoBrain `skills/sampler_pipeline/reference.md` ~129–136, `autofit_workspace_developer/searches/{ultranest,pyswarms}` onto `NonLinearSearch` + `posterior_kind` + `test_mode_budget`, and (recommended) autofit_workspace_test graphical `SeededDynestyStatic` → `af.DynestyStatic(seed=)`. Exact text in the #1686/#1687 bodies.
- Traps: GitHub auto-retargets a stacked PR to main when its base PR merges (no manual `--base` needed); `pytest -n auto` remains broken on this suite; the Codex read-only sandbox cannot run the disk-backed suite, so the worker re-ran those gates.

## Original prompt

# `@PyAutoFit` A4: decompose `NonLinearSearch`, search-level seed, delete the family bases

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
Phase: A4
Witness: `abstract_search.py` is ≤600 lines; BFGS at test-mode level 1 runs a reduced `maxiter`; two `Emcee(seed=1)` fits on one platform produce identical `samples.csv`; `Nautilus().hash_list` is unchanged; the A0a golden table is byte-identical for all 15 default constructions (default, explicit-None, explicit-seed, old-JSON and old-incomplete-output cases tested separately, the explicit-seed NUTS/SMC re-key accepted and recorded); the #1493 clipper tripwire passes; serialized constructor-argument sets match; subclassing a deprecated family base warns; the three developer-tier searches (`autofit_workspace_developer/searches/{nss,ultranest}`, `pyswarms`) still run; a 2-step EP test with MockSearch passes; autofit + autolens workspace smoke and `autofit_workspace_test/scripts/graphical` pass.
Review-minutes: 45
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

Authority: epic report `draft/research/autofit/search_extensibility_epic_report.md`
§3.2 (family bases + the nine invariants), §3.3 "Seed (D4)" with its legacy
table, §8.3 (D14), §8.5 (D22: `FitLifecycle` deferred to A5), the "#### A4"
phase entry; surveys 01 P4 and 02 P4. Dependencies A2 and A3 are merged;
review-05 fixes merged 2026-10-14 (PyAutoFit#1683). Human-agreed order
2026-10-14: A4 after B4a. Do not re-derive the decisions.

## Shape: ONE task, THREE stacked PRs, merged in order

**PR 1 — A4a decompose.** `TestModeBypass` with a shared
`finalize_result(samples)` and a generic `apply_test_mode` from
`test_mode_budget` via a post-init hook (BFGS level 1 → reduced `maxiter`);
`SearchFactorOptimiser` moves to `graphical/expectation_propagation/` keeping
`release_search_internal` and the updater cache-invalidation semantics;
`SearchRuntimeSettings` and `paths_from`; paths capabilities. `FitLifecycle`
is NOT extracted (D22). The legacy pool shims (`make_pool`, `make_sneaky_pool`,
`number_of_cores` accessors on the search) are marked deprecated but kept —
Emcee and the initializer still call them; their deletion is A5 when every
search is on `run(ctx)`. `SneakyPool` itself stays as `PoolFactory.sneaky`
(human ruling 2026-10-14). Target: `abstract_search.py` ≤600 lines.

**PR 2 — A4b seed (D4).** One search-level `seed` with `SeedSequence` fan-out:
stream 0 to the initializer (which stops using global `random`), stream 1+ to
the backend; grid-search children derive child streams. The seed enters the
identifier through a conditional in the identifier walk when not None — never
by adding `"seed"` to the base `__identifier_fields__`. Legacy table: Nautilus
and NSS keep their static `"seed"` field and their `seed` kwarg becomes an
alias of the base seed; NUTS and SMC keep an unhashed default 42 (sentinel
default to tell "default 42" from "user passed 42") and a user-supplied seed is
hashed — record the accepted re-key of existing explicit-seed NUTS/SMC output
folders; the other 11 hash the seed only when not None. Promise scoped
honestly: same seed → same initial points for every search; bit-identical
samples only within a pinned backend/platform where demonstrated; MCMC archive
searches resume statistically.

**PR 3 — A4c family bases (D14).** Delete `AbstractMCMC`/`AbstractNest`/
`AbstractMLE` from the concrete searches' MRO. Their modules keep exporting
distinct deprecated thin subclasses that preserve the former defaults and warn
via `__init_subclass__` (removed one release later). Initializer, clipper and
autocorrelation defaults move into per-`posterior_kind` default objects applied
in each concrete `__init__`, never on `NonLinearSearch`; BFGS/MultiStart keep
`"clipper"` in `__identifier_fields__`. The plotter becomes per-`posterior_kind`,
replacing the family `plot_results`. SMC moves to the `weighted` posterior kind
with evidence and drops `auto_correlation_settings` (old `search.json` carrying
it still loads); its module stays at `mcmc/blackjax/smc/`. `AbstractDynesty`
stays. Brain `skills/sampler_pipeline/reference.md` (the subclassing guidance at
~:128-129) and the three developer-tier searches are updated in the same PR set
(PyAutoBrain + autofit_workspace_developer companion PRs, after PR 3 opens).

## Invariants every PR must hold (report §3.2)

1. Public class names and `af.` export names. 2. Identifier hashes — the A0a
golden table; the only change is the seed rule's table. 3. `files/search.json`
class paths, round-tripping, and serialized constructor-argument sets
(`dictable.py` walks `__bases__`). 4. On-disk layout and filenames incl.
`search_internal/*`; old outputs read forever. 5. `samples_info["class_path"]`
values (re-export aliases for moved classes). 6. The #1493 clipper tripwire.
7. `NonLinearSearch` stays a subclass of `AbstractFactorOptimiser`
(`EPOptimiser` accepts `af.Emcee()`). 8. External subclasses keep working one
release. 9. `Result` stays one class.

## Risks (report)

EP's path mutation and memory release (the RAL comments ~`:470-505`); test-mode
changes reach every workspace smoke run (bypass levels 2/3 heavily used in
autolens_workspace) — run autofit + autolens workspace smoke before each ship.

## Constraints

- `pytest -n auto` is broken on the PyAutoFit suite (address-based parametrize
  ids); run serially. Emulate the `unittest-nojax` leg before each ship.
  Sphinx warnings ≤30. Prior/Message design (#1500) untouched.
