# Search extensibility epic: research report and phased plan

Written 2026-10-07 by the architect session; no code edited. Companion to the prompt in `search_extensibility_epic.md`. Four read-only Opus surveys fed this report. Their full text is in `search_extensibility_epic_surveys/` and is cited as `surveys/01 §n` … `surveys/04 §n`:

- `01_search_architecture.md`: the `autofit/non_linear/` package, contracts, duplication, persistence, a target design.
- `02_jax_interface.md`: every route by which JAX reaches a search, a per-search matrix, failure modes measured with probes, a unified contract.
- `03_search_docs.md`: a coverage matrix over ~20 repos, the blast radius of one new search, a registry-driven documentation design.
- `04_inference_profiling_infra.md`: autolens_inference/autolens_profiling anatomy, Pulse/Insight registration, the first benchmark, the birth path.

Paths are relative to `fit/PyAutoFit/autofit/non_linear/` unless prefixed; line numbers are the surveys' (PyAutoFit `main` @ e807cc531, 2026-10-07).

## 0. Summary

- **Two corrections to the brief.**
  - (a) `autofit_inference` reports to **PyAutoInsight** (`organs/PyAutoInsight`, contract `inference-summary@1`), not to PyAutoPulse. Insight's first producer is autolens_inference, and its second-producer fixture (`tests/fixtures/galaxy_summary_v1.json`) already passes with no reader changes. PyAutoPulse is the home of `autofit_profiling` (`profiling-summary@2`). See `surveys/04 §0.1`.
  - (b) `autofit_profiling` is already a filed Pulse task: `organs/PyAutoPulse/tasks/autofit_profiling_bootstrap.md`, campaign `autofit`, status `needs-decision`, waiting on the human's repo-creation answer. This epic **adopts that task** as track-B phase B4 and does not write a second spec (`surveys/04 §0.2`).
- **The public API is sound.** `af.<Search>(...)` and `search.fit(model, analysis)` stay as they are. Adding a search is expensive for four other reasons (`surveys/01` headline):
  - no declared contract: the only `@abstractmethod` is `_fit`, plus about 10 implicit duties;
  - roughly 900–1,000 lines of copy-paste (`Fitness(...)` ×11, the samples tail ×12);
  - a 1,691-line `NonLinearSearch` that bundles 14 concerns, about 22% of which is test-mode bypass;
  - five `search_internal` persistence strategies, plus an emcee hack in `paths` and three global-config mutations.
- **JAX is patchy because nothing declares it** (`surveys/02` verdict).
  - Four probes answer "is this JAX?", three knobs mean "compile it", and there are four ways to build the compiled callable.
  - A JAX analysis given to Emcee, Zeus or Drawer runs **eager `jnp` with no warning: 7.80 ms per call against 0.29 ms jitted**. PyAutoLens and PyAutoGalaxy analyses default to `use_jax=True`, so `af.Emcee` on `al.AnalysisImaging` hits this by default.
  - NSS fails late: a numpy analysis crashes inside the blackjax trace, and any model assertion crashes the trace.
  - `Nautilus(force_x1_cpu=True)` with a numpy analysis crashes.
  - BFGS-on-JAX takes finite differences of a jitted function.
  - `Fitness.grad` has no callers.
- **The documentation does not scale** (`surveys/03 §3`).
  - One new search touches **about 51 hand-edited files across about 20 repos**; about 16 of those files are pure roster lists.
  - Nautilus, the default sampler everywhere, has no RTD API page and no cookbook section. Seven of the 15 searches have no API page.
  - Seven files still claim that per-search YAML config exists. PySwarms and MultiNest are still documented after their removal.
- **Architecture: one registry, generated outward.**
  - Capability facts become class attributes on each search. `search/registry.py` collects them.
  - Docs, the RTD capability matrix, llms.txt, the three assistants' rosters, and the Brain SamplerSurface are all generated from its versioned manifest; Fit applies its own test-mode budgets through Nerves' generic mode API.
  - The runtime gate enforces the same flags, so docs and behaviour cannot drift.
  - `NonLinearSearch` is decomposed into collaborators; a `FitContext` plus a `run(ctx)` hook (frozen in A1, bridged in A2) cuts a new search's backend code to ~120–250 lines plus one registry entry and ~6 PyAutoFit edits (§4 R12).
- **Benchmark repos.**
  - `autofit_inference` is the public, every-search, toy-problem catalogue of record. Its first benchmark is `gaussian_x3_blend` (10 parameters, ordered centres) under a pre-registered protocol; producer-asserted verdicts go to Insight.
  - `autofit_profiling` finds where `search.fit` spends its time and reports it to Pulse.
- **Plan.** Track A (PyAutoFit framework) runs A0–A5 and track B (benchmark repos) runs B1–B5; every phase can ship on its own. **Start now with A0a(i), A0c and B1 (human gate: two `gh repo create`)**, then A0b → A0a(ii), A1 and B2, then A2‖A3 → A3b and the B3 pilot.
- **Reviewed 2026-10-07** by Codex gpt-6-astra and Claude Fable (high); the collated decisions D1–D22 are in §8 and are already applied to §1–§7.

## 1. Research findings

### 1.1 The search package today (`surveys/01 §1–§8`)

**Inventory.** There are 15 public concrete searches, 9 backends, 3 family bases and 3 sub-family bases (`surveys/01 §1`).

- Exports are at `autofit/__init__.py:98-113`. NSS and SMC are lazy, through `_LAZY_ATTRS` at `:211-215`.
- The `_fit` bodies vary widely in size: MultiStart 829 lines, SMC 312, NUTS 243, NSS 199, down to Drawer at 62.
- `multi_start_gradient/search.py` is 2,258 lines on its own.
- Search defaults live in `__init__` signatures. YAML search config was removed in #1202 (`463612878`), but `config/non_linear/README.md` still describes `mcmc/nest/mle.yaml`.

**The contract is implicit** (`surveys/01 §2`). A concrete search overrides some mix of the following hooks:

- `_fit`, `samples_via_internal_from` and `samples_info_from`;
- `output_search_internal` and `apply_test_mode`;
- `backend`/`checkpoint_file` and `__identifier_fields__`.

Every constructor arg must also be stored as `self.<arg>`, because `to_dict` reads them back for `files/search.json` (`paths/directory.py:385`). The duties every `_fit` re-implements are:

| Duty | Instances |
|---|---|
| Build `Fitness(...)` | 11 call sites (guarded only by the AST test `test_quick_update_wiring.py`) |
| Pool selection | 4 mechanisms (`make_sneaky_pool`, `make_pool`, Dynesty `_fork_pool_cls`, Nautilus `_LikelihoodWorkerPool`) |
| Initializer → start points | 8 identical `samples_from_model(...)` calls; `plot_start_point` called by hand in 4 |
| Resume detection | 7 idioms |
| Chunked `perform_update` loop | 9 loops; Dynesty and Nautilus bypass `_steps_until_full_update` |
| Samples tail (`Sample.from_lists → Samples*`) | 12 copies |

Bugs that had to be fixed N times are evidence of this cost: #1420/#1422 (chunk int casting), #1628 (discard/thin pairing) and #1442/#1443/#1630 (`pool(1)` deadlock). There were 77 commits to `search/` since 2026-06-01, 26 of them to `abstract_search.py` (`surveys/01 §8`).

**God class** (`surveys/01 §3`). `abstract_search.py` holds:

- paths selection (`:189-217`) and config reads (`:219-264`);
- the thread-env warning (`:271-319`);
- the **EP adapter** (`:325-511`, 187 lines);
- logging, with `_log_process_state` duplicated verbatim at `updater.py:339-358`;
- a `timer` property that builds a new `Timer` and calls `makedirs` on every access (`:537-553`);
- the fit lifecycle (`:602-1144`);
- the **test-mode bypass** (`:894-1046`, `:1146-1374`, about 380 lines);
- persistence, chunk scheduling, updater wiring, start-point plotting and the samples fallback;
- pools, including the dead `make_sneakier_pool` at `:1672`;
- dead state: `self.iterations` (`:262`) and `self.kwargs` (`:269`).

**The family split carries little weight** (`surveys/01 §4`).

- The three bases add about 200 lines: three defaults (initializer, clipper, autocorrelation settings) and `plot_results`.
- No `isinstance(…AbstractNest|AbstractMCMC|AbstractMLE)` exists anywhere.
- The real axes are capabilities: posterior kind (weighted+evidence / chain / point), gradients, batching, pool versus vectorised, and native checkpoint.
- Several searches sit in the wrong family:
  - SMC sits under MCMC but produces weighted particles and a log-evidence, and accepts the meaningless `auto_correlation_settings` (`smc/search.py:78`).
  - NUTS shares its plumbing with MultiStart, not with Emcee.
  - NSS shares only `plot_results` with Dynesty and Nautilus.
  - Drawer is "evaluate N prior draws", not an optimiser.

**Samples and persistence** (`surveys/01 §5–§6`).

- Every `samples_via_internal_from` does the same five steps.
- There are two log-prior APIs: `log_prior_list_from`, and a per-vector `sum(log_prior_list_from_vector)` in Nautilus, NSS and Drawer.
- There are five persistence strategies: default dill; Emcee's HDF with a no-op output; NUTS/SMC duplicated hand pickle (`nuts/search.py:509-527`); saving inside `_fit` (Drawer, BFGS, MultiStart); strip-then-dill (Nautilus `:686-697`).
- `paths/directory.py:238-246` returns an `emcee.backends.HDFBackend` ("This is a nasty hack…").
- `conf.instance["output"]["search_internal"] = True` is set in the Emcee (`:108`), NUTS (`:235`) and SMC (`:286`) constructors. Merely constructing `af.Emcee()` changes whether a later Nautilus fit keeps `search_internal/`.
- `samples_from` swallows `AttributeError` (`abstract_search.py:1622`). A typo silently reads the previous `samples.csv`.
- Samples are converted 2–3× per update (`updater.py:225`, `:184`, plus the Emcee/Zeus loop). Emcee computes autocorrelation up to 6× per update.
- Search-specific output is limited to `search_internal/`, `samples_info` keys, the Samples subclass and `plot_results`; everything else is already generic.

**Hygiene bugs** (`surveys/01 §8`):

- Drawer reads `self.timer.time` unguarded under `NullPaths` (`drawer/search.py:147`) and ignores its `search_internal` argument (`:158-159`).
- Nautilus `call_search` mutates `self.iterations_per_full_update` (`:582-586`), which changes `search.json` after construction.
- `AbstractNest(number_of_cores=None)` conflicts with the `> 1` check (`abstract_nest.py:28` vs `abstract_search.py:271`).
- Emcee has no fallback for "burn-in removed everything"; Zeus does (`zeus:358-377`).
- Zeus computes `discard/thin/chain` and never uses them (`zeus:283-290`).
- Unknown kwargs such as `n_lives=` are silently swallowed by `**kwargs`, and `SettingsSearch.search_dict` relies on that to splat `use_jax_vmap` into every search.
- Dynesty uses `raise RuntimeError` as single-core control flow (`dynesty/search/abstract.py:249-250`).

### 1.2 The JAX interface (`surveys/02 §1–§4`)

