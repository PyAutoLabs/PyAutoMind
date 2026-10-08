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

B1 human gate passed 2026-10-07 (both repos created, empty). A0a(i) prompt filed 2026-10-07 at `draft/test/autofit/search_conformance_metadata_layer.md`; plan approved by the human 2026-10-07 (ruling: identifiers stay the same; any identifier change is flagged first); ISSUED as PyAutoFit #1666 (https://github.com/PyAutoLabs/PyAutoFit/issues/1666), task `search-conformance-metadata` in active.md, worktree `~/Code/PyAutoLabs-wt/search-conformance-metadata` on `feature/search-conformance-metadata`; PyAutoFit claim released from community-pages (its #1663 merged). MERGED 2026-10-07T20:37Z (PR https://github.com/PyAutoLabs/PyAutoFit/pull/1667, pending-release; record `complete/2026/10/search-conformance-metadata.md`); 3066 passed / 5 strict xfails locally, no-jax leg emulated; the 5 xfails are the A0b (NUTS/SMC round trip) and A3 (Emcee/NUTS/SMC config mutation) repairs. A0a(i) DONE. B1 registration ISSUED 2026-10-07 as PyAutoMind#492 (task `search-ext-b1-registration`, 6-repo worktree + org .github branch `feature/search-ext-b1-registration`); human approved the plan, Mind coordination with mind-dashboard-simplify (#491), RAL clones, and the deviation that NO Pulse/Insight registry rows land at B1 (both organs' `check` fail an instance without a published summary; the `fit` rows land in B4a/B3). Cortex row is `planned` (no ledger until B3). SHIPPED 2026-10-07 as 7 PRs: autofit_inference#1, autofit_profiling#1, Mind#493, Heart#292, Cortex#60, Pulse#33, .github#34 — 5/7 MERGED the same evening (both skeletons, Mind#493, Cortex#60, Pulse#33); Heart#292 blocked by a pre-existing Brain#499 test break (bug drafted), .github#34 awaiting an explicit merge OK (no CI). Both repos now carry AGENTS.md + hooks on main; RAL clones at the skeleton heads. B1 DONE 2026-10-08: Heart#292 and .github#34 merged (Heart#292 unblocked by PyAutoHeart#293, record `complete/2026/10/heart-dashboard-markdown-link-test.md`); record `complete/2026/10/search-ext-b1-registration.md`. A0c part 1 prompt FILED (`draft/docs/autofit/search_extensibility_a0c_fit_repair.md`), plan presented 2026-10-07 evening and APPROVED by the human 2026-10-08 with the ruling that the superseded `autofit_workspace_developer/searches/nss/` directory is deleted via Gut (recoverable ref), not bannered; part 2 = downstream ghost sweep, to file after part 1. Next: A0c part 1 (start_dev 2026-10-08); A0b → A0a(ii) after #1667 merges. Survey findings folded into the A0a(i) plan: NUTS/SMC `search.json` round trip fails today (kind-string `inverse_mass_matrix`), the Emcee/NUTS/SMC construction mutation targets `output.search_internal` (invisible under the test config), only the jax family is absent on `unittest-nojax` (nautilus/zeus/emcee/dynesty stay installed), no capability attributes exist yet. Next after A0a(i): A0c and B1 registration, then A0b → A0a(ii).
