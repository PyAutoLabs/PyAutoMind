## autofit-assistant-birth
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/1 (closed)
- completed: 2026-07-10
- prs: autofit_assistant#2 (phases 1-3) + #3 (phase 4) — both MERGED same day; birth commit 3667f84 direct to main (empty-repo)
- summary: autofit_assistant born PUBLIC and fully built in one --auto supervised session (launch gates: public at birth, hand-authored, demos = gaussian + SNe cosmology). 14 skills (af_wrap_likelihood + af_adapt_to_domain are the differentiators), 16-page provenance-stamped stats wiki, autoassistant tooling port (52/52 tests), benchmarks (3 cards, parity-enforced), hpc/, llms.txt, wiki-currency CI — whose first PR run CORRECTLY caught the baseline pinning local source (2026.7.6.649) vs live release (2026.7.9.1); honest re-pin 62c34d2 in a clean venv (ambient PYTHONPATH had aliased local source). Demos validated with real fits: gaussian recovers truth; Pantheon+ flat-LCDM gives Om=0.344 H0=73.1 (Brout22-consistent, diagonal-errors caveat documented). Newborn checklist legs 1-3 green; leg 4 = autofit_assistant#4 checklist (human). Follow-ups filed: feature/pyautobuild/autofit_assistant_wiki_currency_wiring.md, feature/autofit_assistant/deferred_skill_tranche.md. Research anchor retired.

## Original prompt

# autofit_assistant — birth the generic inference assistant

Type: feature
Target: autofit_assistant
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

autolens_assistant is proving to be very good, and is now excelling at various science cases.

It is time to make autofit_assistant, noting that this has the following differences:

- Autolens is tied to a specific scientific domain (lensing), whereas autofit_assistant is a tool to help someone perform inference in their own specific scientific domain. That means, when someone begins using autofit_assistant, one of their first tasks is probably going to be also training or adapting it to their scientific domain. This probably includes paper ingestion, manually providing code with a likelihood function (ideally) and the model composition.

- AutoFit assistant would benefit from a wiki on all the core statistics concepts it uses during inference albeit many are probably there from the general foundation model. Nevertheless, the EP wiki we made would be valuable here, probably some stuff specific to each source code sampler, maybe stuff on priors, have a think.

- like the autolens_assistant pairs to the autolens_workspace via skills, we want to do the exact same with the autofit assistant.

- All the core features of the autolens_assistant (making a science project, open data repository design, benchmarks, assistant and teacher mode, HPC link, etc) should be kept and designed suitable for autofit.

## Design

### What it is

`autofit_assistant` is the PyAutoFit AI Assistant: a generic, public agent workspace
following the autolens_assistant pattern (AGENTS.md canonical + skills + wiki +
science-project machinery), paired to **PyAutoFit + autofit_workspace**.

The defining inversion versus autolens_assistant: the lensing assistant ships with its
scientific domain built in; the autofit assistant's user **brings their own domain**.
Domain adaptation is therefore a first-class onboarding product, not an afterthought —
the assistant's first job with a new user is to *become* their domain assistant.

### Relationship to existing machinery

