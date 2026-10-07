# 03 — How non-linear searches are documented across PyAuto, and how that must scale

Read-only survey, 2026-10-07. All repos on `main`. Paths relative to `/home/jammy/Code/PyAutoLabs`.

## 0. Ground truth: the live search roster

`fit/PyAutoFit/autofit/__init__.py` (lines 97-110, 209-214) exports **15 concrete searches**:

| Family | Classes (module) | Install |
|---|---|---|
| Nested | `DynestyStatic`, `DynestyDynamic` (`nest/dynesty`), `Nautilus` (`nest/nautilus`), `NSS` (`nest/nss`, lazy attr) | dynesty base; nautilus-sampler in `[optional]`; NSS needs blackjax `[optional]` |
| MCMC | `Emcee` (`mcmc/emcee`), `Zeus` (`mcmc/zeus`), `BlackJAXNUTS` (`mcmc/blackjax/nuts`), `SMC` (`mcmc/blackjax/smc`, lazy attr) | emcee base; zeus/blackjax `[optional]` |
| MLE | `Drawer` (`mle/drawer`), `BFGS`, `LBFGS` (`mle/bfgs`), `MultiStartAdam`, `MultiStartADABelief`, `MultiStartLion`, `MultiStartProdigy` (`mle/multi_start_gradient`) | scipy base; optax base (marker-gated) |

Removed from the library (archived in `fit/autofit_workspace_developer/searches/`): **PySwarms** (Global/Local), **UltraNest**. MultiNest/PyMultiNest long gone.

