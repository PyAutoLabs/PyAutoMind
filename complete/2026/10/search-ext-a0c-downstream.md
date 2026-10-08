## search-ext-a0c-downstream
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/776
- completed: 2026-10-08
- epic: search-extensibility (phase A0c part 2)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/777
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/652
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/115
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/777
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/652
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/97
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/86
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/257
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/37
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/157
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/34
- merge-commit: PyAutoLens 7a97f601; PyAutoGalaxy c32b3304; PyAutoCTI 4c96d1b1; HowToLens df89f98b; HowToGalaxy 6d99dbff; autogalaxy_workspace 3afb5a6b; autocti_workspace f82dea34; autolens_assistant f46e296f; autogalaxy_assistant e317f381

### Outcome
The downstream sweep of removed-search ghosts and stale search claims across the lens, galaxy and CTI families. PySwarms/MultiNest are gone from the three libraries' docs and CITATIONS (Nautilus, Dynesty, Emcee, Zeus named instead; autocti's dead autosummary targets replaced by LBFGS); HowToLens and HowToGalaxy's optional searches tutorial describes LBFGS/BFGS and the MultiStart gradient optimisers instead of "LBFGS only"; autogalaxy_workspace's duplicated `__Start Point__` header is merged; autocti_workspace's config README lists only `GridSearch.yaml`; the al/ag assistants' search skill and concept page drop the per-search YAML claim and carry the full roster (NSS, BlackJAXNUTS, SMC, BFGS, MultiStart×4). First `--auto` run of the epic: Opus implementation + ship workers, Fable review and merge; tier glance auto-merged in-turn.

### Validation and limits
Library suites 832 / 1357 / 271 passed on docs-only diffs; ag searches guide smoke exit 0; notebooks regenerated; assistants provenance 0 errors. Review found one false claim before PR-open ("every start_here.py uses MultiStartProdigy"; 8/21 lens, 5/9 galaxy) and it was reworded. The HowTo PRs first failed the navigator catalogue-staleness leg because only the notebook had been regenerated; `regenerate_navigator.py` fixed `workspace_index.json` and the re-run was green. Heart STALE at launch and ship. Left outside the Witness for a follow-up: JOSS `paper/` files and PyAutoGalaxy/PyAutoCTI `files/citations.*` still mention PySwarms; autolens_assistant `wiki/core/api/searches.md`, `wiki/core/stack/autofit.md` and `config/visualize/plots_search.yaml` keep PySwarms text.

## Original prompt

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
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/776
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
