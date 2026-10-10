# Search extensibility epic: a PyAutoFit search framework for many samplers, a unified JAX contract, generated search docs, and autofit_inference / autofit_profiling

Type: research
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace
- autofit_workspace_test
- HowToFit
- autofit_assistant
- PyAutoBrain
- PyAutoMind
- PyAutoCortex
- PyAutoPulse
- PyAutoInsight
- PyAutoNerves
- PyAutoHeart
- PyAutoLens
- PyAutoGalaxy
- PyAutoCTI
Themes:
- searches
- jax
- documentation
- inference
- profiling
Difficulty: large
Autonomy: human-required
Priority: high
Epic: search-extensibility
Status: draft
Filed: 2026-10-07
Witness: A toy search written from `search/_template/search.py` against the `run(ctx)` hook passes both conformance layers (metadata on every CI leg, backend execution on the full-extras legs) in ~120–250 backend lines with ~6 PyAutoFit edits (search file, registry entry, export line, unit test, integration script, workspace section); every `af`-exported search declares capability attributes enforced by the `fit()` gate after the test-mode bypass (REQUIRED+numpy raises; JAX analyses get a lazily jitted objective); docs/api/searches.rst, the RTD capability matrix, a fenced roster block in llms.txt and the three assistants' rosters are generated from the versioned search manifest, pinned to the installed autofit release, leaving ~10–12 hand-edited documentation files per new search (from ~51); autofit_inference publishes the `gaussian_x3_blend` + `gaussian_x3_separated` wave-1 pilot and then scored wave-2 verdicts (50 seeds, thresholds frozen after the pilot; success rate with Wilson intervals, wall per right answer with bootstrap intervals) to PyAutoInsight as instance `fit`, and autofit_profiling publishes `profiling-summary@2` to PyAutoPulse as instance `fit` with the epic-1 ranked bottleneck table (B4a).

Research report and phased epic plan: `search_extensibility_epic_report.md` alongside this file (written 2026-10-07 by the architect session from four Opus surveys in `search_extensibility_epic_surveys/`; no code edited).

## Summary

The public search API (`af.<Search>(...)`, `search.fit(model, analysis)`) stays. What gets refactored is the code behind it:

- an implicit contract;
- about 1,000 lines of copy-paste across 15 searches;
- a 1,691-line `NonLinearSearch` god class;
- five `search_internal` persistence strategies.

The epic replaces these with:

- **capability class attributes** collected by **one registry**;
- one `Fitness.objective(kind)` factory and a fail-fast JAX gate. This also fixes eager, un-jitted JAX in Emcee, Zeus and Drawer (27× slower);
- a `RawSamples` adapter and a `Checkpointer`;
- the extracted collaborators;
- finally, a `FitContext` + `run(ctx)` hook, so that a new search is one file plus one registry entry.

Per-search documentation facts are generated from the registry, which cuts about 51 hand-edited files per new search to about 10–12. Per-search judgement has exactly one public home, `autofit_inference`, which reports to **PyAutoInsight**, not Pulse. `autofit_profiling` reports to PyAutoPulse and is the already-filed Pulse task `autofit_profiling_bootstrap`, which this epic adopts.

The first benchmark is `gaussian_x3_blend`: 3 Gaussians plus a background (10 parameters) with ordered centres, run under a pre-registered protocol alongside a `gaussian_x3_separated` control. Wave 1 is an exploratory pilot; scored wave 2 runs on RAL `--partition=ral` only, never `gpu`.

Reviewed 2026-10-07 by Codex gpt-6-astra and Claude Fable (high); decisions in report §8.

The plan has two dependency-ordered tracks:

- **A0–A5:** the PyAutoFit framework.
- **B1–B5:** the benchmark repos. B1 is a human gate on two `gh repo create`.

Start with A0a(i), A0c and B1.

## Original request (verbatim)