Per-search YAML config was **deleted** in PyAutoFit `463612878` ("replace YAML config with explicit Python defaults in search classes", #1202). Every workspace's `config/non_linear/` now holds only `GridSearch.yaml` + README. Search defaults are `__init__` kwargs; there is **no per-search capability metadata** on the classes (no `requires_jax`, `uses_gradients`, `has_evidence` attribute). The only JAX-related hooks are ad-hoc kwargs (`Nautilus(use_jax_vmap=)`, `MultiStart*(gradient_mode=)`). Test-mode handling is per class (`apply_test_mode` in Emcee/Zeus, generic bypass in `abstract_search.py:839+`), via `autofit.non_linear.test_mode` / `autonerves.test_mode`.

## 1. Coverage matrix

Legend: **Y** present · **p** partial (name-dropped in prose / list only, no section or example) · **–** absent · **!** present but stale/wrong.

Columns:
- **API** = `fit/PyAutoFit/docs/api/searches.rst` autosummary
- **Prose** = PyAutoFit RTD prose (`docs/cookbooks/search.md` section; `p` = only in `overview/natural_language.md` / `scientific_workflow.md`)
- **afW** = `fit/autofit_workspace/scripts/searches/{nest,mcmc,mle}.py` section (+plot script)
- **afT** = `fit/autofit_workspace_test/scripts/searches/<Name>.py`
- **HTF** = `fit/HowToFit/scripts/` (ch1 tutorials 3/6/7, chapter_advanced)
- **alW** = `lens/autolens_workspace/scripts/guides/modeling/searches.py` (or wider usage)
- **agW** = `galaxy/autogalaxy_workspace/scripts/guides/modeling/searches.py`
- **acW** = `cti/autocti_workspace/scripts`
- **Asst** = `fit/autofit_assistant` (`skills/af_configure_search.md`, `wiki/core/concepts/*.md`); al/ag assistants noted
- **Brain** = SamplerSurface tier from `organs/PyAutoBrain/agents/faculties/samplers/samplers.sh`

| Search | API | Prose | afW | afT | HTF | alW | agW | acW | Asst | Brain tier |
|---|---|---|---|---|---|---|---|---|---|---|
| DynestyStatic | Y | Y | Y (+plot, get_dist) | Y | Y | Y | Y | – | Y | promoted `nest/dynesty`; minimal `dynesty_simple` |
| DynestyDynamic | Y | Y | Y | Y | – | Y | Y | – | Y | promoted (same dir) |
| **Nautilus** (default everywhere) | **–** | p (no cookbook section) | Y (+plot) | Y (+`_jax`) | Y (t6) | Y (151 scripts) | Y (38) | Y (26, only search used) | Y ("recommended default") | promoted; 5 minimal; 1 mature cell (autolens_inference) |
| NSS | – | – | **!** README claims it, section removed (`e731e6d`) | Y | – | – | – | – | – (Brain table only) | promoted `nest/nss` **and** archive `searches/nss` ("parked", stale) |
| Emcee | Y | Y | Y (+plot) | Y | Y | Y | Y | – | Y | promoted; minimal `emcee_simple` |
| Zeus | Y | Y | Y (+plot) | Y | – (HowToLens/Galaxy only) | Y | Y | – | Y | promoted |
| BlackJAXNUTS | Y | p | Y (mcmc.py) | Y | Y (t6, t7) | – | – | – | Y | promoted `mcmc/blackjax`; minimal `nuts_jax` |
| SMC | Y | – | – | – | – | – | – | – | – | **invisible** (folded into `mcmc/blackjax` dir; probe `blackjax_smc` in autolens dev) |
| Drawer | – | – | Y (mle.py) | – (gap flagged) | – | – (test only) | p (ellipse scripts) | – | Y | promoted; gap: no integration script |
| BFGS | Y | – | – | – | – | – (in PyAutoLens `api/modeling.rst`) | – | – | p (wiki) | promoted `mle/bfgs` (counted via LBFGS) |
| LBFGS | Y | Y | Y | Y | Y | Y | Y | – | Y | promoted; minimal `lbfgs_simple` |
| MultiStartAdam | – | p | Y (mle.py) | Y (+Resurrect, NaN, jax_assertions) | Y (t6, t7) | – | – | – | p (af README only; al/ag skills Y) | promoted; gap **false-positive** (dir≠class name) |
| MultiStartADABelief | – | – | p (prose in mle.py) | – | – | – | – | – | – | promoted (same dir) |
| MultiStartLion | – | – | p (prose in mle.py) | – | – | – | – | – | – | promoted (same dir) |
| MultiStartProdigy | – | p | – | Y | – | Y (19 scripts; guide section) | Y (11; guide section) | – | – (al/ag skills + ag wiki Y) | promoted; findings lane (pix_prodigy) |
| PySwarms (removed) | – | – | – | – | – | – | – | **!** config README | – | archive |
| UltraNest (removed) | – | – | – | – | – | – | – | – | – | archive |

Headline readings:
- **Nautilus — the default sampler in every science workspace — has no RTD API page and no cookbook section.** `docs/api/searches.rst` lists only DynestyDynamic/DynestyStatic under "Nested Samplers".
- Six live searches (NSS, Drawer, MultiStartAdam/ADABelief/Lion/Prodigy) have **no API page**; Nautilus makes it seven of 15.
- Only **5 of 15** searches (DynestyStatic/Dynamic, Emcee, Zeus, LBFGS) get a cookbook section — the 2022-era roster. Cookbook "It then provides example code for using every search" is false.
- **SMC** exists only as an API stub: no example, no test script, no assistant mention, invisible to the Brain gap rule.
- autocti only ever uses Nautilus; it has no search guide at all (fine) but its docs still advertise PySwarms.
- Library-level per-search unit test dirs are essentially empty (`test_autofit/non_linear/search/mcmc/__init__.py` only) — integration coverage lives in afT.

## 2. Surfaces in detail

### A. PyAutoFit RTD (`fit/PyAutoFit/docs/`)
- `api/searches.rst`: three autosummary blocks (Nested: DynestyDynamic, DynestyStatic; MCMC: Emcee, Zeus, BlackJAXNUTS, SMC; MLE: BFGS, LBFGS), Tools, GridSearch. Generated pages in `api/_autosummary/autofit.*.rst` (committed). No JAX/gradient column; the intro says only "three types".
- `api/samples.rst`: Samples, SamplesPDF, SamplesMCMC, SamplesNest, SamplesStored — no NSS/SMC-specific samples.
- `cookbooks/search.md` (383 lines): generic options + sections for Emcee, Zeus, DynestyDynamic, DynestyStatic, LBFGS. It is a **hand-maintained mirror** of `fit/autofit_workspace/scripts/cookbooks/search.py` (identical section list; no generator found in PyAutoHands). Points users to `notebooks/searches/mcmc.ipynb`, `notebooks/plot/emcee_plotter.ipynb`.
- `overview/natural_language.md` (l.117-123) is the only RTD prose with a family/JAX breakdown: "Nested: Dynesty and Nautilus; MCMC: Emcee and Zeus; Gradient-based (JAX): BlackJAXNUTS, MultiStartAdam/MultiStartProdigy". `scientific_workflow.md` uses Nautilus in prompts.
- `features/search_chaining.md`, `search_grid_search.md`, `interpolate.md`, `sensitivity_mapping.md`, `graphical.md`, `cookbooks/configs.md` all use `af.DynestyStatic` as the example search (contrasts with Nautilus default elsewhere).
- `general/citations.md`: only a Dynesty section. `files/citations.bib` has dynesty, emcee, nautilus, zeus1/2, but also **multinest/pymultinest** (removed) and **no** blackjax, optax, prodigy, NSS.
- `general/configs.md` still says configs "customize the default behaviour of the non-linear searches" — no longer true for per-search defaults.
- `installation/overview.md`: dependency list (dynesty, emcee, …) hand-written; `installation/source.md` references `optional_requirements.txt`, which **does not exist**.
- `docs/conf.py`: no `autodoc_mock_imports`; it imports `autofit` directly, so optional sampler deps must be installed in the RTD env (NSS/SMC are lazy attributes, which is what lets SMC's autosummary resolve without importing blackjax at import time).
- No page anywhere answers "which search should I use" with a capability table (evidence? gradients? JAX-native? GPU? warm start needed?).

### B. autofit_workspace (`fit/autofit_workspace/`)
- `scripts/searches/`: `nest.py` (DynestyStatic, DynestyDynamic, Nautilus), `mcmc.py` (Emcee, Zeus, BlackJAXNUTS), `mle.py` (Drawer, LBFGS, MultiStartAdam; ADABelief/Lion in prose), `start_point.py`. Notebooks mirror (`notebooks/searches/*.ipynb`, generated).
- `scripts/searches/README.md` describes NSS at length ("joins the nested-sampling lineup in nest.py", `pip install autofit[nss]`) — **both false**: the section was removed (`e731e6d`) and there is no `[nss]` extra in `pyproject.toml`.
- `scripts/plot/`: `dynesty_plotter.py`, `emcee_plotter.py`, `nautilus_plotter.py`, `zeus_plotter.py`, `get_dist.py` — one per search with search-specific plotting.
- `scripts/cookbooks/search.py` = source of the RTD cookbook (5 searches).
- `scripts/features/search_chaining.py`; `scripts/overview/overview_3_statistical_methods.py`.
- `config/non_linear/`: `GridSearch.yaml` + README ("Defaults for individual searches ship with PyAutoFit itself"). Correct.
- `smoke_tests.txt`: `searches/{mcmc,nest,mle}.py` are in the curated smoke list (so a new section in these files is smoke-tested by PyAutoHeart `heart/smoke.py`).
- `llms.txt` (hand-written): "Nested sampling (Dynesty, Nautilus, NSS) → nest.py" — stale NSS. `llms-full.txt` is **auto-generated by PyAutoHands** (`autohands/navigator.py`) — a working generation precedent.
- No search-comparison / "which search" page.

### C. autofit_workspace_test / autofit_workspace_developer
- `fit/autofit_workspace_test/scripts/searches/`: BlackJAXNUTS, DynestyDynamic, DynestyStatic, Dynesty_jax, Emcee, LBFGS, MultiStartAdam, MultiStartProdigy, MultiStartResumeNaNCounters, MultiStartResurrect, NSS, Nautilus, Nautilus_jax, Zeus. Missing: **SMC, Drawer, BFGS, MultiStartADABelief, MultiStartLion**. Also `scripts/jax_assertions/multi_start_gradient_auto_convergence.py`.
- `fit/autofit_workspace_test/smoke_tests.txt`: `searches/Emcee.py`, `DynestyStatic.py`, `Nautilus.py` + features/database/graphical. Run by `run_all_scripts.sh` (everything) and PyAutoHeart smoke (`organs/PyAutoHeart/heart/smoke.py`, `.github/workflows/smoke-tests.yml`). Policy (`sampler_pipeline` SKILL): "never grow smoke_tests.txt to exercise a sampler"; integration scripts are run on demand.
- `fit/autofit_workspace_developer/`: `searches_minimal/` (prototype tier: dynesty/emcee/lbfgs/nautilus*/nuts_jax + `_metrics.py` MLTracker + `output/comparison.txt`), `searches/` archive (pyswarms, ultranest, **nss** — whose README still says "removed from the library on 2026-07-11 … parked", although `1459734a4` re-mainlined it). Root README describes only UltraNest/PySwarms.
- New-search checklist today (from `organs/PyAutoBrain/skills/sampler_pipeline/reference.md` Stage 3-4): search.py, samples.py, `af.` export, extra, numpy-only unit test, config mirroring, integration script `<Name>.py` (+`_jax`). **No documentation step at all.**

### D. HowToFit (`fit/HowToFit/scripts/chapter_1_introduction/`)
- `tutorial_3_non_linear_search.py`: Search Types; MLE (LBFGS), MCMC (Emcee), Nested (DynestyStatic); "What is The Best Search To Use?" (generic prose, links to the cookbook).
- `tutorial_6_gradients.py`: MLE (LBFGS, MultiStartAdam), MCMC (Emcee, BlackJAXNUTS), Nested (Nautilus) — the only teaching material on gradients/JAX per family.
- `tutorial_7_the_details.py`: "Comparing Searches", "Hamiltonian Diagnostics" (DynestyStatic, Emcee, BlackJAXNUTS, MultiStartAdam).
- chapter_advanced: DynestyStatic/Emcee in graphical/EP tutorials.
- HowToFit is family-level, which is the right altitude: it should not need edits per new search unless a new *family/concept* appears.

### E. Other workspaces and libraries — the duplicated prose
- `lens/autolens_workspace/scripts/guides/modeling/searches.py` (435 l.) and `galaxy/autogalaxy_workspace/scripts/guides/modeling/searches.py` (392 l.): Nautilus, JAX, Live Points, MultiStartProdigy, Dynesty, Emcee, Zeus, LBFGS, Start Point, Search Cookbook. Near-duplicates (271 diff lines after namespace normalisation; agW has a **duplicated `__Start Point__` header**, l.280/336). Neither covers NSS, BlackJAXNUTS, SMC.
- `…/guides/plot/searches.py` in both (Dynesty, Emcee, Zeus, GetDist; 822 l. in alW).
- `lens/HowToLens/scripts/chapter_optional/tutorial_searches.py` and `galaxy/HowToGalaxy/scripts/chapter_optional/tutorial_searches.py`: Nested (Nautilus), Optimizers ("PyAutoFit supports the LBFGS optimizer" — ignores MultiStart*), MCMC (Emcee, Zeus). Plus `chapter_2_*/tutorial_1_non_linear_search.py`, `tutorial_9_search_chaining.py`.
- `cti/autocti_workspace`: Nautilus only; no search guide.
- `*_workspace_test` (lens/galaxy/cti): Nautilus only (plus one Drawer in alT latent smoke).
- Library RTD API pages re-listing autofit searches: `lens/PyAutoLens/docs/api/modeling.rst` (Nautilus, LBFGS, BFGS, DynestyDynamic, Emcee), `galaxy/PyAutoGalaxy/docs/api/modeling.rst` (same), `cti/PyAutoCTI/docs/api/modeling.rst` (Nautilus, DynestyDynamic, Emcee, **PySwarmsLocal, PySwarmsGlobal** under `currentmodule:: autofit` — dead autosummary targets).
- Library index/installation/citation prose: `lens/PyAutoLens/docs/index.md:123` and `galaxy/PyAutoGalaxy/docs/index.md:147` cite PySwarms as an example search; `galaxy/PyAutoGalaxy/docs/installation/overview.md:35`, `cti/PyAutoCTI/docs/installation/overview.rst:48` list PySwarms as a dependency; `docs/general/citations.*` in PyAutoGalaxy/PyAutoCTI say "(e.g. Dynesty, Emcee, PySwarms, etc)" (PyAutoLens's was updated to "Nautilus, Dynesty, Emcee, Zeus").
- `CITATIONS.md` per repo (10 files) list different subsets: HowToFit {dynesty, nautilus, emcee}; PyAutoLens {dynesty, nautilus, emcee, zeus}; autolens/autogalaxy_workspace, HowToLens {dynesty, emcee}; PyAutoGalaxy, HowToGalaxy, PyAutoCTI {dynesty, emcee, pyswarms}; PyAutoFit/autofit_workspace none.
- Configs: every workspace (`config/non_linear/` in afW, afT, alW, agW, acW, alT, agT, acT, HowToLens, HowToGalaxy) contains only `GridSearch.yaml` + README → **no per-search config propagation exists any more**; nothing to sync. Stale READMEs: `fit/PyAutoFit/autofit/config/non_linear/README.md` (says **PyAutoLens**, lists `mcmc.yaml`/`nest.yaml`/`mle.yaml` that don't exist), `cti/autocti_workspace/config/non_linear/README.rst` (same three files, "e.g. PySwarms"). `fit/autofit_assistant/skills/af_configure_search.md` and `wiki/core/concepts/non_linear_search.md:57` plus `galaxy/autogalaxy_assistant/skills/ag_configure_search.md` tell users "per-sampler defaults live in `config/non_linear/*.yaml`" — false since #1202.
- PyAutoNerves role: `autonerves.conf` layered config + `autonerves.test_mode` (test-mode levels, `skip_latents`). It no longer carries any per-search defaults; it is the right place for *test-mode/CI reductions* per search, not for user defaults.

### F. Assistants and the Brain samplers faculty
- `fit/autofit_assistant/skills/af_configure_search.md`: roster "Nautilus, DynestyStatic, DynestyDynamic; Emcee, Zeus, BlackJAXNUTS; LBFGS, Drawer" — omits NSS, SMC, BFGS, all MultiStart*. Says "until the core wiki lands" (it has landed) and "HowToFit chapter 2" (HowToFit has `chapter_1_introduction` + `chapter_advanced`). Recommendation logic: evidence → nested (Nautilus default); posterior-only → Emcee/Zeus, NUTS if differentiable; point → LBFGS; "propose a benchmark on their real likelihood rather than folklore".
- `wiki/core/concepts/non_linear_search.md` holds a hand-written **roster table** (Family | Search | One-line character) — 8 searches; family pages `nested_sampling.md`, `mcmc_and_hmc.md`, `mle_and_optimizers.md`, `initialization_and_chaining.md`; `wiki/core/stack/autofit.md`.
- `fit/autofit_assistant/benchmarks/` are **LLM-assistant task benchmarks** (prompts: hard_sne_cosmology, medium_wrap_likelihood, teacher_workflow; `RESULTS.md` "No runs recorded yet") — the assistant has **no sampler benchmark evidence** of its own.
- `lens/autolens_assistant/skills/al_configure_search.md`, `galaxy/autogalaxy_assistant/skills/ag_configure_search.md` + `wiki/core/concepts/non_linear_search.md` carry their own rosters (incl. MultiStartAdam/Prodigy). Three assistant rosters, maintained independently.
- Brain: `organs/PyAutoBrain/agents/faculties/samplers/AGENTS.md` + `_samplers.py`/`samplers.sh` (SamplerSurface). Tiers: minimal (`autofit_workspace_developer/searches_minimal`), archive (`…/searches`), integration (`autofit_workspace_test/scripts/searches`), promoted (PyAutoFit module dirs), experiment probes + findings (`autolens_workspace_developer/searches_minimal`, 36 probes, 9 `*_findings.md`), mature (`autolens_inference` cells — 1 today: `nautilus/point_source/simple_source_plane`). Benchmark record: `fit/autofit_workspace_developer/searches_minimal/output/comparison.txt` (1D Gaussian; nss_simple/nss_jit/nss_grad/nautilus_simple/nautilus_jax) + per-sampler summaries; deeper record in private `PyAutoMemory/wiki/methods/concepts/sampler-benchmarks.md`. Judgment tables (sampler↔likelihood, gradients/JAX, initialization providers vs consumers, promotion criteria, maturation lane) are the richest "which search" guidance in the ecosystem — but internal only.
- `skills/sampler_pipeline/{SKILL,reference}.md`: ingest → prototype → profile → promote. Stale: cites "`[nss]` extra is the worked example" (no such extra), "workspace configs override library defaults … mirror config keys" (no per-search config), and its Boundary section names `autolens_profiling` as the mature tier where the faculty now says `autolens_inference`.

### G. llms.txt / AGENTS.md
- Hand-written: `fit/autofit_workspace/llms.txt` (stale NSS), `fit/PyAutoFit/AGENTS.md:66` ("nautilus; MLE: LBFGS/BFGS/drawer"), `fit/autofit_workspace/AGENTS.md` (LBFGS), `lens/HowToLens/llms.txt` (Nautilus).
- Generated (PyAutoHands navigator): all `llms-full.txt` — they follow the scripts automatically.

## 3. The blast radius of adding ONE new search today

To bring a new search to parity with the best-documented ones (Emcee/LBFGS), in order (library first). Code files are listed for completeness but not counted as docs.

Code (not counted): `autofit/non_linear/search/<group>/<name>/{search,samples}.py`, `autofit/__init__.py`, `pyproject.toml` extra, unit test.

**PyAutoFit (library docs)**
1. `fit/PyAutoFit/docs/api/searches.rst` (autosummary entry)
2. `fit/PyAutoFit/docs/api/_autosummary/autofit.<Name>.rst` (committed generated stub)
3. `fit/PyAutoFit/docs/cookbooks/search.md` (contents list + section)
4. `fit/PyAutoFit/docs/overview/natural_language.md` (family/JAX list)
5. `fit/PyAutoFit/docs/installation/overview.md` (dependency list, if new dep)
6. `fit/PyAutoFit/docs/general/citations.md`
7. `fit/PyAutoFit/files/citations.bib` (+ `files/citations.md`, `files/citation.tex`)
8. `fit/PyAutoFit/AGENTS.md` (package map line)

**autofit_workspace**
9. `scripts/searches/<family>.py` (section; smoke-tested)
10. `scripts/searches/README.md`
11. `scripts/cookbooks/search.py` (mirror of #3)
12. `scripts/plot/<name>_plotter.py` (if search-specific plots)
13. `llms.txt`
14. `CITATIONS.md`
(notebooks, `llms-full.txt`, `workspace_index.json` regenerate via PyAutoHands — not hand-edited)

**autofit_workspace_test / developer**
15. `fit/autofit_workspace_test/scripts/searches/<Name>.py` (+ `<Name>_jax.py`)
16. `fit/autofit_workspace_developer/searches_minimal/<name>_simple.py` + `output/comparison.txt` row (pre-promotion evidence)

**HowToFit** (only if a new family/capability)
17. `scripts/chapter_1_introduction/tutorial_3_non_linear_search.py` and/or `tutorial_6_gradients.py`
18. `CITATIONS.md`

**autolens / autogalaxy / autocti (lockstep duplicates)**
19. `lens/autolens_workspace/scripts/guides/modeling/searches.py`
20. `galaxy/autogalaxy_workspace/scripts/guides/modeling/searches.py`
21. `lens/autolens_workspace/scripts/guides/plot/searches.py` (if plots)
22. `galaxy/autogalaxy_workspace/scripts/guides/plot/searches.py` (if plots)
23. `lens/HowToLens/scripts/chapter_optional/tutorial_searches.py`
24. `galaxy/HowToGalaxy/scripts/chapter_optional/tutorial_searches.py`
25. `lens/PyAutoLens/docs/api/modeling.rst`
26. `galaxy/PyAutoGalaxy/docs/api/modeling.rst`
27. `cti/PyAutoCTI/docs/api/modeling.rst`
28-30. `docs/general/citations.*` in PyAutoLens, PyAutoGalaxy, PyAutoCTI
31-37. `CITATIONS.*` in PyAutoLens, PyAutoGalaxy, PyAutoCTI, autolens_workspace, autogalaxy_workspace, HowToLens, HowToGalaxy
38-39. `docs/installation/overview.*` in PyAutoGalaxy, PyAutoCTI (dependency lists)

**Assistants**
40. `fit/autofit_assistant/skills/af_configure_search.md` (roster + branch)
41. `fit/autofit_assistant/wiki/core/concepts/non_linear_search.md` (roster table)
42. `fit/autofit_assistant/wiki/core/concepts/<family>.md`
43. `fit/autofit_assistant/wiki/core/concepts/initialization_and_chaining.md` (provider/consumer role)
44. `fit/autofit_assistant/wiki/core/stack/autofit.md`
45. `lens/autolens_assistant/skills/al_configure_search.md`
46. `galaxy/autogalaxy_assistant/skills/ag_configure_search.md`
47. `galaxy/autogalaxy_assistant/wiki/core/concepts/non_linear_search.md`
48. `lens/autolens_assistant/wiki/core/concepts/non_linear_search.md`

**Organs / galleries**
49. `organs/PyAutoBrain/agents/faculties/samplers/AGENTS.md` (judgment table)
50. `PyAutoMemory/wiki/methods/concepts/sampler-benchmarks.md` (private record)
51. `fit/autofit_visualization/scripts/samples/visualization.py` (+ regenerated manifest) if the search has its own plots

**Count: ~51 hand-edited documentation files across ~20 repos** (≈35 minimum for a search with no plots, no new family, no new dependency). Of these, ~16 are pure *roster lists* (API rst ×4, rosters in assistants ×6, citations/CITATIONS ×12 overlap, llms.txt, AGENTS.md) — exactly the content a registry could generate. None of this is in the `sampler_pipeline` promotion checklist, which is why every search added since 2025 (Nautilus, NSS, SMC, BlackJAXNUTS, MultiStart*) is partially documented.

## 4. Inconsistencies found

1. **Nautilus missing from `fit/PyAutoFit/docs/api/searches.rst`** and from `docs/cookbooks/search.md` / `autofit_workspace/scripts/cookbooks/search.py`, despite being the recommended default in every assistant and 200+ workspace scripts.
2. RTD api missing NSS, Drawer, MultiStartAdam/ADABelief/Lion/Prodigy; cookbook claims to cover "every search" but covers 5/15.
3. `fit/autofit_workspace/scripts/searches/README.md` advertises NSS in `nest.py` + `pip install autofit[nss]`; the section was removed (`e731e6d`) and no `[nss]` extra exists. Same stale NSS in `fit/autofit_workspace/llms.txt:28`.
4. `fit/autofit_workspace_developer/searches/nss/README.md` says NSS is "parked … removed 2026-07-11" — it was re-mainlined (`1459734a4`); the archive copy now duplicates library code and the SamplerSurface lists NSS as both archive and promoted.
5. Per-search config claims after #1202: `fit/PyAutoFit/autofit/config/non_linear/README.md` (also says "PyAutoLens"), `cti/autocti_workspace/config/non_linear/README.rst`, `fit/autofit_assistant/skills/af_configure_search.md` ("Per-sampler defaults live in config/non_linear/"), `fit/autofit_assistant/wiki/core/concepts/non_linear_search.md:57`, `galaxy/autogalaxy_assistant/skills/ag_configure_search.md`, `fit/PyAutoFit/docs/general/configs.md`, `organs/PyAutoBrain/skills/sampler_pipeline/reference.md` Stage 3 point 6.
6. PySwarms (removed) still documented: `cti/PyAutoCTI/docs/api/modeling.rst:53-54` (dead autosummary targets), `lens/PyAutoLens/docs/index.md:123`, `galaxy/PyAutoGalaxy/docs/index.md:147`, `galaxy/PyAutoGalaxy/docs/installation/overview.md:35`, `cti/PyAutoCTI/docs/installation/overview.rst:48`, citations in PyAutoGalaxy/PyAutoCTI docs + `CITATIONS.*` of PyAutoGalaxy, HowToGalaxy, PyAutoCTI, autocti config README.
7. `fit/PyAutoFit/files/citations.bib` carries multinest/pymultinest (removed) and lacks blackjax/optax/prodigy (PyAutoLens/PyAutoGalaxy citations.md already cite optax/prodigy — the library bib disagrees with its consumers).
8. `fit/PyAutoFit/docs/installation/source.md:37` references a non-existent `optional_requirements.txt`.
9. `fit/autofit_assistant/skills/af_configure_search.md`: "until the core wiki lands" (landed), "HowToFit chapter 2" (no such chapter).
10. SamplerSurface gap rule keys on module-directory names: false positive "multi_start_gradient has no integration script" (MultiStartAdam.py exists) and false negatives for SMC (dir `blackjax` matched by BlackJAXNUTS) and BFGS (dir `bfgs` vs LBFGS.py). Archive tier double-counts NSS. `comparison.txt` is a 1D-Gaussian table dominated by NSS variants.
11. `organs/PyAutoBrain/skills/sampler_pipeline/SKILL.md` Boundary names `autolens_profiling` as the mature tier; the faculty AGENTS.md says `autolens_inference` (profiling retired that role, autolens_profiling#245).
12. `galaxy/autogalaxy_workspace/scripts/guides/modeling/searches.py` has two `__Start Point__` sections; HowToLens/HowToGalaxy `tutorial_searches.py` say "PyAutoFit supports the LBFGS optimizer" with no mention of MultiStart* optimisers the same workspaces now default to for pixelizations.
13. JAX claims: no single authoritative statement of which searches are JAX-native, gradient-consuming, GPU-batched or evidence-producing. Claims are scattered (natural_language.md, nest README's "order of magnitude" NSS claim, Brain table "~50× per-eval", HowToFit t6) and only the Brain's is benchmark-backed — and it is internal/private.
14. RTD feature pages use `af.DynestyStatic` as the generic example while workspaces/assistants recommend Nautilus — not wrong, but signals drift.

## 5. Proposed scalable documentation architecture

### Principle
Per-search **facts** (name, family, import path, install extra, capability flags, citation keys, example anchors, test script, status) must have exactly one home — the library — and every roster/table/list elsewhere is **generated** from it. Per-search **judgement** (when to pick it, measured performance) lives in exactly one public place (a search gallery/benchmark repo) and one internal place (the Brain faculty). Narrative teaching stays family-level and therefore search-count-independent.

### The registry (single source of truth) — in PyAutoFit
`autofit/non_linear/search/registry.py` (or class attributes + a collector), one record per search:

```python
SearchInfo(
  name="Nautilus", family="nest", module="autofit.non_linear.search.nest.nautilus.search",
  status="stable" | "experimental" | "archived",
  extra="optional", upstream="https://github.com/johannesulf/nautilus",
  evidence=True, posterior=True, point_estimate=False,
  gradients="none" | "optional" | "required", jax="callback" | "vmap" | "native",
  gpu="no" | "batched", warm_start="provider" | "consumer" | "neutral",
  resumable=True, search_plots=["corner_anesthetic", ...],
  citations=["nautilus"], example="autofit_workspace:scripts/searches/nest.py#Search: Nautilus",
  integration_test="autofit_workspace_test:scripts/searches/Nautilus.py",
)
```
Capability flags as class attributes (`AbstractNest.produces_evidence = True`, `BlackJAXNUTS.requires_gradients = True`) let the runtime enforce them too (e.g. warn when a gradient search gets a non-JAX analysis) — documentation and behaviour cannot drift apart. A unit test asserts every `NonLinearSearch` subclass exported from `af` has a record, and every record's `example`/`integration_test` path exists (the latter in workspace CI).

Generated artefacts:
- `docs/api/searches.rst` autosummary blocks per family + a **capability matrix** page (`docs/searches/index.md`: family, evidence, gradients, JAX/GPU, warm-start role, install, example link). Replaces the hand list and becomes the RTD "which search" page.
- `files/citations.bib` subset check + a generated "cite the searches you used" table consumed by every `citations.md`/`CITATIONS.md` (link to one canonical page instead of 13 hand lists).
- `autofit search list --json` (or `python -m autofit.search_registry`) → read by PyAutoHands navigator to regenerate `llms.txt` search lines, by the three assistants' `/af_refresh_api_docs`-style skills to regenerate their roster tables (`<!-- generated: search-roster -->` fenced blocks), and by the Brain SamplerSurface to key tiers **by class, not module dir** (fixes the false positive/negatives in §4.10).
- PyAutoLens/PyAutoGalaxy/PyAutoCTI `api/modeling.rst`: replace their hand lists with a single link/intersphinx reference to PyAutoFit's searches page (or include a generated snippet). Removes 3 lockstep files and the PySwarms ghost.

### Search gallery (mirror of the `<lib>_visualization` pattern)
A per-search "card" generated by running each search on the standard problem(s), like `autofit_visualization`'s producers + `gallery/viz_manifest.yaml`:
- producer per search (the existing afT integration script, reduced settings) → manifest row: wall time, evals, ESS, log Z, max log L, parameter recovery, plots (corner, trace), library version.
- The `_metrics.MLTracker` contract in `searches_minimal/` already defines the columns; promote it to the gallery's schema.
- Rendered as a Pages board (PyAutoPulse/PyAutoEyes style) and linked from the RTD matrix page, so "which search" claims are backed by a dated public table instead of folklore or private PyAutoMemory.
- Home: a new **`fit/autofit_inference`** repo (the autofit-level sibling of `lens/autolens_inference`): standard problems (1D Gaussian, multimodal, high-D correlated, funnel), every registered search, CPU and GPU legs, re-run on release. `autolens_inference` stays the real-likelihood mature tier; `autofit_inference` is the generic, cheap, every-search baseline. The Brain SamplerSurface reads its manifest as the benchmark record (replacing the ad-hoc `comparison.txt`).

### PyAutoNerves
Per-search defaults are Python kwargs now — do **not** reintroduce per-search YAML. Nerves' role: (a) `test_mode` reductions per search declared in the registry (`test_mode_kwargs`) so smoke/test-mode behaviour is uniform rather than a hand-written `apply_test_mode` per class; (b) optional project-level overrides through the layered config keyed by registry name, if ever needed, documented once in Nerves. All stale "config/non_linear/*.yaml" claims (§4.5) get deleted.

### What lives where
| Layer | Content | Scales with #searches? |
|---|---|---|
| PyAutoFit registry + RTD | facts, capability matrix, API pages, citations — generated | yes, automatically |
| PyAutoFit RTD prose | family concepts (nested/MCMC/HMC/MLE/multi-start), generic search options; cookbook trimmed to common options + link to matrix | no |
| autofit_workspace `scripts/searches/` | one runnable section per *stable* search (family files; consider one file per search as the roster grows, e.g. `searches/nest/nautilus.py`) — smoke-tested | yes, 1 section per search |
| autofit_workspace_test | one integration script per search, required by registry test | yes, 1 file |
| HowToFit | family-level teaching (t3 types, t6 gradients, t7 diagnostics/comparison) — only touched when a new family/capability appears | no |
| autolens/autogalaxy guides, HowToLens/Galaxy `tutorial_searches.py` | domain advice only (which settings matter for lens models), pointing at the matrix for the roster; never re-list every search | no |
| assistants (af/al/ag) | generated roster block + hand-written decision guide that cites gallery numbers | roster yes (generated) |
| Brain samplers faculty | internal judgement + promotion criteria; reads registry + gallery manifest; private PyAutoMemory stays private | no (data-driven) |
| autofit_inference (new) | public per-search benchmark gallery | yes, automatically |

### Phases
**Phase 1 — repair (docs-only, no new machinery).** Fix §4: add Nautilus/NSS/Drawer/MultiStart* to `api/searches.rst`; Nautilus section in cookbook (+workspace mirror); delete stale NSS README/llms claims; purge PySwarms/MultiNest across library docs/CITATIONS/bib; delete per-search-YAML claims (PyAutoFit config README, autocti config README, 3 assistant files, configs.md, sampler_pipeline); fix af_configure_search staleness; mark `autofit_workspace_developer/searches/nss` superseded; add integration scripts for SMC/Drawer/BFGS. Add a **"Stage 5 — documentation"** to `sampler_pipeline/reference.md` listing the §3 blast radius as the interim checklist.

**Phase 2 — registry.** `SearchInfo` records + capability class attributes in PyAutoFit; completeness unit test; generated `docs/api/searches.rst` + `docs/searches/index.md` capability matrix; `autofit search list --json`; downstream libraries' `api/modeling.rst` collapse to a link. One CITATIONS canonical page.

**Phase 3 — consumers generate.** PyAutoHands navigator regenerates `llms.txt` roster lines; assistants regenerate roster blocks (af/al/ag); SamplerSurface keys tiers by registry class; Nerves `test_mode` reductions from the registry; workspace CI checks registry `example`/`integration_test` paths exist. Collapse alW/agW `guides/modeling/searches.py` duplicates onto a shared domain-advice template plus a link to the matrix.

**Phase 4 — search gallery (`autofit_inference`).** New repo with producers per search on standard problems, manifest + Pages board (PyAutoPulse/Eyes pattern), release re-render; Brain faculty and assistants cite it as the benchmark of record; RTD matrix links each row to its gallery card. After this, adding a search = code + registry record + integration script + one workspace section; everything else regenerates (blast radius ~51 → ~5 hand-edited files).