- **Switches.** Two: `Analysis(use_jax=...)` (`analysis.py:88-118`), and the harness override `PYAUTO_DISABLE_JAX=1` (`autonerves/test_mode.py:256-271`), which turns `use_jax=True` into False (`analysis.py:94-95`) and is a default of the Heart smoke profile (`autofit_workspace_test/config/build/profile_smoke.yaml:12-13`). No config key exists.
- **Defaults disagree.** `af.Analysis` defaults to False. Every PyAutoGalaxy/PyAutoLens dataset analysis defaults to True, for example `lens/PyAutoLens/autolens/analysis/analysis/dataset.py:50`.
- **Graph analyses.** `AnalysisFactor` never runs `Analysis.__init__`, so it has no `_use_jax` at all. `FactorGraphModel` has its own `use_jax=False`. Probe: `child True factor MISSING graph False numpy`.
- **`Fitness`.** Dispatch is chosen once (`fitness.py:281-286`). With `use_jax=True` and neither `use_jax_jit` nor `use_jax_vmap` set, `_call` is plain eager `call`.
  - `_vmap = jax.jit(jax.vmap(call))` recompiles for each distinct batch length (`:890-893`).
  - `_grad` is unjitted and has no caller (`:926-947`).
  - Every search that hands `fitness._jit`/`.call` straight to a sampler bypasses `call_wrap`, so it loses history and quick updates.
- **Compile logging.** `log_on_first_compile` covers only `Fitness` and latents. The NUTS, SMC, NSS and MultiStart jits are not logged (`surveys/02 §1.4`).
- **Per-search state** (`surveys/02 §2`):
  - Dynesty and Nautilus: optional JAX path.
  - NSS, NUTS, SMC and MultiStart: JAX required, but **NSS has no check**.
  - Emcee, Zeus and Drawer: no JAX path.
  - BFGS: optional JAX path without `jac=`.
