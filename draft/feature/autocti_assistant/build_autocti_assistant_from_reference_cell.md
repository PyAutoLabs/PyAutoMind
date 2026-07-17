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
