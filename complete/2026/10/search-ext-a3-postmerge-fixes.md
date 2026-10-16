## search-ext-a3-postmerge-fixes
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1682
- completed: 2026-10-14
- epic: search-extensibility (phase 3c — post-merge fixes for A2/A3/A3b)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1683

**Shipped:** PyAutoFit#1683 (merged 2026-10-14 as 8437a3b76 via a human `/prm`; tier judge). Fixes all seven findings of the post-merge Codex gpt-6-astra review 05 (`draft/research/autofit/search_extensibility_epic_reviews/05_codex_astra_a2_a3_a3b_postmerge.md`). Every finding reproduced on main 911fe05e1 and each fix was test-first. The human ruled the 2026.10.11.1/2026.10.12.1 releases that carried the unfixed findings deliberate, so these ship as fixes in the next release.
- F1: a pre-A2 `Fitness` pickle with `use_jax_jit=False` restores as an eager objective (legacy key maps onto `compile`); a pickle with neither flag restores eager.
- F3: new `ExecutionSettings` in `preflight.py`, reached through `NonLinearSearch.execution_settings(analysis)`; preflight traces the resolved settings the backend runs (an eager scalar run is not traced; gradient/batched kinds still are). Dynesty's `use_jax_jit` flows through `fitness_overrides`; the `run(ctx)` bridge, Dynesty and MultiStartGradient build their `Fitness` from the same object.
- F2: the archive finalizes before `.completed` is written; NSS keeps its checkpoint until the result is written. With `PYAUTO_SKIP_FIT_OUTPUT=1` NSS leaves its checkpoint beside `.completed` (a completed folder never resumes).
- F4: direct `_fit` entry builds its `PoolFactory` from the analysis, so JAX never forks; the same gap was closed in Dynesty's core count, the initializer's `n_cores` and `make_sneaky_pool` (Zeus `make_pool()` unchanged, no analysis in its signature).
- F5/F6: `FitContext` closes context-created pools on success too (`PoolFactory.close(failed)` is idempotent); `ctx.update` saves the resume state before `perform_update` and never calls `finalize`. `docs/design/run_ctx.md` notes updated.
- F7: golden BlackJAX diagnostics are pinned by value, reference and ownership; sentinel -999 fails. CSV tolerance stays rtol 1e-12.
- Witness (item 7, on the PR): a scratchpad worktree at tag 2026.10.7.1 produced Dynesty and Emcee output folders; the new code loaded them via the Aggregator and took the "Fit Already Completed" path with the same max logL; hard kills (`os._exit(9)`) mid-fit resumed and completed under the new code; zipped restore worked for old- and new-era folders.
- Tests: full suite 3579 passed / 1 skipped / 4 xfailed; `unittest-nojax` emulation 3274 passed / 170 skipped / 2 xfailed; CI green on unittest 3.12, 3.13 and nojax plus Docs. Sphinx 30 warnings (limit 30). `pytest -n auto` is broken on the PyAutoFit suite (address-based parametrize ids in `test_prior_properties.py`, shared output folders) — pre-existing, run serially.
- Decided at close-out (human question 2026-10-14): `SneakyPool` stays as the pool factory's `sneaky` strategy; the `make_sneaky_pool` search-level shim is legacy and goes when A4/A5 remove the legacy `_fit` surface.
- Carried: review 05 item 8 (consolidate Drawer dill / Nautilus pool context / NSS checkpoint lifecycle) → later task, tagged in the epic ledger Resume.

## Original prompt