- **Clone v1** (Brain#78 / Build#135 / Heart#56) already proved a lightweight seed can
  regenerate the skeleton in one command (134 files, clean `al_→af_` substitution,
  341-entry PENDING queue). Per the 2026-07-10 decision the maintainer authors the real
  assistant from this prompt rather than accepting a clone birth — but the clone plan
  JSON and its derived prefix mapping are the authoritative checklist of what is
  mechanical vs. what needs genuine re-authoring. Decide at plan time whether Phase 0
  uses the seed as scaffold or hand-authors against its file list.
- **Repo creation is an interactive gate**: a dedicated question naming the repo
  (`PyAutoLabs/autofit_assistant`) and visibility must precede `gh repo create`.
  Private-first, public flip only after the Heart `newborn_validation.md` checklist.
- **Absorbs** `research/autofit_assistant/autofit_assistant_planning.md` (the planning
  anchor holding the PyAutoMemory migration notes). Its sequencing blocker — the EP
  framework-review write-ups — landed 2026-07-10, so this prompt is unblocked. Retire
  the research anchor when this ships.

### Pillar A — domain adaptation as the first-run experience (the differentiator)

- A domain-onboarding flow (extend `start-new-project` or a dedicated
  `af_adapt_to_domain` skill) that interviews the user and drives three adaptation
  channels:
  1. **Paper ingestion** — adapt `al_ingest_paper`: papers from the user's field grow a
     `wiki/literature/` sub-wiki in their clone (autolens ships this full; autofit ships
     it near-empty by design, with the schema/AGENTS.md so it grows well).
  2. **Likelihood wrapping (the ideal path)** — `af_wrap_likelihood`: user supplies
     existing code with a likelihood function; the skill produces an `Analysis` class
     around it, with the standard traps documented (data/noise conventions, `log_likelihood_function`
     contract, JAX-compatibility triage).
  3. **Model composition** — `af_compose_model`: turn the user's parametrisation into
     `af.Model`/`af.Collection` with priors, linking to the priors wiki pages.
- Adaptation output lands in `wiki/project/` (profile.md + domain journal), mirroring
  how the lens assistant calibrates depth per user.

### Pillar B — core statistics/inference wiki

`wiki/core/concepts/` for the statistics the assistant leans on during inference.
Foundation-model knowledge covers the generic textbook layer; these pages earn their
place by being **PyAutoFit-specific** (what the implementation actually does, its knobs,
its pitfalls):

- Model composition & priors (prior types, prior design pitfalls, `sigma=0` point-mass
  idiom, latent variables).
- Non-linear search overview + **one page per shipped sampler family** (dynesty,
  nautilus, ultranest, emcee, zeus, PySwarms, optimizers, …) — match the installed
  PyAutoFit roster at write time, not memory.
- Nested sampling, MCMC/HMC, initialization & search chaining, sampler benchmarks.
- **Graphical models & EP** — migrate the EP write-up per the migration notes.
- Evidence, model comparison, samples/posteriors, aggregator/result analysis.

Seeding: generalised public rewrites of `PyAutoMemory/methods_wiki/` pages
(expectation-propagation, nested-sampling, sampler-benchmarks, hamiltonian-monte-carlo,
gpu-nested-sampling, initialization-chaining, bayesian-inference, samplers source
notes). PyAutoMemory is personal — never referenced from the public repo; originals
stay there as the private superset. `wiki/core/stack/` shrinks to autoconf + autofit.

### Pillar C — workspace pairing via skills

Exactly the autolens_assistant↔autolens_workspace mechanism, retargeted at
**autofit_workspace** (`scripts/{overview,cookbooks,features,searches,model,plot,simulators}`):

- Port the `autoassistant/` package (audit_skill_apis + API gate hook, refresh_api_docs,
  to_notebook, literature `--check-citations` incl. the fifth wiki-currency leg,
  benchmark runner) with `af_` naming and `sources.yaml` pointing at
  PyAutoFit/autoconf/autofit_workspace clones @ main.
- Candidate `af_*` skill set (grounded against workspace scripts at build time):
  setup_environment, compose_model, configure_search, run_search, chain_searches,
  load_results (aggregator), custom_analysis / wrap_likelihood, simulate_dataset,
  plot_fit, debug_fit_failure, graphical_ep, hierarchical_inference,
  sensitivity_mapping, ingest_paper, adapt_to_domain, to_notebook, update_wiki,
  audit_skill_apis, refresh_api_docs; plus project-workflow skills
  (start-new-project, contribute-upstream) and the `_style.md`/`_bootstrap_skill.md`
  meta-skills.

### Pillar D — ported core features, generalised for inference

- **Modes**: assistant / teacher / maintainer. Teacher mode anchors to **HowToFit**
  chapters (as the lens teacher anchors to HowToLens).
- **Benchmarks**: `benchmarks/` prompts+runs+RESULTS with the test-enforced card↔README
  parity; inference-flavoured cards (compose a model, wrap a supplied likelihood, run
  and interpret a search, EP on a graph, debug a broken fit).
- **Science project / open-data repository design**: keep the shareable-project
  template, redesigned for user-supplied data — dataset conventions must be
  domain-neutral (the user's data format is part of onboarding, not assumed).
- **HPC link**: `hpc/` batch templates + sync, CPU-first with the GPU path where the
  user's likelihood supports JAX.
- **Worked demo projects** (analogue of cosmos_web_ring / slacs0946): open decision —
  the canonical 1D Gaussian plus at least one *real* non-lensing case that exercises
  likelihood-wrapping end-to-end. Choose at plan time.
- Infrastructure parity: llms.txt, config/, Makefile, activate.sh, live-visual flag
  where applicable, smoke CI via the proven reusable family workflow, firewall/policy
  + url_fixups riders, safety invariants adapted (the real-data-inspection gate
  generalises to "plot/inspect the user's dataset before first fit").

### Phasing (split at start_dev; each phase its own issue/PR cycle)

- **Phase 0 — birth + skeleton**: interactive repo gate; AGENTS/CLAUDE/modes/config/
  Makefile/CI; safety invariants; empty wiki scaffolding. (Clone seed as scaffold vs
  hand-author: decide here.)
- **Phase 1 — workspace pairing**: `autoassistant` tooling ported + the first tranche
  of `af_*` skills grounded in autofit_workspace, API audit green.
- **Phase 2 — core wiki**: statistics concepts + per-sampler pages + EP/graphical
  migration from methods_wiki (public rewrites).
- **Phase 3 — domain adaptation**: adapt_to_domain / ingest_paper / wrap_likelihood /
  compose_model flow + start-new-project + worked demo project(s).
- **Phase 4 — parity & publish**: benchmarks, teacher mode, HPC link, llms.txt,
  citation/currency CI, Heart newborn checklist → public flip.

### Open design decisions (resolve during planning, with the user)

1. Worked demo project choice (what plays the role of cosmos_web_ring).
2. Sampler roster for dedicated wiki pages (audit installed PyAutoFit).
3. Clone-seed scaffold vs. full hand-authoring for Phase 0.
4. Whether the shareable science-project template lives in-repo or as a separate
   PyAutoScientist-family template repo.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10; header + design hand-fixed in session (target autofit_assistant, not PyAutoFit) -->