Soon, we are going to do a large scale inference run using PyAutoPulse and autolens_inference, but I want to do some infrastructure refactoring and improvements to support this first. Firstly, this campaign will likely lead to a number of new samplers and searches being added to PyAutoFit -- my vision is that we will see many more added, because with AI it is easy to add and maintain them. Therefore, I want us to refactor abstract_search.py and the search package to enable the most streamlined and efficient adding of searches. The API i s already good, but I suspect there are a number of refactors which could improve the extensibility of PyAutoFit. This includes things like how we manage results with Samples after a search runs, managing the split of mcmc / nest / mle and the abstraction layer between a search's internal results and PyAutoFit's formats. This likely will require some deep thought a review, but I am confident some clear redesigns are possible. I suspect abstract_search would benefit further from more separation of concerns where possible. A complete assessment of the JAX interface, which at the moment is a bit patch-y in terms of when a search supports or uses it would be worthwhile, I think this also need to be unified across all searches and a clear seapration of when as earch does or does not use JAX. Pair this work to how searches are documented throughout PyAutoFit RTD, its workspace and the workspace of other packages. I think this work will be paired to (or follow up) an autofit_inference package, which implements models that make sense to profile and evaluation different searches. This should begin with one model and likelihood function, which should extend the toy Gaussian to have around 10 parameters, maybe fitting 3 Gaussians? We would then add extra models to test different behaviour. We should also put in an autofit_profiling repo which mirrors PyAutoPulse for this to speed them up. These runs will ultimately build up a large ctalogue of information and research wikis to support the autofit_assistant in recommending and choosing a search for a user. Clearly this is a large task, which is going to become an epic,  and thus needs scoping out and reviewing at this scale accordingly.

## Status

