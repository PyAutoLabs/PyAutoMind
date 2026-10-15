# `@PyAutoFit` A5 (consumers): generate rosters, tiers and anchors from the pinned search manifest

Type: refactor
Target: autofit
Repos:
- PyAutoHands
- PyAutoBrain
- PyAutoMemory
- autofit_assistant
- autolens_assistant
- autogalaxy_assistant
- autofit_workspace
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Epic: search-extensibility
Phase: A5-consumers
Witness: `python -m autofit search-manifest --json` pinned to the installed `autofit.__version__` regenerates every roster block byte-identically (`--check` mode in each consumer); the Hands navigator `--roster` mode writes the fenced roster block in the curated `llms.txt`; the af/al/ag assistants' roster blocks regenerate from the same manifest; Brain's SamplerSurface keys tiers by registry class; workspace CI checks the registry `example`/`integration_test` anchors against the pinned version, not `main`; al/ag `guides/modeling` search guidance collapses onto domain advice plus a matrix link; the capability matrix links each row to its B3 catalogue card.
Review-minutes: 30
Unattended: needs-slicing
Filed: 2026-10-14
Issued: 2026-10-15

Unblocked 2026-10-15: 2026-10-15: search-ext-a5-library merged (PyAutoFit#1689 → #1690 → #1691 → #1692, record `complete/2026/10/search-ext-a5-library.md`; pending-release — consumers pinned to the installed `autofit.__version__` need a PyAutoFit release carrying them)

Authority: epic report "#### A5" consumer bullets (D18: consumers generate from the versioned manifest pinned to the installed version), `search_extensibility_epic_surveys/03_search_docs.md` "Phase 3 — consumers generate". Library half: `complete/2026/10/search-ext-a5-library.md` (new-search template `search/_template/search.py`). Survey the actual consumer file names first (the report's `guides/modeling/searches.py` path does not exist in the current workspaces; find the live equivalents and the Brain samplers faculty surface) and record them in the plan. One PR per repo; Hands and Brain first (generators), then the assistants and workspaces.

## Facts from the 2026-10-15 survey (PyAutoFit main 3f4699b95; do not re-derive)

- Manifest: `python -m autofit search-manifest --json` (`autofit/__main__.py`), schema `search-manifest@1` (`autofit/non_linear/search/registry.py:36`), top-level `{schema, autofit_version, families, capability_attributes, searches}`; per search `name, class_path, family (mcmc|nest|mle), lazy, requires, example, integration_test, capabilities{...}`; capability keys in `capabilities.py:165-185` (`status` stable|experimental is the only tier-like field; there is no `tier`). 15 searches: Emcee, Zeus, BlackJAXNUTS, SMC | DynestyStatic, DynestyDynamic, Nautilus, NSS | Drawer, BFGS, LBFGS, MultiStartAdam/ADABelief/Lion/Prodigy. Anchors: `example` = `autofit_workspace:scripts/searches/{nest,mcmc,mle}.py#Search: <Name>` (None for SMC, NSS, BFGS, MultiStartADABelief/Lion/Prodigy); `integration_test` = `autofit_workspace_test:scripts/searches/<Name>.py` for all 15. `test_registry.py:121-127` checks anchor FORMAT only; nothing resolves them across repos. Existing manifest consumer: `docs/_generate_searches.py` (capability matrix `docs/searches/index.rst`, linked from PyAutoLens/PyAutoGalaxy docs as `autofit:search_capability_matrix`). The manifest has shipped in releases since A1, so the installed release already serves it; only A4/A5 internals are unreleased.
- No repo has a generated roster today; every roster is hand-written. Surfaces: PyAutoHands `autohands/navigator.py` (writes `llms-full.txt` + `workspace_index.json`; the curated `llms.txt` is never written, no `--roster` mode) + `check_navigator.py` + reusable `.github/workflows/navigator_check.yml` + `check_search_memory.py:40-44` (hard-coded MultiStart names); autofit_workspace `llms.txt:27-31` (8-name roster), `scripts/searches/README.md:5-7`, `scripts/cookbooks/search.py:20-29`; autolens/autogalaxy_workspace `scripts/guides/modeling/searches.py` (exists, hand-written guidance; the epic citation merely dropped `scripts/`); autofit_assistant `skills/af_configure_search.md:20-23` (current 15-name roster), `wiki/core/concepts/non_linear_search.md:23-35` (STALE 7-row table; there is no `search_selection.md` — the choosing guidance is `non_linear_search.md:37+`); autolens_assistant `skills/al_configure_search.md`, `wiki/core/api/searches.md:23-165` (STALE: UltraNest, Particle Swarm; no NSS/SMC/BlackJAXNUTS), pick table :167-176 stays hand-written; autogalaxy_assistant `skills/ag_configure_search.md`, `wiki/core/api/searches.md:36-251`, `wiki/core/stack/autofit.md:53-70`; PyAutoBrain samplers faculty is the functional `digest()` in `agents/faculties/samplers/_samplers.py:299` (tiers minimal/archive/integration by script stem, promoted by AST of `autofit/__init__.py`, `gaps` by case-insensitive stem→class match with `PROTOTYPE_ALIASES`), `AGENTS.md:47-70` (env vars `PYAUTO_FIT`, `_DEVELOPER`, `_TEST`, `PYAUTO_LENS_DEVELOPER`, `PYAUTO_INFERENCE`; no `PYAUTO_FIT_INFERENCE`), `skills/sampler_pipeline/reference.md:121-155` (stage-3 promotion, no registry/template mention) and `:212-240` (lockstep list). `run_search` vs `run_point_search`: Brain `_declared_cell` matches only `run_search` (`_samplers.py:216`) and globs `scripts/*/searches/*/*.py`; autolens_inference defines `run_point_search` (`scripts/misc/searches/_point_runner.py:406`) called from `scripts/point_source/simple/baseline.py:32` with no `model_type`, so the lens mature tier is always empty; autofit_inference's `run_search` (`scripts/misc/searches/_runner.py:717`) is not scanned at all. PyAutoNerves only hand-pins backend extras in `setup_colab.py:32-76` — out of scope (optional drift check later).

## Rulings for the plan (settled here; flag in PR bodies)

1. **Source of truth = the installed release's manifest.** Every generated block carries `<!-- search-manifest@1 autofit <version> -->`; `--check` regenerates against the installed `autofit` and fails on drift. Source-main-vs-release drift is reported by a separate `--against-source <path>` mode, never a CI failure. No PyAutoFit release is needed to ship this task.
2. **One generator, in PyAutoHands** (`autohands/search_roster.py` + `regenerate_search_roster.py` / `check_search_roster.py`, wired into the reusable `navigator_check.yml` as a roster leg): renders (a) a fenced roster block for curated `llms.txt` files and assistant skill/wiki pages, (b) an anchor-resolve check that each manifest `example`/`integration_test` anchor exists in the named workspace checkout (`--workspace-root`), (c) `check_search_memory.py` reads MultiStart names from the manifest. Consumers pin the block by markers; prose outside the markers is untouched.
3. **Brain**: `digest()` keys `promoted` and `gaps` by manifest `name`/`integration_test` (AST path kept as fallback when `autofit` is not importable); add the `PYAUTO_FIT_INFERENCE` mature tier reading autofit_inference `catalogue/search_catalogue.json` cells (from the B5 scope) with `_declared_cell` accepting both `run_search` and `run_point_search`; `sampler_pipeline/reference.md` stage 3 points at the registry entry and `search/_template/search.py`; the lockstep list shrinks to the hand-written pick tables. The matching Mind `FIREWALL_ALLOWLIST` entry in `scripts/repos_sync.py` is written by the main session (Fable edits Mind), not the worker — the worker names the exact tokens it needs in the Brain PR body.
4. **Assistants**: roster blocks regenerated in `af/al/ag_configure_search.md` and the `non_linear_search.md` / `api/searches.md` catalogue name lists (stale UltraNest/Particle Swarm rows removed, NSS/SMC/BlackJAXNUTS added); pick tables and literature pages stay hand-written (literature stale names only flagged in the PR body). `af_configure_search.md` cites `autofit_inference/catalogue/search_catalogue.json` at a pinned commit (B5 scope).
5. **al/ag workspaces**: `scripts/guides/modeling/searches.py` is NOT generated; each gets a `--check` drift test that every search it names is in the manifest and a one-line link to the capability matrix; the roster in `autofit_workspace/llms.txt` + `scripts/searches/README.md` becomes a generated block.
6. **PyAutoMemory**: one page `wiki/methods/concepts/sampler-benchmarks.md` pointing at autofit_inference's catalogue and protocol ids (B5 scope), hand-written.
7. PR order, one per repo: PyAutoHands → PyAutoBrain → autofit_workspace → autofit_assistant → autolens_assistant → autogalaxy_assistant → autolens_workspace → autogalaxy_workspace → PyAutoMemory. Workspace repos' smoke CI must stay green; no notebook regeneration beyond what `generate.py` already does for touched scripts.

