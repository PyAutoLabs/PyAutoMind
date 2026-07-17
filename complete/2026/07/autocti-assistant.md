- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/136 (closed)
- completed: 2026-07-17
- repo-born: https://github.com/PyAutoLabs/autocti_assistant (PUBLIC — flipped 2026-07-17 on human approval after Heart newborn-validation legs 1-4)
- pr-phase0: https://github.com/PyAutoLabs/PyAutoBrain/pull/137 (merged 8db0c8e) + https://github.com/PyAutoLabs/autolens_assistant/pull/76 (merged dfa07b1)
- pr-phase1: https://github.com/PyAutoLabs/autocti_assistant/pull/1 (seed-infra, merged)
- pr-phase2: https://github.com/PyAutoLabs/autocti_assistant/pull/2 (ac_* skills, merged 557ba0b)
- pr-phase3: https://github.com/PyAutoLabs/autocti_assistant/pull/3 (wiki, merged f061651)
- pr-phase4: https://github.com/PyAutoLabs/autocti_assistant/pull/4 (demonstrations, merged 1337a68)
- summary: Built autocti_assistant, the CTI-calibration domain assistant cell, as a lightweight-seed clone of autolens_assistant via the Clone Agent. 5 phases, one PR-set each, all merged 2026-07-17; repo flipped PUBLIC on human approval. Phase 0 unblocked the birth: 39 files in the reference cell (euclid mode, JOSS paper, .mcp.json, cosmos_web_ring scripts) matched no template-boundary pattern and hard-failed clone --apply (exit 4), blocking EVERY future assistant birth — classified in both _clone.py's REFERENCE_PROFILES and maintainer.md's owning prose, plus a per-PR CI guard (check_boundary.py + clone-boundary.yml) so the author who adds a file classifies it. Phase 1 birthed the seed (born private via clone_seed.py) and fixed two seed-infra boundary leaks (wiki-currency installed autocti from PyPI — the autolens shape — vs source+arcticpy; audit probed autogalaxy, not a CTI dep). Phase 2 authored 9 ac_* skills grounded in the 118 validated autocti_workspace scripts (setup incl. arcticpy, workspace-nav, simulate 1D/CI, mask+extract, fit incl. the factor-graph joint fit, correct, plot function-API, aggregator), all audit-clean, baseline written. Phase 3 authored wiki/core (6 CTI concept pages) + wiki/literature (8-paper bibliography VERIFIED via web search vs arXiv/ADS — Massey 2010/2013/2014, Anderson&Bedin 2010, Israel 2015, Short 2013, Skottfelt 2017 — 6 source pages + 3 entities) + wiki/project/state.md; privacy seam held (PyAutoMemory wiki/cti consulted for structure/pointers only, all content written from public knowledge, never copied). Phase 4 authored + RAN 4 demonstrations that recover the input trap models for real (1D density 0.13→0.1323 release 1.25→1.261; 2D CI 0.13→0.1334 1.25→1.312; correction trail 3.9x suppressed; aggregator round-trip) and de-lensed the llms.txt cold-session front door.
- clone-decision: mode = lightweight-seed, FORCED (exact-clone/differentiated-sibling are v2/unimplemented, exit 5); reference autolens_assistant; born PRIVATE, flipped public only after Heart legs 1-3 + demonstrations. Epic filed on PyAutoBrain (not PyAutoCTI — intake trap; PyAutoCTI is a consumed dependency) per the pyautoscientist-3b-clone precedent.
- grounding-corrections: aggregator is ac.agg.CTIAgg not Dataset1DAgg (both exist); plot scripts at scripts/plot/ not per-geometry; Short 2013 = arXiv:1302.1416, Israel = 1506.07831 (web-verified, not memory). Real 1D API: Clocker1D(express=), TrapInstantCapture(density=,release_timescale=), CTI1D(trap_list=,ccd=), SimulatorDataset1D.via_layout_from, Mask1D.masked_fpr_and_eper_from, layout.extract.eper/fpr.*, af.AnalysisFactor+FactorGraphModel, search.fit(model=fg.global_prior_model)→result_list, clocker.remove_cti.
- traps: (1) the audit/idiom checker trips on a DEFUNCT symbol or idiom written in PROSE to say it's gone (aplt.Output, 'analysis + analysis', wildcard aplt.subplot_*) — rephrase so no live-looking token; (2) --check-citations checks ONLY code Project:path cites, NOT markdown links — a separate link sweep is needed and caught systematic relative-path depth errors (3-deep concepts/ needs ../../../skills/, sources/ needs ../../core/); (3) factor-graph fits store results PER-FACTOR — the aggregator's max_log_likelihood_instance is None and CTIAgg errors ('ModelInstance' has no 'cti'); use samples.max_log_likelihood()[0].cti; (4) PYTHONPATH must APPEND PyAutoCTI (ambient has the editable checkouts but omits it) — replacing it silently drops autoarray/autofit to old site-packages and the gate passes vacuously; (5) a demonstration must ACTUALLY recover — demo2 first cut (2 noisy levels) recovered density but not release timescale (→2.90); fix the DATA (more clean levels), never the assertion; (6) profile.md is the on-demand USER profile (session-start reads it) — project state goes in wiki/project/state.md.
- systemic-finding: autolens_assistant's "generic" tier has absorbed lensing-stack assumptions at every layer — file classification (the 39), the audit's autogalaxy, the wiki-currency PyPI-install shape, and content in _bootstrap_skill.md, wiki/README, llms.txt, scripts/AGENTS.md. Load-bearing ones de-lensed as hit; the DURABLE fix is reference-side (domain-parameterize or reclassify vs _clone.py so future births don't re-hit it) — worth its own prompt against autolens_assistant + _clone.py. Only surfaceable by a real birth.
- follow-ups-open: (a) reference-side systemic de-lensing of the generic tier (above); (b) scripts/AGENTS.md still carries lensing SLaM-pipeline content (needs a CTI-pipeline rewrite — went public with it, minor); (c) PyAutoBrain test suite never runs in CI (10+ test files, only docs.yml + nightly — that's why Phase 0's guard went into autolens_assistant CI); (d) the CTI release train remains unwired (draft/release/autocti/cti_release_train_wiring.md, human-required) so PyPI serves a pre-resurrection wheel and the assistant installs from source.
- epic: COMPLETE — a working, documented, validated, PUBLIC CTI assistant: 9 grounded skills, a CTI reference + verified literature wiki, 4 demonstrations that recover input traps, honest cold front door; publish-gate legs 1-4 passed. Clone Agent v1 (--apply lightweight-seed) proven end-to-end on its second real birth (after ic50_assistant).

## Original prompt

# Build autocti_assistant — the CTI calibration domain assistant cell

Type: feature
Target: autocti_assistant
Repos:
- @autocti_assistant
- @PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Build **autocti_assistant**, the science-assistant cell for CTI calibration with
PyAutoCTI, seeded from the mature reference assistant cells. This follows the
CTI resurrection epic (all six phases merged 2026-07-17 — PyAutoCTI,
autocti_workspace and autocti_workspace_test are fully modern:
`complete/2026/07/cti-resurrection-phase{0..5}.md`), which makes the domain
assistant the natural next organ of the CTI cell line.

## Original request (verbatim)

> can you draft the prompt to write the autocti_assistant, which il will run in
> opus

## Routing / gates (read before starting)

- **Route through the Clone Agent** (`/clone`) at start_dev time for the
  CloneDecision: exact-clone vs sibling vs seed. `autolens_assistant` is the
  mature reference cell (library-domain assistant, closest shape);
  `autofit_assistant` and the ic50_assistant build
  (`complete/2026/07/build_ic50_assistant_from_autofit_assistant.md`) are the
  precedent runs of this playbook.
- **Repo creation is a human interactive gate** — ask name / org / visibility
  as a dedicated question before any `gh repo create`. Suggested default:
  `PyAutoLabs/autocti_assistant`, public (matching autolens_assistant /
  autofit_assistant).
- **Privacy seam**: PyAutoMemory (`wiki/cti/` — trap physics, the arctic
  algorithm, Euclid VIS / HST ACS heritage, per-topic source bibliographies) is
  the user's private knowledge base. Consult it (via the memory faculty) for
  *pointers and structure*, but a public assistant wiki must be **rebuilt from
  the public literature** with verifiable citations — never copy PyAutoMemory
  pages into a public repo. Bib entries verbatim from the literature; validate
  with the assistant `--check-citations` tooling + link CI (the
  autolens_assistant PR#41/#42 pattern).
- **Intake-classification trap** (hit on the ic50 build): bare library mentions
  steal Target — this is a **new assistant cell**, not a PyAutoCTI change.
  PyAutoCTI is a consumed dependency.
- **Judgment tier throughout**: skills and wiki prose are the product (this is
  why it runs in Opus). Mechanical validation runs may be delegated.

## Ground truth the assistant must teach (post-resurrection API only)

Everything is grounded against the live stack — grep
`autocti_workspace/scripts/` (all 118 scripts validated 2026-07-17) and
`PyAutoCTI/AGENTS.md`, never memory of the old API:

- **Plotting is the matplotlib function API**: `aplt.subplot_dataset_1d`,
  `aplt.subplot_imaging_ci`, `aplt.figure_*`, `aplt.plot_array`/`plot_yx`,
  `aplt.plot_cti_1d`, `*_list` combined subplots. There are **no**
  `*Plotter` / `MatPlot*` / `Visuals*` objects.
- **Multi-dataset fits are factor graphs**: `af.AnalysisFactor(prior_model=
  model, analysis=...)` per dataset → `af.FactorGraphModel(*factors)` →
  `search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)`;
  results come back as a list (`result_list[0].max_log_likelihood_fit`).
  Analysis summing (`analysis + analysis`) no longer exists.
- **arcticpy install recipe** (a top-3 user question, guaranteed): needs
  `libgsl-dev` + a C++ toolchain; `pip install numpy cython` first, then
  `pip install arcticpy==2.6 --no-build-isolation --no-deps` — a naive pip
  install **downgrades numpy below 2.0**. No-root header workaround in
  `PyAutoCTI/AGENTS.md`; CI form in
  `autocti_workspace_test/.github/scripts/smoke_install.sh`.
- **Test/fast-mode conventions**: the knob is `PYAUTO_TEST_MODE` (2 = sampler
  bypass; `PYAUTOFIT_TEST_MODE` does not exist). Known artifact: identical-
  prior ordered-trap models tie at prior medians under the bypass and raise
  their own assertion (filed autofit issue) — real runs are fine.
- **Domain surface**: `Dataset1D` / `ImagingCI`, `Layout1D`/`Layout2DCI` +
  Region objects, FPR/EPER extraction (`layout.extract`, region strings
  `"fpr"/"eper"` in 1D and `"parallel_fpr"`… in 2D), `Clocker1D(express=, roe=)`
  vs `Clocker2D(parallel_express=, parallel_roe=)` (different kwargs!),
  `CTI1D`/`CTI2D`, trap species + `CCDPhase`, correction
  (`remove_cti`), noise scaling / hyper fits, the aggregator
  (`ac.agg.Dataset1DAgg` etc. over the consolidated `dataset.fits` format).

## Scope sketch (to be firmed at start_dev / clone-agent time; expect phases)

1. **Seed the cell** from the CloneDecision's reference: AGENTS.md (persona:
   CTI-calibration assistant; include the chat handshake — "chat use requires
   the GitHub connector; tell me if you can actually read the repo"),
   CLAUDE.md pointer, config, citation/link tooling, Makefile/activate
   conventions (mind the venv trap: clear PYTHONPATH).
2. **Skills** (`skills/ac_*.md`, grounded per-skill against
   autocti_workspace's validated scripts): install (incl. arcticpy),
   simulate 1D + charge injection, compose + fit a CTI model (single and
   factor-graph multi-dataset), masking + FPR/EPER extraction, correction,
   plotting (function API), results + aggregator, workspace navigation,
   test-mode/fast-run conventions.
3. **Wiki**: `wiki/core/` (what CTI is, trap physics, FPR/EPER anatomy, the
   arctic algorithm, calibration strategy, parallel vs serial) and
   `wiki/literature/` (concepts/entities/sources for: Massey/Israel-line CTI
   correction, the arctic papers, Euclid VIS CTI calibration, HST ACS CTI
   history, trap pumping, CTI as a weak-lensing shape systematic) — public
   sources only, every citation verified.
4. **Project profile** (`wiki/project/profile.md`): the resurrection state,
   what is and is not wired (release-train wiring pending —
   `draft/release/autocti/cti_release_train_wiring.md`), Euclid heritage in
   `autocti_workspace_test/legacy/`.
5. **Demonstrations** (the assistant must be able to drive these end-to-end,
   and they double as its validation): simulate + calibrate a 1D dataset
   (recover the input trap density/timescale), simulate + calibrate a small
   charge injection image, correct a dataset and show the residual
   improvement, load results through the aggregator and plot.
6. **Validation**: `--check-citations` clean, link CI green, the demonstration
   fits run, and a cold-session smoke ("new Opus session + this repo only"
   answers an install question and a calibration question correctly).