- **Inconsistencies I1–I7.** Four probes; three knobs; four builders; uneven fail-fast; `gradient_mode` honoured only by MultiStart (NUTS/SMC silently ignore `"forward"`); duplicated NaN/ceiling guards (NSS's copy has no assertion handling); and three invalid-value sentinels: `-inf`, `-1e99`, and NSS's sampling `-1e30` (`nss/search.py:42`; its post-fit `Fitness` uses `-1e99`).
- **Failure modes** (`surveys/02 §3`):
  - Eager JAX in Emcee, Zeus and Drawer (3.1).
  - `force_x1_cpu`+numpy crash (3.2).
  - NSS late failure on numpy or on assertions; its `Fitness` is built after sampling, so the resume sanity check runs at the end (3.3).
  - BFGS finite differences; the workspace wrongly says "use_jax=False is required by LBFGS" (`autofit_workspace/scripts/searches/mle.py:84`) (3.4).
  - x64 is forced only by an env var at `autonerves` import time and is never asserted (3.5).
  - Fork after JAX initialisation in Emcee, Zeus, the initializer and `make_pool` (3.6).
  - Dynesty's `except RuntimeError` also catches `XlaRuntimeError` (3.7).
  - Ragged-chunk retraces; MultiStart already pads (3.8).
  - The seed lives in four places, and the initializer uses the unseeded global `random`, so `seed=42` does not make NUTS reproducible (3.10).
  - Process-global pytree classifiers (`pytrees.py:105-111`) (3.13).
- **Test mode never touches JAX.** Test modes ≥2 skip `_fit` entirely (`abstract_search.py:839-844`), so the workspace smoke matrix cannot catch the failure modes above (`surveys/02 §1.9`); unit tests do run real JAX fits (e.g. `test_blackjax_smc.py`).
- **No traceability declaration** exists on `Analysis`. The nearest precedent is `latent_batch_mode` (`surveys/02 §4`).

### 1.3 Documentation surfaces (`surveys/03 §0–§4`)

- **The coverage matrix is uneven** (`surveys/03 §1`).
  - Only DynestyStatic/Dynamic, Emcee, Zeus and LBFGS have a cookbook section; the cookbook claims "every search".
  - SMC exists only as an API stub: no example, no test script, no assistant mention, and it is invisible to the Brain gap rule.
  - The Brain SamplerSurface keys on module-directory names. That gives a false positive for MultiStart and false negatives for SMC (`blackjax` dir) and BFGS (`bfgs` vs `LBFGS.py`).
- **Duplicated prose.**
  - `autolens_workspace` and `autogalaxy_workspace` `guides/modeling/searches.py` are near-duplicates (271 diff lines); the ag copy has a duplicated `__Start Point__` header.
  - Three library `api/modeling.rst` files re-list autofit searches. The PyAutoCTI one has dead `PySwarms*` autosummary targets.
  - Ten `CITATIONS.*` files list different subsets of samplers.
  - Three assistants keep independent rosters.
- **Generation precedents already exist.** PyAutoHands' `autohands/navigator.py` generates `llms-full.txt`, and the `<lib>_visualization` manifest pattern is in use (`surveys/03 §2.B, §5`).
- **Repair list.** `surveys/03 §4` lists 14 numbered inconsistencies; they are adopted verbatim as the A0c repair list (§4).

### 1.4 Benchmark and profiling infrastructure (`surveys/04 §1–§9`)

- **autolens_inference** (`surveys/04 §1`) is the template for autofit_inference.
  - It is a set of standalone scripts with a `ruff.toml` root sentinel.
  - A config-name grammar is validated by `CONFIG_NAME_RE` (`_inference_cli.py:47`). Targets look like `<instrument>/<variant>/seed<n>`.
  - Row schema v1 carries `truth_delta_sigma` and the admission bar (`per_call_s`, `likelihood_share`).
  - It has `hpc/sync` (no `push`), a WALL-BASIS gate, `build_readme.py --check`, and an exporter (`scripts/misc/tooling/export_inference_summary.py`) that hard-codes `scientific: not_assessed` (`:152`); the runner is `scripts/misc/searches/_point_runner.py`.
  - Its `inference-summary.yml` sends `insight-refresh`.
  - It applies **no automatic acceptance threshold**; a human rules in the Cortex.
- **autolens_profiling to Pulse** (`surveys/04 §2–§3`).
  - Producers write versioned summaries.
  - `catalogue.json` is `profiling-summary@2`, the live Pulse pin.
  - Drift policy `runtime-drift-2x-1ms`, with a release-sweep host pin and a load-average cap.
  - Adding a Pulse instance takes four steps and a fixture. The `repo` field must be a Mind `repos.yaml` key.
  - Pulse has only cosmetic lens assumptions: the label at `pulse/setup_browser.py:43`.
  - The Brain **profiling conductor is hard-wired** to autolens_profiling (`agents/conductors/profiling/_profiling.py:107`).
- **Insight** mirrors Pulse one-to-one and **accepts producer-asserted** `scientific.convergence/acceptance` (`insight/summary.py:239`). A pre-registered protocol in autofit_inference can therefore emit real verdicts, which autolens_inference does not (`surveys/04 §3`).
- **Seeds to reuse** (`surveys/04 §5`):
  - HowToFit `gaussian_x3` gives the shape only. It is co-centred at 50 and exchangeable (9 parameters), so label switching makes truth ill-posed.
  - `af.ex.util.simulate_dataset_1d_via_profile_1d_list_from` draws **unseeded** noise.
  - autofit_visualization has a seeded simulator pattern, and integration scripts exist per search.
  - `searches_minimal/_metrics.py` provides MLTracker (evals-to-ML, time-to-ML).
  - `nautilus_bottleneck_findings.md` reports neural-network training at 40–52%, bounds at 25–38% and likelihood at 0.6% on a 10-d, 5 µs likelihood.
- **Existing fit-side Cortex projects.** `analytic_gaussian` and `ep_toy_gaussian` already exist. Their lesson is that thresholds calibrated on 5 seeds were under-calibrated against 200 (`surveys/04 §9`).

## 2. Critique of the asks

**Ask 1: refactor `abstract_search.py` and the search package for streamlined addition. KEEP.**

- The evidence is strong. Every reliability bug class in `search/` since June came from re-deriving implicit duties by copying a peer.
- Keep the public API (the user's own judgement, confirmed by `surveys/01` headline).
- The deliverable is a **declared contract plus composition**, not a rewrite.
- Alternatives considered and rejected (`surveys/01 §9`):
  - a checklist alone: cheap, but does not stop the bug class;
  - capability mixins: MRO, `__init__` chaining and `to_dict` argument discovery make them brittle;
  - a single generic `Search` class holding backends: breaks `isinstance`, `search.json` class paths and identifier hashes.
- The recommended design is composition *inside* the existing public classes.

**Ask 2: Samples management and the internal-to-PyAutoFit format abstraction. KEEP, narrowed.**

- The adapter is only five steps. The real work is one `RawSamples` type, one log-prior helper, and a `Checkpointer` that owns `search_internal/`.
- Moving `SamplesSMC`/`NSSamples` into `samples/` is optional and requires re-export aliases, because `samples_info["class_path"]` is persisted and re-instantiated by the aggregator (`aggregator/search_output.py:369`).

**Ask 3: the mcmc/nest/mle split. RESHAPE.**

- Do not flatten; demote. The family names are the documented user mental model (workspace `searches/{mcmc,nest,mle}.py`, HowToFit tutorials 3/6/7), but that is a docs concept the registry's `posterior_kind` preserves; persisted class paths name the concrete class only.
- Delete the bases with deprecated thin subclasses for one release (D14); behaviour moves to per-`posterior_kind` default objects (R3). SMC changes posterior kind without moving its module.

**Ask 4: unify JAX. KEEP, with one rule the brief did not anticipate.**

- "A clear separation of when a search does or does not use JAX" must also cover **a non-JAX search given a JAX analysis**. That is the commonest silent failure (Emcee on a PyAutoLens analysis).
- Ruling R4: such searches still get a lazily jitted scalar objective (D10).
- Declaration (class attributes), dispatch (one factory) and enforcement (a fail-fast gate plus an `eval_shape` preflight) are three separate concerns and land in separate phases.

**Ask 5: pair with documentation across RTD and the workspaces. KEEP, and make it structural.**

- Hand-maintaining about 51 files per search is why every search added since 2025 is only partly documented.
- Facts are generated from the registry, and judgement has exactly one public home and one internal home (R7).
- Teaching stays family-level.
- Do not bring back per-search YAML. Nerves only consumes test-mode reductions.

**Ask 6: autofit_inference with a ~10-parameter 3-Gaussian model. KEEP, with three amendments.**

- (1) Fix a label convention (ordered-centre assertions plus sorted-centre relabelling, D15), or component-labelled comparisons are ill-posed.
- (2) Judge against a *reference posterior* from long runs, not against the generating truth.
- (3) Pre-register the success criteria; calibrate and freeze the tolerance bands after an exploratory pilot, which is the analytic_gaussian lesson (D16).
- The organ is Insight, not Pulse (R1a).

**Ask 7: an autofit_profiling repo "mirroring PyAutoPulse". KEEP, already filed.**

- It is a *producer* for Pulse, not a mirror of Pulse.
- The spec is the existing Pulse task, which this epic adopts (R1b).

**Ask 8: a catalogue and research wikis for autofit_assistant search recommendation. KEEP, last.**

- The consumer pages cite the catalogue at a pinned commit.
- The name must not collide with `autofit_assistant/benchmarks/`, which holds LLM prompt benchmarks. Use `catalogue/`.

## 3. Recommended architecture

**Ruling register.** Both reviews found R9–R11 undefined; each ID now has one statement and one home.

| ID | Ruling | Where |
|---|---|---|
| R1 | (a) autofit_inference reports to Insight; (b) autofit_profiling is the adopted Pulse task | §0, §3.7, B4 |
| R2 | One declarative registry, published as a versioned JSON manifest | §3.1 |
| R3 | Family bases deleted with deprecated thin subclasses; the §3.2 invariants | §3.2, A4 |
| R4 | JAX contract: one probe, one objective factory, gate after the test-mode bypass, one seed | §3.3 |
| R5 | `RawSamples` adapter; archive (`result_internal`) separate from `resume_state` | §3.4 |
| R6 | Per-fit `FitContext` and `run(ctx)`, frozen in A1, bridged in A2 | §3.5 |
| R7 | Documentation layers, facts generated and version-pinned | §3.6 |
| R8 | `gaussian_x3_blend` benchmark under a pilot-then-scored protocol | §3.7 |
| R9 | The phased two-track plan (A0–A5, B1–B5) and its start order | §4 |
| R10 | The open questions put to the human, and their rulings | §5 |
| R11 | `ideas.md` candidates, proposed and not appended | §6 |
| R12 | The expected-outcome table | §4 "Expected outcome" |

### 3.1 One registry, not two (R2)

Survey 01's `SearchSpec` (class attributes, `surveys/01 §9`) and survey 03's `SearchInfo` (a registry record, `surveys/03 §5`) are **the same object**. Keeping two would recreate the drift this epic exists to remove. Ruling: **facts are class attributes on each search, mirrored in a declarative `non_linear/search/registry.py`** (D3). Each entry is data (`class_path` string, `lazy`, `posterior_kind`, the capability attributes, install extra, upstream, citations, anchors, status); the registry never imports a search module at `autofit` import time, so `_LAZY_ATTRS` (`autofit/__init__.py:207-213`) and the Heart `unittest-nojax` leg (`lib-tests.yml:520-600`) still hold. A test, skipped where the optional dependency is absent, asserts entry == class attributes. Static capabilities are distinct from effective run capabilities (SMC yields evidence only with a prior-sampling initializer, `smc/search.py:364`).

| Attribute | Values | Source of the need |
|---|---|---|
| `jax_use` | `none` / `optional` / `required` | `surveys/02 §5.1` |
| `gradient` | `none` / `uses` | `surveys/02 §5.1` |
| `batched` | bool | `surveys/02 §5.1` |
| `honours_gradient_mode` | bool | `surveys/02 §1.6` |
| `posterior_kind` | `chain` / `weighted` / `point` | `surveys/01 §4` |
| `produces_evidence` | bool | `surveys/01 §4`, `surveys/03 §5` |
| `resumable`, `checkpointer` | bool (honest: Dynesty, Nautilus, NSS, MultiStart only), an archive `Checkpointer` class | `surveys/01 §5.4`, D5 |
| `warm_start` | `provider` / `consumer` / `neutral` | Brain faculty table, `surveys/03 §5` |
| `install_extra`, `upstream_url`, `citation_keys` | str, str, list | `surveys/03 §5` |
| `status` | `stable` / `experimental` / `archived` | `surveys/03 §5` |
| `test_mode_budget` | e.g. `{"nsteps": 10, "nwalkers": 20}` | `surveys/01 §8` (7 budget-field names) |
| `objective_target`, `invalid_value` | `log_likelihood` / `log_posterior` / `neg2_log_posterior`, sign, unit-cube or physical coordinates; sentinel `-1e99` / `-1e30` / `-inf` | `surveys/02` I7, D9 |

- **Anchors.** The registry also carries `example` (for example `autofit_workspace:scripts/searches/nest.py#Nautilus`) and `integration_test` anchors.
- **Completeness test.** A unit test asserts that every `af`-exported search is registered; it never requires sibling repos. Workspace CI checks the cross-repo anchors against the pinned release.
- **Exchange format.** `autofit search-manifest --json` (or `python -m`) publishes a versioned manifest; it is the only cross-repo format. PyAutoNerves never imports Fit's registry: Fit applies its own `test_mode_budget` through Nerves' generic mode API.
- **Field normalisation.** Survey 03's `evidence/posterior/point_estimate` booleans collapse into `posterior_kind` + `produces_evidence`. Its `jax="callback|vmap|native"` and `gpu` collapse into `jax_use` + `batched`, which the runtime can actually enforce.
- **Generated outward, never hand-edited:**
  - `docs/api/searches.rst` and an RTD capability-matrix page ("which search");
  - a fenced roster block inside the curated `llms.txt`, written by a new Hands navigator `--roster` mode (today's navigator writes only `llms-full.txt`, `navigator.py:18-21`);
  - roster blocks in the af/al/ag assistants, pinned to the installed release (`<!-- generated: search-roster @autofit X.Y -->`);
  - Brain SamplerSurface tiers, keyed by **class, not module dir**;
  - the canonical citations page.
- **Runtime enforcement.** The `fit()` gate reads the same flags.
- **Exports stay hand-written.** Survey 01 also proposed building the `af` exports and `_LAZY_ATTRS` from the registry. The completeness test guards them instead, so a new search costs one export line (counted in R12).

### 3.2 Family bases deleted with deprecated subclasses; invariants (R3)

`AbstractMCMC/AbstractNest/AbstractMLE` are deleted from the concrete searches' MRO in A4 (D14). Their modules keep exporting **deprecated thin subclasses** (distinct classes that preserve the former defaults and warn via `__init_subclass__`), removed one release later. Initializer, clipper and autocorrelation defaults move into per-`posterior_kind` default objects applied in each concrete `__init__`, never on `NonLinearSearch`. `AbstractDynesty` stays (shared backend code). The plotter becomes per-`posterior_kind`, replacing the family `plot_results`. **Invariants every phase must hold** (`surveys/01 §9`, D6, D14):

1. Public class names and `af.` export names.
2. Identifier hashes: the class `__name__` and `__identifier_fields__` values (`mapper/identifier.py:136`). A golden table of all 15 default constructions is frozen in A0a; the only change is the seed rule's table (§3.3).
3. `files/search.json` class paths and round-tripping, and the serialized constructor-argument sets (`dictable.py:146` walks `__bases__` under `**kwargs`).
4. On-disk layout and filenames, including `search_internal/*` names; old outputs are read forever and written in the current format.
5. `samples_info["class_path"]` values; any moved Samples class leaves a re-export alias.
6. The #1493 clipper tripwire (`test_identifiers.py:486-494`): `clipper` never lands on `NonLinearSearch`; BFGS/MultiStart keep it in `__identifier_fields__`.
7. `NonLinearSearch` stays a subclass of `AbstractFactorOptimiser` (`abstract_search.py:138`), so `EPOptimiser` still accepts `af.Emcee()`.
8. External subclasses keep working for one release: `autofit_workspace_developer/searches/{nss,ultranest}/search.py`, `pyswarms/abstract.py`, and Brain `sampler_pipeline/reference.md:128-129`.
9. `Result` stays one class (`result.py:330`); the brief's "results with Samples" is the Samples adapter (§3.4).

SMC moves to the `weighted` posterior kind with evidence. Its module stays at `mcmc/blackjax/smc/`.

### 3.3 JAX contract (R4)

- **Probe.** `Analysis.is_jax` is the single probe and replaces the four in I1. `AnalysisFactor` gains the attribute. Whole-graph fitting derives `FactorGraphModel.use_jax` from its children (all equal, or raise); per-factor EP allows mixed children, each factor's own flag winning (D12). `ModelAnalysis` (`model_analysis.py:9`) and hierarchical factors forward their wrapped flag; A1 specifies gradient-mode propagation and wrapper serialization.
- **Objective factory.** `Fitness.objective(kind)` with `kind ∈ {scalar, batched, value_and_grad, batched_value_and_grad}` (`surveys/02 §5.2`). `kind` is execution only; the statistical target, sign, coordinates and invalid-value policy are the search's declared `objective_target`/`invalid_value` (D9):
  - on numpy, it returns plain callables, and grad kinds raise;
  - on JAX, it returns lazily jitted callables (compile on first call; `compile=False` debug escape hatch) wrapped in `log_on_first_compile`, pads via a reusable batching helper (lifted from MultiStart `:1147-1165`), caches per kind and strips on pickle;
  - it is built on one unjitted composable objective. MultiStart keeps its own transformed-coordinate builder (finite-gradient diagnostics) on top of it. NUTS stays on a scalar log-density (blackjax builds its own `value_and_grad`); honouring `gradient_mode` there is a separate spike.
- **Deprecations.** `use_jax_jit`, `use_jax_vmap` and `SettingsSearch.use_jax_vmap` become deprecated aliases that warn for one release.
- **`jax_use=none` rule.** A `jax_use=none` ("backend does not require JAX") search given a JAX analysis **still gets a lazily jitted `objective("scalar")`**. This fixes 3.1 for Emcee, Zeus, Drawer and the initializer. Completed fits never compile just to load results (D10).
- **Fail-fast gate in `fit()`, after the test-mode bypass return** (`abstract_search.py:~841`, i.e. only when `test_mode_level() < 2`, so `PYAUTO_TEST_MODE=2` + `PYAUTO_DISABLE_JAX=1` smoke runs stay green; D2):
  - a `required` search with a numpy analysis raises `SearchException` with one shared message;
  - a `jax.eval_shape` **trace preflight** per declared objective kind (scalar/batched/grad), chaining the original traceback (`raise … from e`). It is not a validity certificate: runtime NaN/`-inf` and host-callback failures pass it (Codex #13); an optional numerical probe at a valid point is offered separately;
  - one fork rule, shipped with the factory in A2: it audits the search pools, the outer grid/sensitivity pools (`grid_search/__init__.py:266`, `:345`) and `analysis/multiprocessing.py` together, refuses explicitly rather than silently downgrading, and records effective worker/thread counts in `search.summary` (D11);
  - an x64 check (warn, or raise for a `requires_fp64` search).
- **Seed (D4).** One search-level `seed`, with `SeedSequence` fan-out: stream 0 to the initializer (which stops using global `random`), stream 1+ to the backend; grid-search children derive independent child streams. It enters the identifier through a conditional in the identifier walk when not None, never by adding `"seed"` to the base `__identifier_fields__` (which would hash the field name for every search). Legacy table:

| Search | Today | After |
|---|---|---|
| Nautilus, NSS | `"seed"` in `__identifier_fields__` (`nautilus/search.py:166`, `nss/search.py:200`) | kept; their `seed` kwarg becomes an alias of the base seed |
| NUTS, SMC | default `seed=42`, not hashed | default stays unhashed; a user-supplied seed is hashed |
| the other 11 | no seed | hashed only when not None |

  Promise: same seed → same initial points for every search; bit-identical samples only within a pinned backend/platform where demonstrated; MCMC archive searches resume statistically, not exactly.

### 3.4 Persistence (R5)

- `samples/adapter.py` holds `RawSamples(parameters, log_likelihood | log_posterior, weights, info)` and `samples_from_raw(model, raw, samples_cls)`. That is one place for the log prior, LL⇄posterior conversion, the #1628 length checks, backend-sentinel unification (`-1e99`/`-1e30`/`-inf`), and `time` and `class_path` injection. It preserves existing representations and weights (chain/point weight 1, weighted normalised; no automatic renormalisation) and specifies parameter ordering, chain/lane metadata and diagnostic ownership (D13).
- `ChainPosterior.thin(...)` is shared by Emcee, Zeus and NUTS, with Zeus's empty-chain fallback.
- **Archive versus resume (D5).** `result_internal` (the final archive: Emcee HDF, NUTS/SMC dicts) is separate from `resume_state` (true interrupted-run resume, which only Dynesty, Nautilus, NSS and MultiStart have; NUTS/SMC `_fit` start fresh, `nuts/search.py:290`). Archive Checkpointer strategies, chosen per search by class attribute:
  - `DillCheckpointer` (the default);
  - `PickleCheckpointer` (NUTS, SMC);
  - `NativeFileCheckpointer(filename, loader)` (emcee HDF, dynesty savestate, nautilus hdf5, NSS pkl).
- Each Checkpointer offers `save/load/exists/finalize` and declares `retain_after_completion`. That **deletes** the three `conf.instance[...] = True` mutations. Internal-result loading is injected through paths/result construction with format-aware legacy detection kept (the HDF detection at `paths/directory.py:238-246` moves, it is not replaced by a dill-only fallback), covering directory, database (no-op save/load, `paths/database.py:230`), null, zipped and summary-only outputs. A3's design note specifies atomic writes, corruption handling and retention precedence.
- `SearchUpdater.update` converts samples once and passes them to `visualize`.

### 3.5 Decomposition and the `run(ctx)` hook (R6)

- **Collaborators** extracted from `NonLinearSearch`:
  - `TestModeBypass`, with a generic `apply_test_mode` driven by `test_mode_budget` from a base post-init hook. BFGS, LBFGS and Drawer gain a reduction; today BFGS runs the full `maxiter=15000` at level 1.
  - `SearchFactorOptimiser`: the EP adapter, moved to `graphical/`; `optimise` stays as a 3-line delegate.
  - `SearchRuntimeSettings`, `paths_from`, `PoolFactory` and `start_points`; `FitLifecycle` extraction is deferred until A5 shows it is needed (D22).
  - Paths capabilities (`has_timer`, `supports_checkpointing`) replace the `isinstance(NullPaths)` checks.
- **Target size.** `abstract_search.py` falls to about 400–600 lines.
- **`FitContext`** gives `run(ctx)` everything a backend needs. It is created per `fit()` invocation, never stored on `self`, never serialized or copied by `copy_with_paths` (a shallow copy, `abstract_search.py:594`; grid children `grid_search/__init__.py:330`), cleaned up on exceptions, and hands snapshots to updates (D6):

| `ctx.` member | Replaces |
|---|---|
| `fitness` / `objective(kind)` | 11 `Fitness(...)` sites, 4 builders |
| `pool` | 4 pool idioms |
| `start_points(n)` | 8 initializer calls + manual `plot_start_point` |
| `resume` | 7 resume idioms (`resume_state`, D5) |
| `schedule` (`chunks()` / `next_budget(done)`) | `_steps_until_full_update`, Dynesty/Nautilus `iterations_from` |
| `update(internal)` | `perform_update(during_analysis=True)` + checkpoint save |
| `rng` | per-search seed handling |

- **The contract a new search implements:**
  - `run(ctx) -> internal`;
  - `raw_samples_from(model, internal) -> RawSamples`;
  - an optional `info_from(internal)`;
  - class attributes.
- **Migration.** A1's design note freezes the `run(ctx)` signature and `FitContext` members; A2 ships the minimal bridge and migrates Drawer and Nautilus as proofs (D7). Existing `_fit` overrides keep working until each remaining search migrates in its own PR in A5: Emcee, Zeus, BFGS; Dynesty, NSS, NUTS, SMC; MultiStart last, with its 829-line `_fit` split internally.
- **Template.** `search/_template/search.py` provides the template. Brain `skills/sampler_pipeline/reference.md` gets the new anatomy and a documentation stage.
- **New samplers.** Samplers proposed during the epic are written against the frozen `run(ctx)` on a branch, viable from A2.

### 3.6 Documentation layers (R7)

| Layer | Content | Scales with #searches? |
|---|---|---|
| PyAutoFit registry → RTD | facts, capability matrix, API pages, canonical citations (generated) | yes, automatically |
| PyAutoFit RTD prose, cookbook | family concepts, generic options; cookbook trimmed + link to matrix | no |
| autofit_workspace `scripts/searches/` | one runnable section per stable search (smoke-tested) | 1 section |
| autofit_workspace_test | one integration script per search (registry anchor) | 1 file |
| HowToFit | family-level teaching (t3, t6, t7) | no |
| al/ag guides, HowToLens/Galaxy `tutorial_searches.py` | domain advice only; link to matrix | no |
| PyAutoLens/Galaxy/CTI `api/modeling.rst` | collapse to an intersphinx link | no |
| af/al/ag assistants | roster block generated against the installed release + hand-written decision guide citing the catalogue | roster generated |
| Brain samplers faculty | internal judgement, promotion criteria; reads registry + catalogue | no |
| autofit_inference | the one public judgement home: per-search catalogue and gallery | automatic |

Survey 03 put the gallery board under "the PyAutoPulse/Eyes pattern" (`surveys/03 §5`). Ruling R1a places it under **Insight**, because the rows are inference results under `inference-summary@1`, not timings. RTD gets `autodoc_mock_imports = ["nautilus", "zeus", "blackjax", "optax"]` in A1, and both the minimal RTD env (`[docs]`) and the full-extras docs env are tested (D18).

### 3.7 Benchmark repos (R8)

**First benchmark: `gaussian_x3_blend`** (`surveys/04 §7`, adopted in substance).

- **Model.** 3 `af.ex.Gaussian` plus a constant `Background(level)` profile, for **10 parameters**.
  - Ordered-centre assertions `g0.centre < g1.centre < g2.centre` (the user-facing model; label convention in D15).
  - Broad shared priors: centre U(0,100), normalization LogUniform(1e-2, 1e2), sigma U(0.5, 30), background U(−1, 1).
- **Dataset.** 100 pixels, centres 25/45/60, σ 3/6/10, normalizations 30/50/40, background 0.02, noise σ=0.04. Simulated with `np.random.default_rng(data_seed)`, and the JSON is committed.
- **Label convention (D15).** The exporter also records sorted-centre relabelled statistics and a `modes_found` count. logZ is compared only within one backend and one assertion mechanism, with the `ln 3! ≈ 1.79` nat convention written into the protocol and validated on a constant-likelihood constrained run.
- **Reference posterior.** 3 long runs each of Nautilus (`n_live=2000`) and DynestyStatic (`nlive=1000`), computed **per backend** (numpy and JAX). They must agree on log Z within 0.2 nat and on medians within 0.1σ. A MAP reference (long MultiStart + LBFGS polish from the reference's best sample) judges optimisers.
- **Success criteria**, pre-registered in `wiki/project/protocol_gaussian_x3.md` (D16):
  - (a) point/MAP searches optimise the log posterior (`bfgs/search.py:225`; LogUniform priors add `−log x`): judged against the MAP reference; max-logL and max-logP are both recorded, never interchanged;
  - (b) posterior accuracy (feeds Insight `acceptance`): `|median − ref| / ref_σ ≤ 1`, a σ-ratio band, a posterior-predictive residual χ² and mode coverage;
  - (c) evidence searches: `|logZ − ref| ≤ 1` nat under the D15 convention;
  - convergence diagnostics are separate (feeds Insight `convergence`): R-hat/ESS for chains, dlogz termination/`n_eff` for nested.
- **Calibration.** The σ-ratio band and all thresholds, timeouts and censoring rules are calibrated on the reference runs' scatter in the pilot, then frozen. The exporter emits `scientific.convergence/acceptance` with `protocol_id` and `reason`.
- **Headline** per (search × config): **success rate** (Wilson interval), and **expected wall per right answer** (bootstrap interval; failed/timed-out attempts and warm-start provider cost included; zero-success defined); never best-seed. Each row also carries:
  - evals-to-target and time-to-target against a shared reference target (MLTracker; its JAX fallback interpolates times, `searches_minimal/_metrics.py:61`, so values are labelled observed or estimated);
  - ESS and ESS/s;
  - `compile_s`, from separate cold- and warm-cache runs;
  - the admission bar (`per_call_s`, `likelihood_share` reported as an estimate).
- **Wave 1 = exploratory pilot; it ranks nothing.** 10 search seeds, local CPU, numpy and JAX where JAX-native, on `gaussian_x3_blend` **and** the `gaussian_x3_separated` control (disjoint, non-overlapping components), so a low success rate can be attributed to the problem or the search:
  - evidence/posterior: Nautilus (`n_live` 100/200/400), DynestyStatic, DynestyDynamic, NSS, SMC;
  - posterior: Emcee and Zeus (numpy and the JAX legs this epic fixes), BlackJAXNUTS (cold from the prior, and warm from a short Nautilus);
  - point/MAP: LBFGS, BFGS, MultiStartAdam, MultiStartProdigy, MultiStartADABelief, MultiStartLion;
  - Drawer is a sanity floor and is not benchmarked. The pilot may run on current `main`, flagged `pilot`.
- **Grouping and ranking.** The catalogue groups by requested task (point/MAP, posterior, evidence), not by representation; every registered search appears as measured, unsupported, deferred or failed. Tasks are never ranked against each other.
- **Wave 2 = scored.** 50 seeds plus 5 data realisations, on a library revision frozen after A2 and A4 merge (affected searches are re-benchmarked after later semantic migrations; the toy is cheap). RAL arrays, **`--partition=ral` only, never `gpu`/`ral,gpu`/`gpu,ral`**. This is the human's hard rule of 2026-09-30: CPU arrays on `ral,gpu` occupied all 124 CPUs on euclid-ral-gpu-1/-2 and left all 8 A100s idle but unschedulable for hours (full text: `hpc_campaign_epic.md` § "Hard constraint").
- **A100 deferred.** The 100-pixel likelihood is dispatch-bound.
- **No GPU template at birth.** Ship only the `batch_cpu` template; survey 03 §5's "CPU and GPU legs" is superseded.

**Reuse** (`surveys/04 §6`):

- Copy or generalise the following from autolens_inference:
  - `_inference_cli.py`, becoming `_autofit_inference_cli.py` with the grammar `{local,ral,a100}_{numpy,jax_cpu,jax_gpu}_{fp64,fp32}`;
  - `scripts/misc/searches/_point_runner.py`, becoming `_runner.run_search(sampler=, dataset_class=, model_type=)`. The literal kwargs are needed by the faculty AST parser `_declared_cell`;
  - the `hpc/sync` CLI, the WALL-BASIS gate, `build_readme.py --check`, and `export_inference_summary.py` with `project` parametrised;
  - the `config/general.yaml` that keeps outputs.
- Copy MLTracker from `searches_minimal/_metrics.py`.
- Copy the seeded simulator pattern and `activate.sh` from autofit_visualization, merged with the RAL `PYAUTO_HPC_BASE` branch.
- **No shared package at birth.** The "project kit" (hpc/sync, WALL gate, `--check` renderers, exporters, now 3–4 copies) is a later refactor prompt, owned by Hands or Nerves.

**Registration path** (`surveys/04 §8`):

1. Mind `repos.yaml` row first (`category: project`), then `repos_sync.py --write`, `ROUTING.md` and `epics.md`, then `--check`.
2. Heart `config/repos.yaml` `excluded:`.
3. A Cortex `projects.yaml` row for **autofit_inference only**, with `partition: ral`, `assistant: autofit_assistant`, `witness_file: results/**/*.json`, and `cortex.py check`.
4. Pulse `registry.yaml` row `instance: fit`, `repo: autofit_profiling`, `profiling-summary@2`, `cortex_project: null`.
5. Insight `registry.yaml` row `instance: fit`, `repo: autofit_inference`, `inference-summary@1`, `cortex_project: autofit_inference`.
6. A Brain `FIREWALL_ALLOWLIST` entry for every Brain file that names either repo.

Organ rows must come **after** the Mind row merges, because both readers refuse unknown identities.

## 4. Phased plan

Epic slug: `search-extensibility`. The plan has two tracks; every phase ships behind the ordinary `start_dev` → `ship_library`/`ship_workspace` gates, library first. Each phase lists scope, repos, dependency, risk, verification and a one-line witness. All of track A holds the §3.2 invariants, verified by the A0 golden identifier table.

### Track A — PyAutoFit framework

#### A0 — Safety net and repair (no dependencies; order A0a(i) → A0b → A0a(ii); A0c independent)

- **A0a, conformance suite in two layers** (`surveys/01` P0; D1).
  - **Repo:** PyAutoFit, tests only.
  - **Layer (i), metadata/serialization, all 15 searches, every CI leg** (including `unittest-nojax`; the module never imports `af.NSS`/`af.SMC` at collection time): construction, `search.json` round trip and constructor-argument sets, identifiers against a **frozen golden table** of all 15 default constructions, declared capability attributes, and `conf.instance` unchanged by construction (xfail for Emcee, NUTS and SMC until A3).
  - **Layer (ii), backend execution, Heart full-extras legs only** (`lib-tests.yml` installs `[optional]`, `:114`), explicitly skipped by declared capability on `unittest-nojax`: capability-matched fixtures (numpy `MockAnalysis` for `jax_use` none/optional, a JAX `MockAnalysis` for required) at `PYAUTO_TEST_MODE=1` with real `DirectoryPaths`; it asserts the output file set, the completed-path resume, a `NullPaths` fit, the `samples_from(model, None)` fallback and the `samples_info` key sets. The module docstring states the coverage contract: every backend executes on the full-extras leg, and `importorskip` may not hide a required backend there. Layer (ii) lands after A0b, so Drawer/`NullPaths` is not an xfail.
  - **Risk:** none.
  - **Verify:** `pytest test_autofit/non_linear` on a full-extras env and with jax/blackjax/optax uninstalled.
  - **Witness:** layer (i) green on all legs; layer (ii) green on `[optional]` legs, with NSS/NUTS/SMC/MultiStart skipped on the no-jax leg by declared capability.
- **A0b, hygiene and dead code** (`surveys/01` P1).
  - **Repo:** PyAutoFit.
  - **Scope:**
    - delete `make_sneakier_pool` and `NonLinearSearch.iterations`;
    - dedupe `_log_process_state`;
    - guard Drawer's timer and honour its `search_internal` argument;
    - stop Nautilus mutating `iterations_per_full_update`;
    - narrow the `samples_from` except to `(FileNotFoundError, NotImplementedError)`, with a WARNING log;
    - delete Zeus's dead `discard/thin/chain`;
    - fix the `AbstractNest` `number_of_cores=None` default;
    - add a `self.kwargs` unknown-kwarg **warning** (not a raise), with `SettingsSearch` filtering `use_jax_vmap` to the searches that accept it;
    - convert samples once per update;
    - compute Emcee autocorrelation once per conversion;
    - fix the stale docstrings and `config/non_linear/README.md`;
    - move-only: `test_autofit/.../optimize/` → `search/mle/`, as its own commit.
  - **Dependency:** A0a layer (i) merged first; layer (ii) follows A0b.
  - **Risk:** low. The narrowed except surfaces hidden errors, which is intended.
  - **Verify:** A0a, `pytest test_autofit`, autofit_workspace smoke `searches/{mcmc,nest,mle}.py`, and workspace_test `searches/{Emcee,Zeus,DynestyStatic,Nautilus,LBFGS}.py`.
  - **Witness:** `grep make_sneakier_pool` returns zero hits, and an Emcee update computes autocorrelation once (unit test).
- **A0c, documentation and coverage repair** (`surveys/03` phase 1; "repair", not docs-only, D8).
  - **Repos:** PyAutoFit, autofit_workspace, autofit_workspace_test, autofit_workspace_developer, the af/ag assistants, PyAutoLens/Galaxy/CTI docs, autocti_workspace and PyAutoBrain.
  - **Scope:** the `surveys/03 §4` list:
    - (1–2) add Nautilus, NSS, Drawer and MultiStart×4 to `docs/api/searches.rst`, and add a Nautilus cookbook section plus its workspace mirror;
    - (3–4) remove the stale NSS claims from the workspace README and `llms.txt:28`, and mark `autofit_workspace_developer/searches/nss` as superseded;
    - (5) delete the per-search-YAML claims ×7;
    - (6–7) purge PySwarms and MultiNest ghosts from docs, CITATIONS and the bib, and add blackjax, optax and prodigy to `files/citations.bib`;
    - (8) fix the `optional_requirements.txt` reference;
    - (9) fix the staleness in `af_configure_search.md`;
    - (10) fix the SamplerSurface gap-rule bugs: false positive for MultiStart, false negatives for SMC and BFGS, and NSS double-counted;
    - (11) fix the `sampler_pipeline` Boundary → `autolens_inference`;
    - (12) fix the duplicated ag `__Start Point__` header and the HowToLens/Galaxy "LBFGS only" claims;
    - correct the "use_jax=False is required by LBFGS" line (`mle.py:84`).
  - **Separate PRs within A0c:** workspace_test integration scripts for SMC, Drawer and BFGS (executable); the Brain SamplerSurface class-keyed gap fix (item 10, parser code); and a **"Stage 5 — documentation"** in `sampler_pipeline/reference.md`, using the `surveys/03 §3` blast radius as the interim checklist.
  - **Shape:** one PR per repo for the prose repairs, plus the separate PRs above. The RTD generic example stays `DynestyStatic` (human ruling 7); item (1–2) still adds the Nautilus cookbook section.
  - **Risk:** low. Check RTD builds; the RTD floor is currently red on an autonerves pin (memory `RTDfloor`), so judge from the GitHub docs legs.
  - **Verify:** RTD/sphinx docs legs, workspace smoke, the `samplers` faculty `gaps` output.
  - **Witness:** all 15 searches appear in `docs/api/searches.rst`, and `grep -ri pyswarms` over library `docs/` returns nothing.

#### A1 — Declare, gate, registry (depends on A0a; `surveys/02` P1 + `surveys/03` P2)

- **Repos:** PyAutoFit; downstream PyAutoLens, PyAutoGalaxy and PyAutoCTI docs.
- **Scope:**
  - capability class attributes (§3.1) on all 15 searches, including `objective_target`/`invalid_value`;
  - `Analysis.is_jax`, replacing the four probes; the `AnalysisFactor` attribute; whole-graph versus per-factor EP backend rules, `ModelAnalysis`/hierarchical-factor flags, gradient-mode propagation and wrapper serialization (D12);
  - the REQUIRED fail-fast gate with one shared message (NSS gains the check), placed after the test-mode bypass return (D2);
  - the Nautilus `force_x1_cpu`+numpy fix (`use_jax_vmap=False`);
  - a declarative, lazy `search/registry.py` plus the completeness and entry==attributes tests, and the versioned `search-manifest --json` (D3);
  - **a design note freezing the `run(ctx)` signature and `FitContext` members** (D7);
  - capabilities surfaced in `search.summary`/`model.info`;
  - generated `docs/api/searches.rst` plus an RTD capability-matrix page;
  - one canonical citations page; `autodoc_mock_imports` in `docs/conf.py` (D18);
  - downstream `api/modeling.rst` ×3 collapsed to an intersphinx link.
- **Risk:** low to medium. The gate changes the error type for NUTS, SMC and MultiStart; that is acceptable.
- **Verify:**
  - attribute assertions parametrised per class; `import autofit` imports no optional backend (nojax leg);
  - a REQUIRED search with a numpy analysis raises `SearchException`; a REQUIRED search with `PYAUTO_DISABLE_JAX=1` + `PYAUTO_TEST_MODE=2` completes;
  - a FactorGraphModel inherits `use_jax`; a mixed-child EP graph still runs per factor;
  - `Nautilus(force_x1_cpu=True)` runs with numpy;
  - the docs build in the minimal `[docs]` env and the full-extras env, and a generated-file `--check`.
- **Witness:** deleting a registry entry fails the completeness test, the RTD matrix renders 15 rows from the manifest, and the `run(ctx)` design note is merged.

#### A2 — Objective factory, PoolFactory, fork rule, run(ctx) bridge (depends on A1; parallel with A3; `surveys/01` P2 + `surveys/02` P2; D8)

- **Repo:** PyAutoFit.
- **Scope:**
  - `Fitness.objective(kind)` (lazy jit, `compile=False` escape hatch; D9, D10), ported to every call site except NSS (A3b): Dynesty and BFGS → scalar; Nautilus → batched; Emcee, Zeus, Drawer and the initializer → scalar (**fixes eager JAX**); MultiStart keeps its transformed-coordinate builder on the shared objective + batching helper; NUTS → scalar log-density (gradient_mode is a separate spike); SMC → batched;
  - `make_fitness(analysis, model, **overrides)` driven by the declared target/invalid-value policy; retire `test_quick_update_wiring.py`;
  - BFGS-on-JAX gets `jac=`, keeping `call_wrap` bookkeeping through a host-side wrapper;
  - deprecation warnings for `use_jax_jit`/`use_jax_vmap`;
  - `PoolFactory` in `parallel/`, owning the EP `number_of_cores` guard, and **the one JAX fork rule** over search, grid/sensitivity and analysis pools (D11), shipped with the factory so Emcee+JAX+`number_of_cores>1` never regresses to N recompiles;
  - `start_points(model, fitness, n)` calls `plot_start_point` once;
  - **the minimal `FitContext`/`run(ctx)` bridge**, with Drawer and Nautilus migrated as proofs (D7).
- **Risk:** medium-low. Pool paths are where hangs lived (#1442/#1630); keep the semantics byte-for-byte.
- **Verify:**
  - a compile-count probe (the `test_fitness_vmap_cache.py` pattern), one compile per kind;
  - an eager-versus-jit timing guard for Emcee+JAX; JAX + `number_of_cores=2` refuses explicitly and `search.summary` records the effective counts;
  - BFGS-JAX `nfev` shows no finite differences;
  - `test_sneaky_map.py`, `test_fork_context.py`; A0a both layers for Drawer and Nautilus via `run(ctx)`; autolens_workspace smoke for Nautilus;
  - workspace_test `{Emcee,Zeus,DynestyStatic,Nautilus,Nautilus_jax,Dynesty_jax}.py` with `number_of_cores=2`.
- **Witness:** Emcee on `af.ex.Analysis(use_jax=True)` runs at jitted speed (≤2× the jit per-call time), `grep "Fitness("` under `search/` finds one site besides NSS, and Drawer and Nautilus run through `run(ctx)`.

#### A3 — Samples adapter, Checkpointer/resume split (depends on A1; parallel with A2, no `Fitness` touch; `surveys/01` P3; D5, D8, D13)

- **Repo:** PyAutoFit.
- **Scope:**
  - golden `samples.csv` tests on pickled emcee, dynesty, nautilus, NUTS and SMC fixtures, **merged before the adapter**;
  - `samples/adapter.py` (`RawSamples`, `samples_from_raw`, one log-prior helper, sentinel unification; D13);
  - `ChainPosterior.thin`, which gives Emcee the empty-chain fallback; base `samples_via_internal_from` implemented once;
  - the three archive `Checkpointer` strategies and the separate `resume_state`; `resumable` declared honestly; delete the NUTS/SMC duplicate pickle, the Emcee no-op and the three `conf.instance` mutations;
  - injected internal-result loading with format-aware legacy detection, and the design note on atomic writes, corruption and retention (D5).
- **Risk:** medium. Numerical equivalence of samples must hold byte-for-byte against the goldens.
- **Verify:**
  - the A0a `conf.instance` xfails flip to pass;
  - `test_emcee/zeus/blackjax_nuts/blackjax_smc.py`, `nss/test_checkpoint.py`;
  - kill-and-resume via `MultiStartResurrect.py` and a Nautilus kill-and-resume;
  - directory, database, null, zipped and summary-only outputs load; the aggregator loads a pre-A3 folder (Emcee HDF included).
- **Witness:** constructing `af.Emcee()` leaves `conf.instance` unchanged, the goldens are byte-identical, and a pre-A3 output folder still loads in the aggregator.

#### A3b — NSS onto Fitness, trace preflight, x64 (depends on A2 and A3; `surveys/02` P3; D2, D8)

- **Repo:** PyAutoFit.
- **Scope:** NSS onto `Fitness` via the factory (traced assertions; the sanity check moves to the start of the run); the `eval_shape` trace preflight per declared kind, after the test-mode bypass, chained tracebacks, plus the optional numerical probe; the x64 check; Dynesty's `RuntimeError` single-core control flow becomes an explicit sentinel that no longer catches `XlaRuntimeError`.
- **Risk:** low-medium.
- **Verify:** NSS with assertions under jit; the preflight raises on an `np.asarray` likelihood with the original error chained; an fp32 warning test; the D2 smoke-profile regression test.
- **Witness:** NSS fits `gaussian_x3_blend` with its ordered-centre assertions under JAX.

#### A4 — Decompose NonLinearSearch, search-level seed, family bases (depends on A2 and A3; `surveys/01` P4 + `surveys/02` P4)

- **Repo:** PyAutoFit; smoke across the downstream workspaces.
- **Scope:**
  - `TestModeBypass`, with a shared `finalize_result(samples)` and a generic `apply_test_mode` from `test_mode_budget` via a post-init hook;
  - `SearchFactorOptimiser` moves to `graphical/expectation_propagation/`, keeping the `release_search_internal` and updater cache-invalidation semantics;
  - `SearchRuntimeSettings`, `paths_from` (`FitLifecycle` deferred, D22);
  - paths capabilities;
  - the `seed` per §3.3 and D4: conditional identifier walk, the legacy table, Nautilus/NSS `seed` aliased, initializer on stream 0, grid children on child streams;
  - family bases per D14: deprecated thin subclasses, per-`posterior_kind` default objects, SMC drops `auto_correlation_settings` (old `search.json` carrying it still loads), Brain `reference.md` and the three developer-tier searches updated in the same PR set.
- **Risk:** medium.
  - EP's path mutation and memory release (the RAL comments at `:470-505`).
  - Test-mode changes reach every smoke run in every workspace (bypass levels 2/3 are heavily used in autolens_workspace).
- **Verify:**
  - `test_abstract_search.py` `TestBypass*`, `test_updater.py`, `test_autofit/graphical/*`;
  - a 2-step EP test with MockSearch;
  - autofit and autolens workspace smoke;
  - `autofit_workspace_test/scripts/graphical`;
  - same seed → identical initial points for every search; identical samples where the backend is demonstrated deterministic;
  - the golden table is byte-identical for all 15 default constructions (default, explicit-None, explicit-seed, old JSON and old incomplete-output cases tested separately); the clipper tripwire passes; serialized constructor-argument sets match;
  - subclassing a deprecated family base warns; the three developer-tier searches still run.
- **Witness:** `abstract_search.py` is ≤600 lines, BFGS at test-mode level 1 runs a reduced `maxiter`, two `Emcee(seed=1)` fits on one platform produce identical `samples.csv`, and `Nautilus().hash_list` is unchanged.

#### A5 — Remaining run(ctx) migrations, generated consumers (depends on A4; `surveys/01` P5 + `surveys/03` P3)

- **Repos:** PyAutoFit (one framework PR, then **one PR per search**), PyAutoHands, PyAutoBrain, PyAutoNerves, the af/al/ag assistants and autofit_workspace.
- **Framework scope:**
  - the base `_fit` delegates to `run(ctx)` (the bridge from A2); `FitLifecycle` only if the migrations show it is needed;
  - SMC moves to the `weighted` posterior kind;
  - the `search/_template/search.py` template;
  - the new anatomy in `sampler_pipeline/reference.md`.
- **Migration order:** Emcee, Zeus, BFGS → Dynesty, NSS, NUTS, SMC → MultiStart (Drawer and Nautilus done in A2).
- **Consumers generate, from the versioned manifest pinned to the installed `autofit.__version__` (D18):**
  - a new Hands navigator `--roster` mode writes the fenced roster block in the curated `llms.txt`;
  - the assistants write their roster blocks;
  - SamplerSurface keys tiers by class;
  - workspace CI checks the registry anchors against the pinned version, not `main`;
  - the al/ag `guides/modeling/searches.py` collapse onto domain advice plus a matrix link;
  - the capability matrix links each row to its B3 catalogue card.
- **Risk:** medium per search. Each search is gated by A0a plus its own workspace_test script, and Nautilus additionally by autolens_workspace smoke (the most-used production search).
- **Verify:** the A0a suite per migrated search, per-search unit tests, `searches/<Name>.py` (+`_jax`) end-to-end, and a template smoke (a toy search built from the template passes A0a).
- **Witness:** a new toy search written from the template passes both A0a layers in ≤250 lines with ~6 PyAutoFit edits (search file, registry entry, export line, unit test, integration script, workspace section); onboarding effort is measured on the first real new sampler.

**Track A parallelism.** A0c is independent; A0a(i) → A0b → A0a(ii) are sequential. A2 and A3 are genuinely parallel after A1 because A3 no longer touches `Fitness`; A3b follows both. Inside A5, the per-search PRs are independent.

### Track B — benchmark repos

#### B1 — Births and registration (HUMAN GATE; no dependencies)

- **Repos:** the new `fit/autofit_inference` and `fit/autofit_profiling`, plus PyAutoMind, PyAutoHeart, PyAutoCortex, PyAutoBrain and the org `.github`.
- **Scope:**
  - two `gh repo create` calls (open question §5.1);
  - skeleton PRs copied per `surveys/04 §6`, carrying the `repos_sync:*` blocks and a layout allowlist for `.claude/`+`CLAUDE.md`;
  - Mind `repos.yaml` rows, then `repos_sync --write` (run with `PYAUTO_ROOT` asserted in a private env), `ROUTING.md` and `epics.md`;
  - Heart `excluded:`;
  - a Cortex row for autofit_inference;
  - Brain `clean_slate.sh`;
  - org profile rows;
  - a RAL clone plus `hpc/sync check`;
  - adopt the Pulse task `autofit_profiling_bootstrap`: answer its open question and link it to this epic.
- **Risk:** low technically, but operational: the shared Mind checkout must be pushed via a temp worktree and cherry-pick, and a firewall-red Mind PR waits for Brain to merge first.
- **Verify:** `repos_sync --check`, `cortex.py check`, both `lint.yml` runs green, `hpc/sync check` reaches RAL.
- **Witness:** both repos are checked out at their declared paths, and `repos_sync --check` and `cortex.py check` are green.

#### B2 — autofit_inference harness, datasets, protocol, reference posterior (depends on B1 and A0a)

- **Repo:** autofit_inference.
- **Scope:**
  - `_autofit_inference_cli.py`, `_runner.run_search(...)` and MLTracker;
  - seeded `gaussian_x3_blend` and `gaussian_x3_separated` simulators with committed JSON;
  - row schema v1 plus protocol fields (relabelled statistics, `modes_found`, max-logL and max-logP, observed/estimated timing flags, stable run IDs shared with autofit_profiling);
  - `wiki/project/protocol_gaussian_x3.md`, **pre-registered before any wave-1 run**, with the D15 label/evidence convention and the D16 pilot-then-freeze rule;
  - per-backend reference-posterior runs (Nautilus and Dynesty long, 3 seeds each), the MAP reference, and the constant-likelihood constrained validation run;
  - README auto-tables;
  - the exporter emitting protocol verdicts.
- **Why it needs only A0a.** The conformance suite doubles as the per-search "standard problem" smoke, and the harness pins the PyAutoFit `main` it ran on.
- **Risk:** low. The main danger is calibrating thresholds on too few seeds, which the pilot-then-freeze rule addresses.
- **Verify:** a CI witness of 1 seed × Nautilus on the real dataset, `build_readme --check`, and exporter validation against Insight `check --offline` with a fixture.
- **Witness:** the CI leg produces an `accepted` row against the committed reference, and the protocol file predates every wave-1 row in git.

#### B3 — Wave-1 pilot, Insight registration, catalogue (depends on B2; wants A1, not blocked)

- **Repos:** autofit_inference, PyAutoInsight, PyAutoCortex, autofit_assistant (wiki campaign page).
- **Scope:**
  - Insight campaign and task `gaussian_x3_search_wave1`: the exploratory pilot, 10 seeds × the wave-1 menu × both models, local CPU, numpy+JAX, on current `main` flagged `pilot`; NSS on the blend is recorded `deferred` until A3b. Inference campaign intent lives in PyAutoInsight `campaigns.yaml`/`tasks/` (Mind `AGENTS.md` "Where work lives"); `surveys/04 §10` called it a Cortex task, but the Cortex ledger `projects/autofit_inference.md` records the runs, not the intent;
  - commit the rows;
  - Insight fixture and `registry.yaml` row `fit`;
  - `catalogue/search_catalogue.json`, keyed by search class and grouped by requested task (point/MAP, posterior, evidence), every registered search marked measured, unsupported, deferred or failed;
  - freeze the thresholds, timeouts and censoring rules in the protocol;
  - a research-wiki campaign page, one row per (model × task) verdict.
- **Risk:** low.
- **Verify:** `pyauto-insight board` and `check --offline`; `cortex.py check`; no cross-task ranking in the generated tables.
- **Witness:** the Insight board shows the `fit` instance with pilot records, the catalogue lists every registered search with a status, and the frozen thresholds are committed before any wave-2 row.

#### B4 — autofit_profiling port and epic 1 (adopts the Pulse task; depends on B1; D17)

Two repos stay: Pulse's `repo` key must be a Mind `repos.yaml` key, and each producer ships its own Pages site. Model/dataset specification and run IDs are shared with autofit_inference.

- **Repos:** autofit_profiling, PyAutoPulse.
- **B4a scope:**
  - re-home the Nautilus anatomy as `gaussian_x1/nautilus/search_fit_breakdown.py` (`axis: breakdown`);
  - a thin `profiling-summary@2` `catalogue.json` exporter (not the 1,272-line v1 renderer), validated with `--validate-with ../PyAutoPulse`;
  - Pages plus `pages_dashboard.yml` → `pulse-refresh`;
  - Pulse fixture and `registry.yaml` row `fit`;
  - update the `autofit` campaign in `campaigns.yaml`;
  - **epic 1**: a ranked bottleneck table for one `search.fit` on a fast likelihood, fed by B2/B3 `likelihood_share` rows;
  - epic 2 (the EP loop) waits for epic 1's top findings to ship.
- **B4b scope:** port `autofit_workspace_developer/{ep,graphical}` plus the analytic benchmark, reproducing the committed baselines on the release-sweep host pin; its own research-grade reproduction task.
- **Risk:** low (B4a); medium (B4b, cross-machine reproduction).
- **Verify:** Pulse `check --offline` and Pages live (B4a); reproduced baselines within their committed tolerance (B4b).
- **Witness:** the Pulse board shows the `fit` instance, and epic 1's table is filed as a Pulse campaign entry.

#### B5 — Consumers, scored wave 2, second model (depends on B3, and on A2 + A4 for wave 2; wants A5's generated roster)

- **Repos:** autofit_assistant (and al/ag roster blocks via A5), PyAutoBrain, PyAutoMemory, autofit_inference.
- **Scope:**
  - `autofit_assistant/wiki/core/concepts/search_selection.md`, plus an `af_configure_search.md` update citing `catalogue/search_catalogue.json` at a pinned commit;
  - a samplers-faculty `PYAUTO_FIT_INFERENCE` mature-tier surface, with a `FIREWALL_ALLOWLIST` entry;
  - fix the `run_point_search` vs `run_search` AST mismatch in passing;
  - a `PyAutoMemory/wiki/methods/concepts/sampler-benchmarks.md` entry;
  - scored wave 2 on RAL `--partition=ral`: 50 seeds, 5 data realisations, on the library revision frozen after A2 and A4 (D16 vii);
  - a second model family (candidates from `surveys/03 §5`: multimodal, high-D correlated, funnel);
  - file the "project kit" refactor prompt.
- **Risk:** low. Wave 2 is subject to the RAL partition rule, and `HPCPullPyAuto` must never run with jobs in flight.
- **Verify:** assistant smoke, the faculty `gaps`/`tiers` output, `cortex.py check`.
- **Witness:** `af_configure_search` cites a pinned catalogue commit, and the samplers faculty lists autofit_inference cells as the mature tier.

### Cross-track dependencies and start order

| Track B phase | Needs from track A | Why |
|---|---|---|
| B2 | A0a | conformance suite = per-search standard-problem smoke |
| B3 | A1 (wanted, not blocking); A3b for NSS on the blend | registry groups the catalogue; NSS assertions need the `Fitness` move |
| B5 wave 2 | A2 and A4 (blocking) | a scored wave needs the factory and the seed on a frozen revision |
| B5 | A5 (wanted) | generated roster blocks in the assistants |
| (A5 → B3) | — | A5's capability matrix links each row to its B3 catalogue card |

**Recommended start order:**

1. Now: A0a(i), A0c, plus B1 (human gate).
2. Then: A0b → A0a(ii), A1 and B2.
3. Then: A2 ‖ A3, then A3b; the B3 pilot (B4a any time after B1).
4. Then: A4, then A5 with its per-search PRs, and B5 (wave 2 after A4).

### Expected outcome (R12; `surveys/01 §9`, `surveys/03 §3`)

| Metric | Today | After A5 |
|---|---|---|
| `abstract_search.py` lines | 1,691 | ~400–600 |
| Lines a new search writes | ~400–700 (copying a peer's `_fit`) | ~120–250 (backend-specific only); this is the real saving |
| Implicit duties per `_fit` | ~10 | 0 (supplied by `FitContext`) |
| Edits for a new search | ~15 across repos | ~6 (search file, registry entry, export line, unit test, integration script, workspace section) |
| Hand-edited documentation files per new search | ~51 across ~20 repos (upper-bound inventory) | ~10–12 (16 roster lists generated, ~4 guides collapsed; the rest is legitimate per-search prose) |
| `Fitness(...)` call sites | 11 | 1 |
| Ways to build the compiled likelihood | 4 | 1 (`Fitness.objective`) |
| "Is this JAX?" probes | 4 | 1 (`Analysis.is_jax`) |
| `search_internal` persistence | 5 strategies + paths hack + 3 config mutations | 3 archive `Checkpointer`s + an honest `resume_state` |
| Cross-search conformance tests | none | metadata layer on every leg; execution layer for every backend on full-extras legs |
| Searches with an RTD API page | 8 of 15 | all, generated |
| Public, dated "which search" evidence | none (private PyAutoMemory) | autofit_inference catalogue via Insight, re-run each release |

Onboarding effort is judged on the first new sampler written against `run(ctx)`, not on line counts.

## 5. Risks and open questions for the human

1. **Create the two GitHub repos now?** The names would be `PyAutoLabs/autofit_inference` and `PyAutoLabs/autofit_profiling`. *Recommend yes.* B1 blocks all of track B, and the Pulse task has been waiting on this answer since 2026-10-04.
2. **Label switching: ordered-centre assertions or disjoint priors?** *Recommended assertions;* superseded by the ruling below (D15).
3. **SMC posterior kind → `weighted` with evidence?** *Recommend yes.* It produces weighted particles and `log_evidence`. The module path stays, and stored `class_path` values are unchanged.
4. **Seed in the identifier only when not None?** *Recommend yes.* Existing output paths do not fork; seeded runs get distinct folders.
5. **Deprecate the `use_jax_jit`/`use_jax_vmap` kwargs with warnings for one release?** *Recommend yes,* then remove them. `autolens_inference` passes `use_jax_vmap=True` today (`_point_runner.py:543-544`), so it needs a one-line follow-up.
6. **Family bases as shims, or delete them?** *Recommended shims;* superseded by the ruling below (D14). Both reviews showed that class paths persist the concrete class only.
7. **Switch the RTD generic example from `DynestyStatic` to `Nautilus`?** *Recommend yes;* this matches every workspace and assistant (`surveys/03 §4.14`). Fold it into A0c or A1.
8. **Should new samplers already in flight wait for A5's `run(ctx)`?** *Recommend: write them against `run(ctx)` on a branch* and rebase when A5's framework PR merges, rather than adding a sixteenth copy of the old pattern.


### Human rulings on §5 (2026-10-07)

1. Create both repos: **yes**.
2. Label switching: **decided (D15).** The model keeps ordered-centre assertions; the exporter adds sorted-centre relabelled statistics and `modes_found`; logZ is compared only within one backend and one assertion mechanism under the `ln 3!` convention; reference posteriors are per backend; the disjoint `gaussian_x3_separated` control runs in wave 1. Plain-language explanation in §8.
3. SMC → weighted/evidence posterior kind: **yes**.
4. Seed in the identifier only when not None: **yes**.
5. Deprecate `use_jax_jit` / `use_jax_vmap` with warnings for one release: **yes**.
6. Family bases: **delete, with deprecated thin subclasses for one release (D14).** Defaults move to per-`posterior_kind` objects in each concrete `__init__`; `AbstractDynesty` stays.
7. RTD generic example: **stays `DynestyStatic`** — Nautilus is slow on fast likelihoods; do not switch.
8. In-flight samplers target the `run(ctx)` hook on a branch: **yes**.

Further risks, no decision needed:

- **Test-mode changes in A4 reach every workspace smoke.** Schedule A4 away from a release.
- **The A3 samples-equivalence goldens must exist before the adapter lands** (now an explicit A3 step).
- **Named policy defaults (D20):** one release of deprecated subclasses for external code; the D4 seed table; exact resume where the backend checkpoints, statistical otherwise, declared per search; old outputs read forever; MAP and ML both recorded; timeouts and false-acceptance rate frozen after the pilot; cold and warm both reported; the toy benchmark re-runs after each PyAutoFit release as its witness.
- **Benchmark honesty.** A `pure_callback` under a single jit can look 20–30× faster than it is, and a timing taken right after compile read 2.4× steady state. Time with warm-up (`surveys/04 §9`).
- **Firewall CI ordering and dashboard-dirty birth PRs** (autolens_inference birth precedent).
- **Nothing inherited.** Treat `comparison.txt` as motivation only for autofit_inference and re-measure. The Pulse task does port the EP baselines as evidence, by its own witness.

## 6. Candidate tasks for `ideas.md` (scholar mode; propose, do not append)

- [from: research search-extensibility · architect] Brain intake: honour declared `Target:`/`Epic:` headers instead of re-deriving them (known header mangling on filing).
- [from: research search-extensibility · surveys/02 §1.2] PyAutoNerves: `build/lib` holds more than 20 recursively nested `build/lib` copies. Route it to a hygiene sweep for packaging debris.
- ~~[from: research search-extensibility · surveys/04 §0] The workspace-root `AGENTS.md` routing table omits PyAutoInsight.~~ Resolved: the table was regenerated on 2026-10-07 and now lists Insight (D21).
- [from: research search-extensibility · surveys/02 §1.9] PyAutoFit/Nerves: add a test-mode level that compiles the JAX objective once (`eval_shape` or one jitted call). Test modes 2/3 never touch JAX today, so the smoke matrix cannot catch tracer failures (A0a layer (ii) covers unit CI).
- [from: research search-extensibility · surveys/04 §3] Brain: the profiling conductor is hard-wired to `autolens_profiling` (`_profiling.py:107`). Generalise it to the Pulse registry before autofit_profiling needs triage.

## 7. Resume note

- **State.** The report and prompt are drafted, reviewed twice (`search_extensibility_epic_reviews/01_codex_gpt6_astra.md`, `02_claude_fable_high.md`) and amended with decisions D1–D22 (§8); every §5 question is ruled. No code was edited and nothing is committed. Surveys live beside this file.
- **Next human action.** Run B1 (two `gh repo create`), and confirm the D20 policy defaults if any should differ.
- **Then.** File A0a(i), A0c (prose plus its separate script and Brain PRs) and B1 through `start_dev`: one issue per repo per phase, library first; A0b and A0a(ii) follow.
- **Tracking.** The epic slug is `search-extensibility`. Phase witnesses are in §4; the ruling register R1–R12 is at the top of §3.
- **Where surveys disagreed and the ruling won:**
  - Survey 03's separate `SearchInfo` record → one class-attribute registry (§3.1).
  - Survey 03's Pulse/Eyes gallery home and its "CPU and GPU legs" → Insight, CPU-only at birth (§3.6–§3.7).
  - Survey 01's registry-built `af` exports → optional; exports stay hand-written in A1 (§3.1).
  - Survey 04's "Cortex task" for wave 1 → an Insight campaign/task plus the Cortex run ledger (§4 B3, per Mind `AGENTS.md`).

## 8. Collated review and final decisions (2026-10-07)

Two independent read-only reviews were run against PyAutoFit `main` @ e807cc531:

- **Codex** — `search_extensibility_epic_reviews/01_codex_gpt6_astra.md`: verdict "amend before implementation"; 28 findings (5 blocker, 20 major, 3 minor), cited `Codex #n`.
- **Fable** — `search_extensibility_epic_reviews/02_claude_fable_high.md`: verdict "right shape, two blockers"; 15 findings (2 blocker, 5 major, 8 minor), cited `Fable Fn`. 29 of its 31 spot-checks held exactly; the two misses are D21 corrections.

The architect collated both reviews into decisions D1–D22. Every decision below is already applied to §0–§7. The reviews agree on direction (declared contract + composition, one factory, one adapter); they disagree only on Q2 (D15) and on the shape of Q6's compatibility layer (D14).

### 8.1 Decisions

- **D1 — Accept** (Codex #1 (blocker), #2; Fable F8; applied in §4 A0a).
  - A0a splits: (i) metadata/serialization for all 15 searches on every leg; (ii) backend execution with capability-matched numpy/JAX `MockAnalysis` fixtures on full-extras legs only, skipped on `unittest-nojax`.
  - The coverage contract forbids `importorskip` hiding a required backend on full-extras.
  - A0b lands before layer (ii), so Drawer/`NullPaths` is not an xfail.
- **D2 — Accept** (Fable F1 (blocker); Codex #13; applied in §1.2, §3.3, A1, A3b).
  - The REQUIRED gate and the trace preflight run after the test-mode bypass return (`abstract_search.py:~841`). `PYAUTO_DISABLE_JAX` is named as the second switch.
  - Regression test: REQUIRED + `PYAUTO_DISABLE_JAX=1` + `PYAUTO_TEST_MODE=2` completes.
  - The preflight runs per declared kind, chains `raise … from e`, and is called a trace preflight, not a validity certificate; an optional numerical probe is separate.
- **D3 — Accept both** (Fable F2 (blocker); Codex #15, #17; applied in §3.1, A1, A5).
  - The registry is declarative and lazy (`class_path`, `lazy`, mirrored attributes); it never imports search modules at `autofit` import time.
  - A test checks entry == class attributes where the dependency is present.
  - A versioned `search-manifest --json` is the only cross-repo format.
  - Nerves never imports Fit's registry.
  - Static and effective capabilities are distinct.
  - Exports stay hand-written, guarded by the completeness test, and the "2 touch points" claim is corrected.
- **D4 — Accept, specified** (Codex #3 (blocker), #4; Fable F3; applied in §3.3, A4).
  - The seed is hashed via a conditional in the identifier walk, never via the base `__identifier_fields__`.
  - The legacy table keeps Nautilus/NSS's static `"seed"` (kwarg aliased) and NUTS/SMC's unhashed default 42.
  - Golden byte-identity is tested for all 15.
  - Reproducibility is scoped honestly: initial points always, samples per pinned platform, MCMC archive resume statistical.
  - The initializer moves off global `random`; grid children get child streams.
- **D5 — Accept** (Codex #5 (blocker), #6; applied in §3.1, §3.4, A3).
  - `resume_state` is separate from `result_internal`, and `resumable` is honest (NUTS/SMC are not: `nuts/search.py:290`).
  - Loading is injected through paths/result with format-aware legacy detection kept; directory, database, null, zipped and summary-only outputs are covered.
  - Atomic writes, corruption and retention go in A3's design note.
- **D6 — Accept** (Codex #7; Fable F11, F5; applied in §3.2, §3.5).
  - `FitContext` is per `fit()` call, never on `self`, never serialized or copied by `copy_with_paths`, and cleaned up on exceptions.
  - New invariants 6–9 cover the `AbstractFactorOptimiser` base, the three developer-tier subclasses with Brain `reference.md:128-129`, and the single `Result`.
- **D7 — Accept** (Codex #24, top-change 2; Fable R6 row, §5.8; applied in §3.5, A1, A2, A5).
  - A1 freezes the `run(ctx)` signature in a design note; A2 ships the bridge and migrates Drawer and Nautilus.
  - Human ruling 8 is viable from A2.
- **D8 — Accept** (Fable F7, F10; Codex #24; applied in §4).
  - A2 = factory + PoolFactory + start_points + fork rule + bridge.
  - A3 = adapter + Checkpointer/resume with no `Fitness` touch, goldens first.
  - A3b (after both) = NSS onto `Fitness`, preflight, x64, Dynesty sentinel.
  - A0c is relabelled "repair", and its scripts and Brain parser fix are separate PRs.
- **D9 — Accept-amended** (Codex #9, #10; applied in §1.2, §3.1, §3.3, A2).
  - `kind` is execution only; `objective_target` and `invalid_value` are declared per search.
  - NSS's sampling sentinel is `-1e30` (`nss/search.py:42`), corrected in §1.2.
  - NUTS stays on a scalar log-density, and `gradient_mode` for NUTS becomes a spike, not a phase promise.
  - MultiStart keeps its builder on the shared objective + batching helper.
- **D10 — Accept-amended** (Codex #11; Fable F10; applied in §3.3, A2).
  - Lazy jit by default, a `compile=False` escape hatch, no compile to load a completed fit, test modes 2/3 keep their bypass.
  - The wording becomes "backend requires JAX" / "has a batched fast path".
- **D11 — Accept** (Codex #12; applied in §3.3, A2).
  - The fork rule audits search, grid/sensitivity (`grid_search/__init__.py:266`, `:345`) and `analysis/multiprocessing.py` pools together; it refuses explicitly and records effective counts in `search.summary`.
- **D12 — Accept** (Codex #14; applied in §3.3, A1).
  - Whole-graph fitting requires agreement; per-factor EP allows mixed children. `ModelAnalysis`, hierarchical factors, gradient-mode propagation and wrapper serialization are specified in A1.
- **D13 — Accept** (Codex #8; Fable R5 row; applied in §3.4, A3).
  - Representations and weights are preserved, with no automatic renormalisation.
  - Ordering, chain/lane metadata and diagnostic ownership are specified.
  - Sentinel unification belongs to the adapter.
- **D14 — Decided: delete with deprecated thin subclasses** (Codex §5 Q6; Fable §5 Q6, F4, F5; human lean; applied in §3.2, A4, §5).
  - (see 8.3).
- **D15 — Decided: reconciled** (Codex #18 (blocker), §5 Q2; Fable §5 Q2, F12(e); applied in §3.7, B2, §5).
  - (see 8.2).
- **D16 — Accept** (Codex #19 (blocker), #20, #21, #22, #25, #23; Fable F12; applied in §3.7, B2, B3, B5).
  - (i) Optimisers are judged against a MAP reference, with max-logL and max-logP both recorded; the column is renamed "point/MAP".
  - (ii) Accuracy acceptance is separate from convergence diagnostics; a predictive check and mode coverage are added.
  - (iii) The σ-ratio band is calibrated in the pilot, then frozen.
  - (iv) Wave 1 is a pilot that ranks nothing; wave 2 (50 seeds, `ral` only) ranks, with Wilson intervals, bootstrapped wall-per-success, failures and provider cost included, and zero-success defined.
  - (v) Timings are labelled observed or estimated, with a shared target and cold/warm runs.
  - (vi) The catalogue groups by task, lists every search with a status, and adds SMC, BFGS, ADABelief, Lion and the Emcee/Zeus JAX legs.
  - (vii) The scored wave runs on a revision frozen after A2 and A4.
- **D17 — Accept** (Fable F13; Codex #26; applied in B4).
  - Two repos are confirmed.
  - B4a = breakdown + exporter + Pulse row + epic-1 table; B4b = EP/graphical baseline port.
  - Model specification and run IDs are shared.
- **D18 — Accept** (Codex #16; Fable F14; applied in §3.1, §3.6, A1, A5).
  - Generated blocks pin `autofit.__version__` in the fence, and workspace CI compares against that pin.
  - RTD gets `autodoc_mock_imports`, and the minimal and full-extras docs envs are both tested. `llms.txt` gets a fenced block from a new navigator `--roster` mode; curated prose is untouched.
- **D19 — Accept** (Fable F6; Codex #17; applied in R12 table, A5).
  - Documentation files ~51 → ~10–12; ~6 PyAutoFit edits; the real saving is the 400–700-line `_fit` → 120–250 lines.
  - Onboarding is measured on the first new sampler.
- **D20 — Accept** (Codex #27; applied in §5).
  - Named policy defaults are recorded in §5 "Further risks".
- **D21 — Accept** (Fable §2 #10, #11, F15; Codex §2 rows 19, 29, 30, 31; applied in §1, §6).
  - Line, path and claim corrections, listed in 8.4.
- **D22 — Reject / partially reject** (Codex §5 Q2 (disjoint first); Codex #24 and R6 row (defer collaborators); applied in §3.5, §3.7).
  - (see 8.5).

**Coverage of the remaining findings.** Codex #17 → D3/D19; #23 → D16(vii) plus the B3 rule that NSS on the blend stays `deferred` until A3b; #24 → D7/D8; #25 → D16(vi); #26 → D17; #28 and Fable F15 (R9–R11 undefined) → accepted: the §3 ruling register defines R9 (phased plan), R10 (open questions) and R11 (`ideas.md` candidates). Fable F9 → D2 (preflight per kind, chained traceback; its measurement that the preflight costs ~0 because jit reuses the trace is recorded). Codex §2 row 27 (family bases are not persisted) → D14 and the §2 Ask 3 rewording.

### 8.2 Q2, label switching, in plain terms (D15)

The model has three Gaussians of identical form. Swapping the labels "g0", "g1" and "g2" leaves the predicted curve unchanged, so every good fit has 3! = 6 equivalent copies in parameter space, one per label permutation. "Did the search recover g1's centre?" therefore has no answer until a convention fixes which component is which. The predictive curve, the evidence and other permutation-invariant quantities stay well defined; label-specific comparisons do not (Codex §5 Q2). There are three conventions:

- **(a) Ordered-centre assertions** (`g0.centre < g1.centre < g2.centre`). This is what users actually run, and it keeps one mode. However, it is implemented differently on the two backends. On numpy a violated assertion raises and the sampler resamples; on JAX it is an `xp.where` penalty with a per-search sentinel (`fitness.py:370-445`, `:512`). The two backends therefore see different effective prior volumes, and logZ can shift by up to ln 6 ≈ 1.79 nat, which is more than the 1-nat tolerance (Codex #18, Fable F12(e)).
- **(b) Disjoint centre priors.** Each component gets its own centre range. This is a different, easier model, trivially identifiable with a normalised prior (Codex's preference for the scored baseline).
- **(c) Exchangeable priors plus post-hoc relabelling.** Sort each sample by centre, then compare; logZ is compared after adding ln 3!. This is backend-neutral and keeps multimodality visible as a diagnostic (Fable's addition).

**Decision.** `gaussian_x3_blend` keeps (a), because it is the user-facing model. The exporter also records (c): sorted-centre relabelled statistics and a `modes_found` count. The logZ criterion applies only within the same backend and the same assertion mechanism, with the ln 3! convention written into `protocol_gaussian_x3.md` and validated on a constant-likelihood constrained run. Reference posteriors are computed separately for numpy and JAX. The `gaussian_x3_separated` control, which is option (b) with disjoint, non-overlapping components, moves into wave 1. A low success rate on the blend can then be attributed to the problem (Fable F12(d): g1/g2 overlap into a degenerate ridge) or to the search.

### 8.3 Q6, family bases (D14)

Both reviews recommend deletion. There are no `isinstance` uses, no `af` exports, and `search.json` and the identifier name only the concrete class (Codex §2 row 27, §5 Q6; Fable §5 Q6). The two reviews differ on the compatibility layer. Fable proposed `AbstractNest = NonLinearSearch`-style aliases. Codex showed that aliasing collapses type identity and loses the former constructor defaults.

**Decision.** In A4, delete the three bases from the concrete searches' MRO. Their modules export distinct deprecated thin subclasses that keep the old defaults and warn via `__init_subclass__`; they are removed one release later. Defaults move into per-`posterior_kind` objects applied in each concrete `__init__`, never on `NonLinearSearch`, so the #1493 clipper tripwire (`test_identifiers.py:486-494`) still passes and BFGS/MultiStart keep `"clipper"` hashed (Fable F4). SMC drops `auto_correlation_settings` when it becomes `weighted`. Brain `reference.md` and the three developer-tier subclasses are updated in the same PR set (Fable F5). `AbstractDynesty` stays. Serialized constructor-argument sets are compared as well as hashes (`dictable.py:146`).

### 8.4 Minor corrections applied (D21)

- Nautilus strip-then-dill is at `nautilus/search.py:686-697`, not `:673`.
- Dynesty's control flow is at `dynesty/search/abstract.py:249-250`.
- Dropped: the claim that the SMC corner plot is unweighted (`samples_plotters.py:98` already passes `weight_list`), and the claim that per-search unit tests are empty (`test_blackjax_smc.py` runs a real JAX fit). Neither appeared in this report's body; both came from the surveys.
- "CI cannot catch" is narrowed to "the smoke matrix cannot catch".
- §1.4 now gives the `scripts/misc/{tooling,searches}/` paths.
- The root `AGENTS.md` table now lists PyAutoInsight (regenerated 2026-10-07); the §6 candidate is resolved.

### 8.5 Rejections (D22)

- **Codex's "disjoint priors first" as the scored baseline: rejected.** The `separated` control gives the disjoint-prior baseline inside wave 1 without changing the user-facing model (D15).
- **Codex's "defer collaborators without demonstrated reuse": partially rejected.** `PoolFactory`, `Checkpointer`, `TestModeBypass` and the EP adapter each already have three or more call sites (`surveys/01 §2–§3`), so they stay. `FitLifecycle` extraction is deferred until A5 shows it is needed.

### 8.6 Residual tensions noted while applying the decisions

- **D4 versus invariant 2 for user-seeded NUTS/SMC.** NUTS/SMC do not hash `seed` today (`nuts/search.py:37-42`; the SMC fields at `smc/search.py:52`), so an existing `BlackJAXNUTS(seed=7)` run is unhashed. Hashing a user-supplied seed re-keys those output folders. Distinguishing "default 42" from "user passed 42" also needs a sentinel default. A4's golden table must include an explicit-seed NUTS/SMC case and its accepted re-key.
- **D8 moves the Dynesty `RuntimeError` work from A2 to A3b.** Its single-core control flow (survey 01) and its `XlaRuntimeError` swallowing (survey 02 §3.7) are now fixed together in A3b; A2's pool work leaves Dynesty's pool selection byte-for-byte.
- **D16(vi) versus Codex #23.** NSS cannot run the blend's assertions before A3b, so the pilot records it as `deferred` rather than `failed`.