# `@PyAutoFit` search-extensibility A2/A3/A3b post-merge fixes (astra review 05)

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: 3c
Witness: (1) a `Fitness` pickled from the A1 release (`compile`-less, `use_jax_jit=False`) unpickles with an eager scalar objective — a regression test asserts the restored objective is not jitted; (2) preflight accepts an eager `use_jax_jit=False` likelihood and a `gradient_mode="reverse"` override by validating the same resolved settings the backend runs; (3) killing a search after `save_results` but before the archive finalizes leaves no `.completed`, and a rerun resumes and completes; NSS keeps its resume state until the result is written; (4) calling `_fit` directly with a JAX analysis never forks (asserted in a test); (5) a resumable toy search run through `run(ctx)` closes context-created pools on both the success and failure exit paths, and `ctx.update` persists the checkpoint strategy; (6) the golden diagnostics test fails when ESS/R-hat are replaced with sentinel values; (7) the disk-backed checks (loading a pre-release output folder, interrupt-and-resume, zipped restore) ran in a writable environment and their outputs are quoted on the PR.
Review-minutes: 30
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-14

## Original request

> Continue working on the PyAutoFit refactor epic. [...] I am happy to follow
> your recommendation on everything else, try do in groups of tasks so theres
> less input from me.

Recommendation adopted 2026-10-14: issue the review-05 fixes as one PyAutoFit
library task before A4/B4. The human ruled that releasing 2026.10.11.1 and
2026.10.12.1 with these findings in was deliberate, so they are now live bugs
in released code rather than release gates; the fixes go into the next release.

## Source

`draft/research/autofit/search_extensibility_epic_reviews/05_codex_astra_a2_a3_a3b_postmerge.md`
(FINDINGS 7; §3 findings, §6 resume actions) and the ledger
`draft/research/autofit/search_extensibility_epic.md` "Resume (2026-10-08 night)".
Verify each finding against current main before fixing it; every earlier astra
finding reproduced. All seven are confirmed still present on main at
`911fe05e1` (2026-10-14).

## Items (ledger order)

1. **Old `Fitness` pickle silently enables JIT** — `fitness.py` `__setstate__`
   pops `use_jax_jit` and defaults `compile=True`. Keep `use_jax_jit=False`
   eager; add a pickle-from-A1 regression test. (F1, P1)
2. **Preflight validates the declared config, not the resolved runtime config**
   — `preflight.py` traces the declared objective kind, so it wrongly rejects
   `use_jax_jit=False` eager likelihoods and the `gradient_mode="reverse"`
   override. Resolve the execution settings once and share them between
   preflight and sampling. (F3)
3. **`.completed` is written before the archive finalizes** —
   `abstract_search.py` writes `paths.completed()` straight after
   `save_results`; NSS discards its resume state during result processing
   (`nss/search.py` `resume_state.discard`). A failed archive write leaves an
   unrecoverable "completed" fit. Finalize first, recover on rerun. Predates A2
   but in scope. (F2, P1)
4. **Direct `_fit` builds `PoolFactory(self)` without the analysis**
   (`abstract_search.py` ~line 2012), so Nautilus JAX can fork with 2 cores.
   Pass the analysis; assert no fork happens. (F4)
5. **`FitContext` leaks context-created pools on success** (`fit_context.py`
   closes pools only on failure) and **`ctx.update` never saves the checkpoint
   strategy**. Both violate the frozen `run(ctx)` contract. Test with a
   resumable toy search on both exit paths. (F5, F6)
6. **Shape-only golden diagnostics** (`test_golden_samples.py`) pass with
   ESS/R-hat set to -999. Add value-sensitive tests of where the diagnostics
   come from; keep the CSV tolerance (rtol 1e-12). (F7)
7. **Disk-backed checks in a writable environment**: loading pre-release output
   folders, interruption and resume, zipped restore. Quote results on the PR.

Out of scope (carried to a later task): consolidating backend-specific
lifecycle paths (Drawer's dill, Nautilus's own pool context, NSS deleting its
checkpoint) — review 05 item 8, tagged [later].

## Constraints

- Library only; no workspace edits. Downstream workspace adoption of A1/A2 was
  already repaired on 2026-10-10 (`complete/2026/10/heart-fitness-dispatch.md`,
  `heart-hierarchical-backend.md`) — do not redo it.
- Emulate the `unittest-nojax` leg before ship (new tests that import jax or
  blackjax need `importorskip`).
- Sphinx warning budget: do not push the count over the CI limit.
- Not the Prior/Message design (#1500): untouched.