B1 human gate passed 2026-10-07 (both repos created, empty). A0a(i) prompt filed 2026-10-07 at `draft/test/autofit/search_conformance_metadata_layer.md`; plan approved by the human 2026-10-07 (ruling: identifiers stay the same; any identifier change is flagged first); ISSUED as PyAutoFit #1666 (https://github.com/PyAutoLabs/PyAutoFit/issues/1666), task `search-conformance-metadata` in active.md, worktree `~/Code/PyAutoLabs-wt/search-conformance-metadata` on `feature/search-conformance-metadata`; PyAutoFit claim released from community-pages (its #1663 merged). MERGED 2026-10-07T20:37Z (PR https://github.com/PyAutoLabs/PyAutoFit/pull/1667, pending-release; record `complete/2026/10/search-conformance-metadata.md`); 3066 passed / 5 strict xfails locally, no-jax leg emulated; the 5 xfails are the A0b (NUTS/SMC round trip) and A3 (Emcee/NUTS/SMC config mutation) repairs. A0a(i) DONE. B1 registration ISSUED 2026-10-07 as PyAutoMind#492 (task `search-ext-b1-registration`, 6-repo worktree + org .github branch `feature/search-ext-b1-registration`); human approved the plan, Mind coordination with mind-dashboard-simplify (#491), RAL clones, and the deviation that NO Pulse/Insight registry rows land at B1 (both organs' `check` fail an instance without a published summary; the `fit` rows land in B4a/B3). Cortex row is `planned` (no ledger until B3). SHIPPED 2026-10-07 as 7 PRs: autofit_inference#1, autofit_profiling#1, Mind#493, Heart#292, Cortex#60, Pulse#33, .github#34 — 5/7 MERGED the same evening (both skeletons, Mind#493, Cortex#60, Pulse#33); Heart#292 blocked by a pre-existing Brain#499 test break (bug drafted), .github#34 awaiting an explicit merge OK (no CI). Both repos now carry AGENTS.md + hooks on main; RAL clones at the skeleton heads. B1 DONE 2026-10-08: Heart#292 and .github#34 merged (Heart#292 unblocked by PyAutoHeart#293, record `complete/2026/10/heart-dashboard-markdown-link-test.md`); record `complete/2026/10/search-ext-b1-registration.md`. A0c part 1 prompt FILED (`draft/docs/autofit/search_extensibility_a0c_fit_repair.md`), plan presented 2026-10-07 evening and APPROVED by the human 2026-10-08 with the ruling that the superseded `autofit_workspace_developer/searches/nss/` directory is deleted via Gut (recoverable ref), not bannered; part 2 = downstream ghost sweep, to file after part 1. A0c part 1 ISSUED 2026-10-08 as PyAutoFit#1668 (task `search-ext-a0c-fit-repair`) and MERGED the same day as 9 PRs (PyAutoFit#1669 pending-release; ws#168; ws_test#107/#108; dev#29; assistant#55; Brain#502/#503); record `complete/2026/10/search-ext-a0c-fit-repair.md`; NSS dev dir condemned (`condemned.md`). Found: Drawer crashes under NullPaths (bug draft filed). Human launched `--auto` for all A0 phases 2026-10-08. A0c part 2 FILED+ISSUED as PyAutoLens#776 (task `search-ext-a0c-downstream`, tier glance) and MERGED the same day as 9 PRs (PyAutoLens#777, PyAutoGalaxy#652, PyAutoCTI#115 pending-release; HowToLens#97, HowToGalaxy#86, autogalaxy_workspace#257, autocti_workspace#37, autolens_assistant#157, autogalaxy_assistant#34), record `complete/2026/10/search-ext-a0c-downstream.md`; A0c DONE. A0b ISSUED as PyAutoFit#1670, SHIPPED as PyAutoFit#1672 (judge, awaiting human /prm; retires the Drawer NullPaths bug draft; kwarg-typos follow-up filed `draft/bug/autofit/search_kwarg_typos_in_workspace_scripts.md`). A0a(ii) ISSUED as PyAutoFit#1671 (planned, blocked-by A0b; implemented stacked on A0b's branch). A0b MERGED 2026-10-08 (PyAutoFit#1672, 1d43b668; record `complete/2026/10/search-ext-a0b-hygiene.md`) and A0a(ii) MERGED after it (PyAutoFit#1673, cf1acd72; record `complete/2026/10/search-ext-a0a2-backend-conformance.md`, 6 strict xfails → A3/A4). ALL OF A0 DONE. Human launched A1 and B2 under `--auto` 2026-10-08: A1 ISSUED PyAutoFit#1674, SHIPPED PyAutoFit#1675 (+ docs PyAutoLens#778/PyAutoGalaxy#653/PyAutoCTI#116), Codex astra adversary review enacted (6 findings), MERGED 2026-10-08 (record `complete/2026/10/search-ext-a1-declare-gate.md`; `search-manifest@1`, `run(ctx)` design note frozen). B2 ISSUED autofit_inference#2, SHIPPED autofit_inference#3, Codex adversary review enacted (12 findings; reference rebuilt), MERGED 2026-10-08 (record `complete/2026/10/search-ext-b2-harness.md`; protocol `gaussian_x3@1`; numpy Nautilus reference; JAX + separated references pending for B3). Next: A2 ∥ A3 (A3b after both), B3 pilot. Survey findings folded into the A0a(i) plan: NUTS/SMC `search.json` round trip fails today (kind-string `inverse_mass_matrix`), the Emcee/NUTS/SMC construction mutation targets `output.search_internal` (invisible under the test config), only the jax family is absent on `unittest-nojax` (nautilus/zeus/emcee/dynesty stay installed), no capability attributes exist yet. Next after A0a(i): A0c and B1 registration, then A0b → A0a(ii).

