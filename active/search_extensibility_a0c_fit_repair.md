# Search documentation and coverage repair, fit family + Brain (epic search-extensibility, phase A0c part 1)

Type: docs
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace
- autofit_workspace_test
- autofit_workspace_developer
- autofit_assistant
- PyAutoBrain
Themes:
- searches
- documentation
- jax
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: search-extensibility
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1668
Filed: 2026-10-07

Phase A0c of the search-extensibility epic (`draft/research/autofit/search_extensibility_epic.md`;
plan in `search_extensibility_epic_report.md` §4 A0c; item list in
`search_extensibility_epic_surveys/03_search_docs.md` §4, re-verified against main on
2026-10-07 by an Opus survey). A0c is split in two issues because it spans sixteen repos:
**part 1 (this prompt)** repairs the fit family and the Brain, where the search facts
originate; **part 2** sweeps the downstream PySwarms/MultiNest ghosts and "LBFGS only"
claims in PyAutoLens/PyAutoGalaxy/PyAutoCTI docs, HowToLens/HowToGalaxy, autogalaxy_workspace,
autocti_workspace and the al/ag assistants. Human ruling 2026-10-07: the RTD generic
example stays DynestyStatic.

## Original request (verbatim from the epic plan)

"A0c, documentation and coverage repair (surveys/03 phase 1; 'repair', not docs-only, D8).
Scope: the surveys/03 §4 list: (1–2) add Nautilus, NSS, Drawer and MultiStart×4 to
docs/api/searches.rst, and add a Nautilus cookbook section plus its workspace mirror; (3–4)
remove the stale NSS claims from the workspace README and llms.txt:28, and mark
autofit_workspace_developer/searches/nss as superseded; (5) delete the per-search-YAML claims
×7; (6–7) purge PySwarms and MultiNest ghosts from docs, CITATIONS and the bib, and add
blackjax, optax and prodigy to files/citations.bib; (8) fix the optional_requirements.txt
reference; (9) fix the staleness in af_configure_search.md; (10) fix the SamplerSurface
gap-rule bugs: false positive for MultiStart, false negatives for SMC and BFGS, and NSS
double-counted; (11) fix the sampler_pipeline Boundary → autolens_inference; (12) fix the
duplicated ag __Start Point__ header and the HowToLens/Galaxy 'LBFGS only' claims; correct the
'use_jax=False is required by LBFGS' line (mle.py:84). Separate PRs within A0c:
workspace_test integration scripts for SMC, Drawer and BFGS (executable); the Brain
SamplerSurface class-keyed gap fix (item 10, parser code); and a 'Stage 5 — documentation'
in sampler_pipeline/reference.md, using the surveys/03 §3 blast radius as the interim
checklist. Shape: one PR per repo for the prose repairs, plus the separate PRs above."

## Scope, part 1 (verified 2026-10-07 against main)

- **PyAutoFit** (`docs/api/searches.rst:27-28,55-56` + 7 `_autosummary` stubs; `docs/cookbooks/search.md`
  Nautilus section between DynestyStatic and LBFGS, soften "every search" at :20;
  `autofit/config/non_linear/README.md` (says PyAutoLens, lists mcmc/nest/mle.yaml — only GridSearch.yaml exists);
  `docs/general/configs.md:3`; `docs/installation/source.md:18,37` (both `requirements.txt` files are missing →
  `pip install -e PyAutoFit` / `-e "PyAutoFit[optional]"`); `files/citations.{bib,md,tex}`: drop multinest/pymultinest,
  add blackjax (Cabezas+ 2024, arXiv:2402.10797), optax, prodigy (Mishchenko & Defazio 2023, arXiv:2306.06101),
  add Nautilus to .md/.tex, fix the `[@sqlite]`→`sqlite2020` key).
- **autofit_workspace** (`scripts/cookbooks/search.py` Nautilus mirror + contents bullet; `scripts/searches/README.md:5-7`
  roster (add BlackJAXNUTS, MultiStartAdam; drop NSS) and delete the `:10-22` "When to use NSS"/`autofit[nss]` block;
  `llms.txt:28` drop NSS; `scripts/searches/mle.py:84-85` — LBFGS runs under JAX (`bfgs/search.py:298-306` calls
  `fitness._jit`; gradients stay finite-difference), so reword as "either backend; use_jax=False here for speed;
  MultiStartAdam below requires use_jax=True"). Regenerate notebooks.
- **autofit_workspace_test** (`config/non_linear/README.md:6-8`), and the **separate scripts PR**: executable
  `scripts/searches/{SMC,Drawer,BFGS,MultiStartADABelief,MultiStartLion}.py` modelled on `BlackJAXNUTS.py`/`LBFGS.py`/
  `MultiStartAdam.py`, run on demand, not added to `smoke_tests.txt`.
- **autofit_workspace_developer** (`searches/nss/`: library copy is live and has diverged → superseded; root
  `README.md` archive definition).
- **autofit_assistant** (`skills/af_configure_search.md:3,21-26,103-105,117` — roster missing NSS/SMC/BFGS/MultiStart×4,
  stale "until the core wiki lands", per-search YAML claim, "HowToFit chapter 2" → `chapter_1_introduction/tutorial_3_non_linear_search`;
  `wiki/core/concepts/non_linear_search.md:57`; `wiki/core/stack/autonerves.md:18`; `config/non_linear/README.md:6-8`).
- **PyAutoBrain**, two separate PRs: (B) `agents/faculties/samplers/_samplers.py` gap rule keyed on exported class names
  (parse `autofit/__init__.py` exports + `_LAZY_ATTRS`), class-vs-integration-stem match with `_jax` stripped, archive names
  that are also promoted excluded, `searches_minimal` variant suffixes (`_mlp`,`_profile`,`_sweep`) handled, plus a unit
  test; verify with `bin/pyauto-brain samplers` (there is no `gaps` verb). (C) `skills/sampler_pipeline/{SKILL.md,reference.md}`:
  Boundary → `autolens_inference` (`SKILL.md:73,111-113`, `reference.md:98,113`), drop the `[nss]` extra and
  config-mirroring lines (`reference.md:142,146-149`), add "Stage 5 — documentation" after Stage 4 using `surveys/03 §3`
  as the checklist, "Stages 3–5" at `SKILL.md:88-91` and `reference.md:184`.

## Out of scope (part 2)

PyAutoLens/PyAutoGalaxy/PyAutoCTI docs + CITATIONS ghosts, HowToLens/HowToGalaxy "LBFGS only", autogalaxy_workspace
duplicate `__Start Point__` (`guides/modeling/searches.py:336`), autocti_workspace and al/ag assistant config claims.

## Verification

GitHub docs legs (RTD floor is red on an autonerves pin — judge from the GitHub legs); `grep -ri pyswarms\|multinest`
over PyAutoFit `docs/` and `files/` empty; autofit_workspace smoke `searches/{mcmc,nest,mle}.py` + cookbook; the five new
workspace_test scripts run under `PYAUTO_TEST_MODE=1`; Brain tests + `bin/pyauto-brain samplers` tier-gaps section
reports only Drawer-style true gaps; `repos_sync --check`.

## Witness

All 15 searches appear in `docs/api/searches.rst`; the Brain samplers tier-gaps section has no false positive for
MultiStart, SMC or BFGS and NSS appears once; `grep -ri pyswarms` over PyAutoFit `docs/` returns nothing.
