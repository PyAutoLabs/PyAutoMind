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
