# Search documentation repair, downstream sweep (epic search-extensibility, phase A0c part 2)

Type: docs
Target: autolens
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoCTI
- HowToLens
- HowToGalaxy
- autogalaxy_workspace
- autocti_workspace
- autolens_assistant
- autogalaxy_assistant
Themes:
- searches
- documentation
Difficulty: medium
Autonomy: safe
Consequence: glance
Witness: `grep -ri "pyswarms\|multinest"` over every listed repo's docs/, CITATIONS.* and config/non_linear/ returns nothing, and autocti's api/modeling.rst has no dead autosummary target
Unattended: ready
Priority: high
Epic: search-extensibility
Status: draft
Filed: 2026-10-08

Part 2 of A0c (`draft/research/autofit/search_extensibility_epic.md`; part 1 is
`complete/2026/10/search-ext-a0c-fit-repair.md`). Part 1 repaired the fit family and the Brain,
where the search facts originate. Part 2 sweeps the downstream ghosts and stale claims that
`search_extensibility_epic_surveys/03_search_docs.md` §2E, §2F and §4 items 5, 6 and 12 list,
all re-verified against main on 2026-10-08. Docs-only, no library source. Human launch 2026-10-08:
`--auto` for every A0 phase.

## Original request (verbatim from the part 1 prompt's out-of-scope list)

"PyAutoLens/PyAutoGalaxy/PyAutoCTI docs + CITATIONS ghosts, HowToLens/HowToGalaxy 'LBFGS only',
autogalaxy_workspace duplicate `__Start Point__` (`guides/modeling/searches.py:336`), autocti_workspace
and al/ag assistant config claims."

## Scope (verified 2026-10-08)

- **PyAutoLens**: `docs/index.md:123` cites PySwarms as an example search → Nautilus/Emcee.
- **PyAutoGalaxy**: `docs/index.md:147` (PySwarms example + `[@pyswarms]` key), `docs/installation/overview.md:35`
  (PySwarms listed as a dependency), `docs/general/citations.md:16` and `CITATIONS.md:14`
  ("e.g. Dynesty, Emcee, PySwarms" → "Nautilus, Dynesty, Emcee, Zeus", matching PyAutoLens).
- **PyAutoCTI**: `docs/api/modeling.rst:53-54` dead `PySwarmsLocal`/`PySwarmsGlobal` autosummary targets under
  `currentmodule:: autofit` (replace with the searches autocti actually uses: Nautilus, DynestyDynamic, Emcee);
  `docs/installation/overview.rst:48`; `docs/general/citations.rst:17`; `CITATIONS.rst:17`.
- **HowToGalaxy**: `CITATIONS.md:14`.
- **HowToLens** `scripts/chapter_optional/tutorial_searches.py:217` and **HowToGalaxy** `:205`: "PyAutoFit supports the
  LBFGS optimizer" → say LBFGS plus the MultiStart gradient optimisers (MultiStartAdam/Prodigy) the workspaces now
  default to for pixelizations, with a pointer to the workspace searches guide. Regenerate the two notebooks.
- **autogalaxy_workspace** `scripts/guides/modeling/searches.py`: duplicated `__Start Point__` header at :280 and :336
  (keep one, merge the prose); regenerate the notebook.
- **autocti_workspace** `config/non_linear/README.rst`: lists `mcmc.yaml`/`nest.yaml`/`mle.yaml` and "e.g. PySwarms";
  only `GridSearch.yaml` exists.
- **autolens_assistant / autogalaxy_assistant**: `skills/al_configure_search.md`, `skills/ag_configure_search.md`
  and `wiki/core/concepts/non_linear_search.md` — remove any remaining "per-sampler defaults live in
  config/non_linear/*.yaml" claim and add NSS, SMC, BFGS and the MultiStart×4 to the rosters where they are listed
  (ag's :307-310 already states only GridSearch.yaml exists; verify al's). Refresh provenance stamps the way
  autofit_assistant#55 did (`--write-provenance`, pins kept). Leave autolens_assistant's one untracked file alone.

Out of scope: any library source; the `api/modeling.rst` intersphinx consolidation (survey §5, a later phase);
HowToLens chapter_2 tutorials (Nautilus-only, correct today).

## Verification

Library docs legs green on GitHub (RTD red on the known autonerves floor is not a verdict); HowToLens/HowToGalaxy
notebook regeneration via PyAutoHands `generate.py`; autogalaxy_workspace smoke `guides/modeling/searches.py` under
`PYAUTO_TEST_MODE=1`; assistant provenance checks 0 errors; the Witness grep.

## Shape

One PR per repo (nine). Library (PyAutoLens, PyAutoGalaxy, PyAutoCTI) first with `pending-release`, docs-only, no
API change; workspace/HowTo/assistant PRs follow.