2026-10-08 evening: A2 (PyAutoFit#1679), A3 (#1680), A3b (#1681, after an NSS witness PASS) and B3 (autofit_inference#5, PyAutoInsight#23, PyAutoCortex#61; wrap-up with no more compute, 223 of 520 pilot rows) all MERGED and closed out. Records are `complete/2026/10/search-ext-{a2-objective-bridge,a3-samples-checkpointer,a3b-nss-preflight,b3-pilot}.md`. Post-merge Codex gpt-6-astra reviews of everything after the A1 review: `search_extensibility_epic_reviews/05_codex_astra_a2_a3_a3b_postmerge.md` (FINDINGS, 7) and `06_codex_astra_b3_postmerge.md` (FINDINGS, 6). Nothing enacted yet; see Resume.

## Heart recovery handoff (2026-10-10 — read before resuming)

The human paused Scientist adoption to repair Heart, then authorized the bounded
repair scopes under exact RED `release validation FAILED (stage integrate)`.
The October 10 rehearsal (Heart run 38038078541, version 2026.10.10.1.dev81101)
used PyAutoFit main 7d056728c: 726 pass / 2 fail / 85 skip; install A–F pass.
These are downstream adoption gaps from **already merged** A1/A2, not unfinished A4:

- autofit_workspace_test#109, task `heart-fitness-dispatch`: explicit JAX analysis
  plus behavioral scalar/batched objective, compile reuse and pickle assertions.
  Before: assertion failure; after: release-profile script PASS (6.4s).
- autolens_workspace#588, task `heart-hierarchical-backend`: imaging analyses use
  NumPy consistently with the existing graph and hierarchical factor. Before:
  backend-agreement SearchException; after: release-profile script PASS (20.7s).
  Matching notebook regenerated. No PyAutoFit library changes.
- Mind#497, task `heart-manifest-drift`: independent generated guidance/table
  drift; DNA missing files already fixed by merged DNA#1 and local main synced.

All 14 repair PRs merged on 2026-10-10 under human `/prm`. Workspace PRs
[autofit_workspace_test#110](https://github.com/PyAutoLabs/autofit_workspace_test/pull/110)
and [autolens_workspace#589](https://github.com/PyAutoLabs/autolens_workspace/pull/589)
passed every configured CI run/job, including both Python 3.12/3.13 smoke legs.
Local smoke: fitness 15 scripts; Lens 41 scripts + 2 notebooks; independent
CLEAN reviews. All twelve manifest PRs linked in Mind#497 merged; Cortex,
.github and public hub had no CI checks and received explicit human approval.
Full generator check, 946 tests and independent CLEAN review passed.

Completion records (original prompts folded; issues closed and claims released):
- [Fitness dispatch](../../../complete/2026/10/heart-fitness-dispatch.md)
- [Hierarchical backend](../../../complete/2026/10/heart-hierarchical-backend.md)
- [Manifest drift](../../../complete/2026/10/heart-manifest-drift.md)

Do not repeat these repairs or change another session's retained B3 pilot
output worktree. Fresh supported wheel integration remains outstanding; the
last authoritative failed run is still 38038078541. No release/rehearsal was
performed or authorized. Scientist adoption and Broca expansion plans remain
unchanged and paused pending Heart recovery.
**Review 05/06 findings below remain unresolved and retain their release/wave-2
constraints.** These workspace repairs do not claim to fix legacy pickle,
preflight, checkpoint finalization, or the inference evidence findings.
Heart only clears through merged fixes plus fresh supported wheel integration
and re-ingest; local passes do not make release readiness GREEN.

## Resume (2026-10-08 night — start here)

Both post-merge astra reviews returned FINDINGS. None has been enacted. **The PyAutoFit pending-release PRs (#1679/#1680/#1681) must not ship in a release until the release blockers in the first list are fixed.** Verify each finding against current main before fixing it; earlier astra findings all reproduced. Then do A4 or B4 (the human chooses).

**PyAutoFit, A2/A3/A3b follow-up** (review 05 §3; suggested single task `search-ext-a3-postmerge-fixes`, library):
1. [blocker-for-release] Unpickling an old `Fitness` silently enables JIT (`fitness.py:965` `__setstate__`): keep `use_jax_jit=False` eager, and add a pickle-from-A1 regression test. (F1, P1)
2. [blocker-for-release] Preflight validates the declared config, not the resolved runtime config (`preflight.py:147,181`). It wrongly rejects `use_jax_jit=False` eager likelihoods and the `gradient_mode="reverse"` override. Resolve the execution settings once and share them between preflight and sampling. (F3)
3. [blocker-for-release] `.completed` is written before the archive finalizes (`abstract_search.py:966,1215`), and NSS deletes its resume state before result processing (`nss/search.py:541`). A failed archive write therefore leaves an unrecoverable "completed" fit. Finalize first and recover on rerun. This predates A2 but is in scope. (F2, P1)
4. [blocker-for-release] Calling `_fit` directly with no active factory builds `PoolFactory(self)` without the analysis (`abstract_search.py:1487,2012`), so Nautilus JAX can fork with 2 cores. Pass the analysis, and assert that no fork happens. (F4)
5. [before-A4] `FitContext` leaks pools that the context created when a fit succeeds (`fit_context.py:139`), and `ctx.update` never saves the checkpoint strategy (`fit_context.py:125`). Both violate the frozen run(ctx) contract. Test with a resumable toy search on both exit paths. (F5, F6)
6. [before-A4] The shape-only golden diagnostics pass even when ESS/R-hat are set to -999 (`test_golden_samples.py:104`). Add value-sensitive tests of where the diagnostics come from, and keep the CSV tolerance. (F7)
7. [blocker-for-release] Run disk-backed checks in a writable environment: loading pre-release output folders, interruption and resume, and zipped restore.
8. [later] Consolidate the remaining backend-specific lifecycle paths: Drawer's dill, Nautilus's own pool context, NSS deleting its checkpoint.

**autofit_inference / Insight, B3 follow-up** (review 06 §3; suggested task `search-ext-b3-postmerge-fixes`; all before wave 2 or B5):
1. [before-wave-2] Fix the contradictory freeze instructions (protocol §7 `:160`, `state.md:62`, Insight `campaigns.yaml:96`). Freeze `@2` before any scored run on the calibration that already exists; do not restart the pilot. Keep the A2+A4 gate for scored wave 2. (P1)
2. [before-wave-2] The bootstrap wall-per-success intervals throw away zero-success resamples (`build_catalogue.py:129`). Keep them as unbounded and regenerate the 4 affected cells. (P1)
3. [before-wave-2] A failed warm-start provider loses its elapsed cost (`_runner.py:825,512,873`), and unknown cost is coerced to 0 in `leg_summary`. Persist the provider time in a `finally`.
4. [before-wave-2] The exporter omits `provider_wall_s`/`warm_start` (`export_inference_summary.py:208`), so the Insight "Total s" shows consumer-only time (73.7 s vs 1150.2 s). Export and display the combined cost.
5. [before-wave-2] Convergence silently drops a stuck parameter whose R-hat/ESS are NaN (`_posterior.py:285`). Require valid diagnostics for every free parameter.
6. [before-B5] Refresh the Insight `fit` snapshot from autofit_inference ≥ 900648b5c, and check that the board shows 223 records; add an acceptance check on the producer revision and record count.
7. [before-B5] Wave-2 infrastructure: a scored-wave manifest identity that includes data realization, protocol and library revision (`_pilot.py:164`), per-realization references, versioned judging, and missing-vs-deferred attempt accounting.
8. [later] Reassessment provenance: the raw row verdicts (14/33/176) differ from the rejudged ones (35/110/78), so record the reference/offset revision. Rerun the tests that the read-only sandbox blocked.

**Other open items carried forward:**
- The B3 worktree `~/Code/PyAutoLabs-wt/search-ext-b3-pilot` holds 1.2 GB of worktree-only pilot output; the human needs to decide what to do with it before `worktree_remove`.
- Draft `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md`.
- Draft `draft/feature/autofit_inference/nss_settings_for_wave2.md`.
- Optional A0a(ii) gap: skips on full-extras CI legs when blackjax/optax are missing.
