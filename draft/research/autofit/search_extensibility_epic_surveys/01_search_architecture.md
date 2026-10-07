# 01 — PyAutoFit non-linear search architecture audit

Scope: `fit/PyAutoFit` @ `main`, package `autofit/non_linear/` (search, samples, paths,
updater, result, config, tests). Read-only audit, 2026-10-07. All paths below are relative to
`fit/PyAutoFit/autofit/non_linear/` unless prefixed otherwise.

**Headline.** The public API (`af.<Search>(...)`, `search.fit(model, analysis)`) is sound and
`fit()` already gives every search a single lifecycle. The cost of adding a search comes from
four other places:

1. **There is no declared contract.** A concrete search has to implement an undocumented mix of
   `_fit`, `samples_via_internal_from`, `samples_info_from`, `output_search_internal`,
   `apply_test_mode`, and sometimes `backend`/`checkpoint_file`. It also has to remember about ten
   cross-cutting duties inside `_fit`: building the `Fitness`, building the pool, the initializer,
   resume, the chunked `perform_update` loop, `plot_start_point` and the test-mode shrink. Nothing
   enforces these duties.
2. **The core is copy-paste.** `Fitness(...)` is built 11 times, the `Sample.from_lists → Samples*`
   block 12 times, the MCMC burn-in/thin block twice, the pickle backend twice, the
   `"time": self.timer...` line 8 times and the `if is_test_mode(): self.apply_test_mode()` line 8
   times. Several bug fixes had to be made N times as a result (PyAutoFit #1420/#1422 chunk int
   casting, #1628 discard/thin pairing, #1442/#1443/#1630 pool(1) deadlock). One test
   (`test_quick_update_wiring.py`) exists only to check, by scanning the AST, that every
   copy-pasted `Fitness(...)` call forwards a kwarg.
3. **`NonLinearSearch` is a 1,691-line god class.** It bundles roughly 14 concerns. About 30% of it
   is test-mode bypass code, and about 11% is an expectation-propagation (EP) adapter.
4. **Persisting `search_internal` has 5 different strategies.** On top of that, `paths` has an
   emcee-specific hack, and three searches mutate global config to force `search_internal`
   retention.

**Recommendation (§9).** Keep the public classes and the family bases (as thin shims). Introduce
the following:

- A declarative `SearchSpec`.
- A `make_fitness()` factory.
- An `InternalState` / `SamplesAdapter` protocol, with one shared `samples_from_arrays()`
  builder.
- A `Checkpointer` strategy object.
- Extraction of the test-mode bypass, the EP adapter and the pool/parallel logic into
  collaborators.
- A parametrised conformance test suite that every search must pass.

There are six phases, each behaviour-preserving and shippable on its own.

---

## 1. Inventory

| Public class (`af.`) | Family base | Module (lines) | Backend library | Dependency | Samples class |
|---|---|---|---|---|---|
| `Emcee` | `AbstractMCMC` | `search/mcmc/emcee/search.py` (398) | emcee `EnsembleSampler` + `HDFBackend` | **core** (`emcee>=3.1.6`, h5py) | `SamplesMCMC` |
| `Zeus` | `AbstractMCMC` | `search/mcmc/zeus/search.py` (448) | zeus `EnsembleSampler` | optional (`zeus-mcmc==2.5.4`) | `SamplesMCMC` |
| `BlackJAXNUTS` | `AbstractMCMC` | `search/mcmc/blackjax/nuts/search.py` (822) + `blackjax/chains.py` (194) | blackjax NUTS (JAX, gradients) | optional (`blackjax>=1.6.2`) | `SamplesMCMC` |
| `SMC` (lazy export) | `AbstractMCMC` | `search/mcmc/blackjax/smc/search.py` (1018) + `smc/samples.py` (119) | blackjax adaptive-tempered SMC (JAX) | optional (blackjax) | `SamplesSMC(SamplesPDF)` |
| `DynestyStatic` | `AbstractDynesty → AbstractNest` | `search/nest/dynesty/search/static.py` (186) + `abstract.py` (619) | dynesty `NestedSampler` | **core** (`dynesty==2.1.5`) | `SamplesNest` |
| `DynestyDynamic` | `AbstractDynesty → AbstractNest` | `.../dynamic.py` (179) + `abstract.py` | dynesty `DynamicNestedSampler` | core | `SamplesNest` |
| `Nautilus` | `AbstractNest` | `search/nest/nautilus/search.py` (761) | nautilus `Sampler` | optional (`nautilus-sampler==1.0.5`) | `SamplesNest` |
| `NSS` (lazy export) | `AbstractNest` | `search/nest/nss/search.py` (671) + `_chunked_nss.py` (138) + `_chunked_update.py` (117) + `samples.py` (25) | blackjax `ns` (JAX) | optional (blackjax ≥1.6) | `NSSamples(SamplesNest)` |
| `BFGS`, `LBFGS` | `AbstractBFGS → AbstractMLE` | `search/mle/bfgs/search.py` (455) | `scipy.optimize.minimize` | core (scipy) | `Samples` (base) |
| `Drawer` | `AbstractMLE` | `search/mle/drawer/search.py` (186) | none (initializer draws) | — | `Samples` (base) |
| `MultiStartAdam`, `MultiStartADABelief`, `MultiStartLion`, `MultiStartProdigy` | `AbstractMultiStartGradient → AbstractMLE` | `search/mle/multi_start_gradient/search.py` (**2,258**) + `convergence.py` (105) | optax (JAX, gradients) | core-ish (`optax`, marker-gated) | `Samples` (base) |
| (test double) `MockSearch` | `NonLinearSearch` | `mock/mock_search.py` (161) | — | — | `MockSamples` |
| (not a search) `SearchGridSearch`, `Sensitivity` | wrappers | `grid/…` | — | — | — |

Counts: **15 public concrete searches**, 9 distinct backends, 3 family bases and 3 sub-family
bases (`AbstractDynesty`, `AbstractBFGS`, `AbstractMultiStartGradient`). The shared core is
`search/abstract_search.py` (1,691 lines) plus `search/updater.py` (358). The package totals
about 25.2k lines.

`_fit` size (from the AST): MultiStart **829**, SMC 312, NUTS 243, NSS 199, Zeus 164, BFGS 154,
Dynesty 133, Emcee 131, Nautilus 75 (it delegates to `fit_x1_cpu`/`fit_multiprocessing`/
`call_search`), Drawer 62. `__init__` size: MultiStart 408, SMC 226, NUTS 192, NSS 160,
Nautilus 117. Most of this is docstrings plus repeated base-class kwargs.

Exports live in `autofit/__init__.py:98-113` (eager imports). `NSS` and `SMC` are lazy through
`_LAZY_ATTRS` (`autofit/__init__.py:211-215`). Docs: `docs/api/searches.rst` lists only Dynesty×2,
Emcee, Zeus, BlackJAXNUTS, SMC, BFGS and LBFGS. **Nautilus, NSS, Drawer and all four MultiStart
classes are missing** from the API docs.

Config: `config/non_linear/` contains only `GridSearch.yaml` and a **stale README** that
describes `mcmc.yaml`/`nest.yaml`/`mle.yaml`. Those files were removed when the YAML search
config was replaced by Python defaults in #1202 (commit `463612878`). The only per-family config
left is `config/visualize/plots_search.yaml` (keys `nest`/`mcmc`/`mle`). Search defaults now live
entirely in each `__init__` signature, which is good.

---

## 2. The contract today (what a concrete search must implement)

Nothing declares the contract: the only `@abstractmethod` is `_fit`
(`abstract_search.py:1376`). Everything else is discovered by reading peers. The table maps what
each search actually overrides.

| Hook | Base default | Overridden by | Notes / duplication |
|---|---|---|---|
| `_fit(model, analysis) -> (search_internal, fitness)` | abstract (`:1376`) | all 15 (10 implementations) | Each one rebuilds `Fitness`, the pool, the initializer, resume and the update loop; see below. The return tuple shape is a convention only. |
| `samples_via_internal_from(model, search_internal=None)` | raises `NotImplementedError` (`:1626`) | all 10 implementations | The `Sample.from_lists(...)` + `Samples*(...)` tail is copy-pasted **12×** (`grep Sample.from_lists` = 12). The `search_internal or <load>` preamble appears in 3 spellings (`or self.backend`, `or self.paths.load_search_internal()`, `if … is None:`). |
| `samples_info_from(search_internal=None)` | none (not on base) | Emcee, Zeus, NUTS, SMC, Dynesty, Nautilus, NSS (7). BFGS, Drawer and MultiStart build it inline | `"time": self.timer.time if self.timer else None` appears 8×. Drawer uses `self.timer.time` unguarded (`drawer/search.py:147`), which raises `AttributeError` under `NullPaths` because `timer` returns `None`. |
| `output_search_internal(search_internal)` | `paths.save_search_internal` dill (`:1394`) | Emcee (no-op, `emcee/search.py:250`), NUTS and SMC (identical direct pickle, `nuts:509`, `smc:662`), Dynesty (dill + delete checkpoint, `abstract.py:592`), Nautilus (strip pools, dill, delete checkpoint, `nautilus:673`) | 5 persistence strategies; see §5. |
| `apply_test_mode()` | no-op (`:1384`) | 8 searches, each followed by an `if is_test_mode(): self.apply_test_mode()` tail in `__init__` | The base docstring says "Called during `__init__`", but the base never calls it. **BFGS, LBFGS and Drawer never reduce** (BFGS runs the full `maxiter=15000` at level 1). MultiStart handles it in `convergence.py:71` instead. |
| `_test_mode_samples_info()` | `{}` (`:1277`) | NUTS, SMC | Opt-in, and documented well. |
| `plot_results(samples)` | raises `NotImplementedError` (`:1690`) | the 3 family bases only (`abstract_mcmc.py:47`, `abstract_nest.py:69`, `abstract_mle.py:30`) | This is the only real family-specific behaviour (see §4). |
| `backend` / `backend_filename` properties | — | Emcee (HDF), NUTS, SMC (pickle, byte-identical) | NUTS and SMC duplicate about 35 lines. |
| `checkpoint_file` property | — | Dynesty (`savestate.save`), Nautilus (`checkpoint.hdf5`), NSS (`nss_checkpoint.pkl`) | 3 names and 3 `try/except TypeError` NullPaths guards. |
| `auto_correlations_from` | — | Emcee, Zeus, NUTS | Emcee and Zeus differ only in the library call. |
| `iterations_from` | — | Dynesty, Nautilus | Each re-derives "NullPaths ⇒ run the whole budget" (`dynesty/abstract.py:376`, `nautilus:639`). |
| `__identifier_fields__` | `()` (`:323`) | every concrete class | Defines the output-folder hash; the choice per search is ad hoc (BFGS/MultiStart hash only `("clipper",)`, while Nautilus hashes 10 fields). |
| `__init__` | base 175 lines | all | 8–9 of the 10 base kwargs (`name, path_prefix, unique_tag, initializer, iterations_per_quick_update, iterations_per_full_update, number_of_cores, silence, session`) are re-declared and re-forwarded in **14 files**. Every constructor argument must also be stored as `self.<argname>`, because `to_dict(search)` (`files/search.json`, `paths/directory.py:385`) reads constructor args back off attributes (`autonerves/dictable.py:instance_as_dict`). This is an implicit contract. |
| `quick_update_message` | `:566` | MultiStart | — |
| `search_kwargs` / `run_kwargs` / `search_internal_from` / `number_live_points` | — | Dynesty pair only | A proper template-method split; the cleanest code in the package. |

### Duties every `_fit` re-implements (none enforced)

| Duty | How it is repeated |
|---|---|
| Build `Fitness` | **11 call sites** (`grep "Fitness("`). Each passes the same 7–8 kwargs (`model, analysis, paths, iterations_per_quick_update, background_quick_update, live_visual_update`) and varies only `fom_is_log_likelihood`, `resample_figure_of_merit`, `convert_to_chi_squared`, `use_jax_*`, `batch_size` and `store_history`. NSS drops the quick-update kwargs (`nss/search.py:560-567`). The AST-scanning test `test_quick_update_wiring.py` exists to catch exactly this. |
| Pool / parallelism | 4 mechanisms: `make_sneaky_pool` (Emcee only, `emcee:149`), `make_pool` (Zeus only, `zeus:173`), Dynesty's own `_fork_pool_cls` (`dynesty/abstract.py:28`), and Nautilus's `_LikelihoodWorkerPool` plus `fork_context` (`nautilus:37`, `:507`). `make_sneakier_pool` (`abstract_search.py:1672`) has **zero callers**. JAX searches ignore `number_of_cores`. |
| Initializer → start points | Emcee, Zeus, Drawer, Dynesty (`live_points_init_from`), NUTS, SMC, BFGS and MultiStart each call `self.initializer.samples_from_model(total_points=…, model, fitness, paths, n_cores)` with the same argument list. |
| `plot_start_point(...)` | Called manually by Emcee, Zeus, BFGS and MultiStart; others skip it. |
| Resume detection | 7 idioms: emcee `get_last_sample()` raising `AttributeError`; zeus `load_search_internal()` raising `FileNotFoundError`/`AttributeError`; dynesty checkpoint file exists; nautilus via `filepath=`; NSS pickle; NUTS/SMC `backend`; BFGS/MultiStart `load_search_internal()` dict. |
| Chunked `perform_update(during_analysis=True)` loop | Emcee, Zeus, NUTS, SMC, Dynesty, Nautilus, NSS, BFGS and MultiStart each own a `while iterations_remaining > 0` loop. `_steps_until_full_update` (`:1399`) was added after #1420/#1422 to centralise the int casting, but Dynesty and Nautilus use their own `iterations_from`. |
| `samples_from` inside the loop for convergence | Emcee and Zeus convert the samples once in the loop and `perform_update` converts again (see §8, efficiency). |

**Quantified duplication** (approximate, in lines):

| Repeated block | Instances | Lines each | Total |
|---|---|---|---|
| Fitness construction | 11 | ~10 | ~110 |
| Samples tail (`from_lists` + wrap) | 12 | ~15 | ~180 |
| Base-kwarg re-declaration + `super().__init__` | 14 | ~25 | ~350 (more with docstrings) |
| MCMC burn-in/thin/logpost-pairing (Emcee and Zeus, `emcee:292-355`, `zeus:337-422`) | 2 | ~80 | ~160 |
| Pickle backend (NUTS and SMC) | 2 | ~35 | ~70 |
| Test-mode tail plus `apply_test_mode` bodies | 8 | ~8 | ~65 |

Roughly **900–1,000 lines** of shared boilerplate. A new search copies about 150–250 lines of it
before writing any backend-specific line.

---

## 3. Responsibilities bundled into `NonLinearSearch` (`search/abstract_search.py`)

| # | Concern | Where (lines) | Size | Extractable? Proposal |
|---|---|---|---|---|
| 1 | Paths selection (Null/Directory/Database) from `name/path_prefix/session` | `__init__` `:189-217` | 30 | Yes → `paths_from(name, path_prefix, unique_tag, session, paths)` factory in `paths/__init__.py`. |
| 2 | Global config reads (`force_*_overwrite`, update cadences, `hpc_mode`, `live_visual_update`) | `:219-264` | 45 | Yes → frozen `SearchRuntimeSettings.from_config()` dataclass, created once and stored as `self.settings`. This removes the `float(...)`/HPC override branching from `__init__`. |
| 3 | Threading-env warning for `number_of_cores>1` | `:271-319` | 50 | Yes → `parallel.warn_if_threads_unpinned(n)`. |
| 4 | **EP factor optimiser adapter** (`optimise`, the `number_of_cores` guard, `SubDirectoryPaths`, visual toggles, `log_norm`, `release_search_internal`) | `:325-511` | **187** | Yes → `graphical/…/SearchFactorOptimiser(search)` wrapping any search. `NonLinearSearch` keeps `optimise` as a 3-line delegate so `AbstractFactorOptimiser` users still work. The `_visualize_fit`/`_visualize_before_fit` class attributes (`:144-145`) are EP state leaking into every search. |
| 5 | Logging (logger property, `configure_handler` decorator, `_log_process_state`) | `:96-135`, `:528-535`, `:716-735` | 70 | Yes. `_log_process_state` is **duplicated verbatim** in `updater.py:339-358` → move it to `search/diagnostics.py`. |
| 6 | Timing (`timer` property creates a new `Timer`, which runs `makedirs`, on every access) | `:537-553` | 17 | Yes → one `Timer` per fit, owned by the lifecycle (below). |
| 7 | Fit lifecycle (`fit`, `pre_fit_output`, `start_resume_fit`, `result_via_completed_fit`, `post_fit_output`) | `:602-1144` (excluding test mode) | ~330 | Yes → `FitLifecycle`/`SearchRunner` that owns the steps around `_fit`. `fit()` stays as the public entry point and delegates. JAX device logging (`:643-656`) moves here too. |
| 8 | **Test-mode bypass and repair** (`_fit_bypass_test_mode`, `_build_fake_samples`, `_test_mode_valid_parameter_vector`, `_test_mode_samples_after_rejected_fit`, `_test_mode_samples_info`) | `:894-1046`, `:1146-1374` | **~380 (22%)** | Yes → `search/test_mode.py: TestModeBypass(search)`. It already depends only on `model`, `analysis` and `paths`. `start_resume_fit` keeps one `if mode>=2: return bypass.run(...)` line. |
| 9 | Search-internal persistence | `:1394-1397`, `post_fit_output` `:1119-1144` | 30 | Yes → `Checkpointer` strategy (§5). |
| 10 | Chunk scheduling (`_steps_until_full_update`, `_check_step_count`) | `:1399-1473` | 75 | Keep it, but extend it so Dynesty and Nautilus use it too. A `UpdateSchedule` value object could own the remaining-budget arithmetic for all searches. |
| 11 | Updater wiring (`_updater` cache invalidation, `perform_update`, `perform_visualization`) | `:1475-1554` | 80 | Already extracted to `SearchUpdater`. The remaining issue is that the updater receives *callables* from the search (`samples_from`, `plot_results`) and the cache-invalidation logic exists because of EP path mutation (concern 4). |
| 12 | Start-point plotting | `:1556-1600` | 45 | Move into the updater (`updater.visualize_start_point`). Call it from the shared initializer helper (§9 Phase 2) so searches stop calling it by hand. |
| 13 | Samples loading fallback (`samples_from`) | `:1602-1630` | 30 | Becomes `SamplesAdapter` (§5). It currently swallows `AttributeError`, which hides real bugs in `samples_via_internal_from`. |
| 14 | Pools (`make_pool`, `make_sneaky_pool`, `make_sneakier_pool`, `check_cores`) | `:70-93`, `:1632-1685` | 80 | Yes → `parallel/pools.py: PoolFactory(number_of_cores, paths)`. Delete `make_sneakier_pool`, which is dead. |
| 15 | Dead state | `self.iterations=0` (`:262`; the updater keeps its own `_iterations`), `self.kwargs` (`:269`; never read) | — | Remove `self.iterations`. Make `self.kwargs` the place where an unknown-kwarg warning fires (see §8). |

Once concerns 4 and 8 move out, the file falls to about 1,100 lines. The full design in §9 takes
it to roughly 400 lines of genuine "search" behaviour: settings, the `_fit` hook, the samples hook
and the plot hook.

---

## 4. The mcmc / nest / mle split

What each family base actually adds:

| Base | Adds | Lines |
|---|---|---|
| `AbstractMCMC` (`search/mcmc/abstract_mcmc.py`) | default initializer `InitializerBall(0.49,0.51)`; `auto_correlation_settings` attribute; `plot_results` → `corner_cornerpy` gated by `samples.pdf_converged` and `plots_search.mcmc` | 60 |
| `AbstractNest` (`search/nest/abstract_nest.py`) | default `InitializerPrior()`; rejects `InitializerParamBounds`; `plot_results` → `corner_anesthetic` gated by `plots_search.nest`. The docstring describes a "stuck sampler auto-terminate" feature **that no longer exists**. Default `number_of_cores=None` (`:28`) would `TypeError` in the base `number_of_cores > 1` check if it were ever reached. | 80 |
| `AbstractMLE` (`search/mle/abstract_mle.py`) | default `InitializerBall(0.49,0.51)`; `clipper` (default `ClipperNone`); `plot_results` → parameter, log-likelihood and figure-of-merit traces gated by `plots_search.mle` | 64 |

Together that is about 200 lines of value: **three defaults (initializer, clipper,
autocorrelation settings) and one plot routine**. Nothing in the codebase type-checks the family:
`grep isinstance(.*AbstractNest|AbstractMCMC|AbstractMLE)` returns zero hits. So the split carries
no polymorphic weight beyond `plot_results`.

Misfits:

- **SMC** sits under `mcmc/` and inherits `AbstractMCMC`, but it is a tempered importance sampler.
  It produces **weighted** particles and a **log-evidence** (`SamplesSMC.log_evidence`), so it is
  closer to nested sampling than to MCMC. It accepts `auto_correlation_settings`
  (`smc/search.py:78`), which has no meaning for SMC. It also inherits the MCMC corner plot gated
  on `pdf_converged`, and the plot uses unweighted cornerpy semantics.
- **BlackJAXNUTS** is gradient-based HMC. It fits under MCMC, but it shares its gradient/JAX
  plumbing (`gradient_mode`, `use_jax`, chains diagnostics) with **MultiStart** (an MLE), not with
  Emcee or Zeus.
- **NSS** is a JAX nested sampler. It shares nothing with Dynesty or Nautilus except
  `plot_results`. Its JAX checkpointing is closer to NUTS/SMC.
- **Drawer** is not an optimiser; it is "evaluate N prior draws". It lives in MLE only to get the
  MLE plots.
- **EP / Laplace / ExactFactorFit** are `AbstractFactorOptimiser`s, not searches. That is correct.
  The coupling problem is the reverse one: every search *is* a factor optimiser (§3, concern 4).
- **GridSearch / Sensitivity** wrap searches and sit correctly outside the hierarchy.

The real axes of variation are **orthogonal capabilities**, not families:

| Capability | Searches |
|---|---|
| produces weighted samples + evidence | Dynesty×2, Nautilus, NSS, SMC |
| produces unweighted chains needing burn-in/thin (autocorrelation) | Emcee, Zeus, NUTS |
| produces a point estimate / trajectory | BFGS, LBFGS, MultiStart×4, Drawer |
| needs gradients / JAX-traced likelihood | NUTS, SMC (HMC kernel), MultiStart, NSS |
| vectorised (batched) likelihood | Nautilus (vmap), NSS, SMC, NUTS, MultiStart |
| Python multiprocessing pool | Emcee, Zeus, Dynesty, Nautilus |
| native checkpoint format | emcee HDF, dynesty savestate, nautilus hdf5, NSS pkl |

**Verdict: keep the three base classes as thin, public-compatible shims, and move behaviour into
capability objects.**

- The **posterior kind** (`PointEstimate`, `WeightedPosterior`, `ChainPosterior`) selects the
  Samples class, the plotter and the default initializer.
- **Capability flags on the `SearchSpec`** (`needs_jax`, `uses_gradients`, `parallelism ∈ {none,
  pool, vectorised}`, `has_evidence`) drive the generic code: the EP guard, the JAX logging and the
  pool creation.

Flattening the hierarchy outright is not worth the churn. Two reasons:

- Search class paths and names are persisted, so moves need alias shims. `files/search.json`
  stores the class path through `to_dict`, and the identifier hashes
  `value.__class__.__name__` (`mapper/identifier.py:136`).
- The family names are the documented user mental model (`docs/api/searches.rst`, workspace
  `scripts/searches/{mcmc,nest,mle}.py`).

Re-parenting SMC (MCMC → a "weighted/evidence" posterior kind) is done through the posterior-kind
object, not by moving the module.

---

## 5. Samples abstraction: from backend internals to `Samples`

### 5.1 Conversion path today

```
_fit() → (search_internal, fitness)
  └─ start_resume_fit (abstract_search.py:808)
       └─ perform_update(during_analysis=False)  → SearchUpdater.update (updater.py:73)
            ├─ _save_samples → self._samples_from(model, search_internal)      [conversion #1]
            │     = NonLinearSearch.samples_from (:1602)
            │         try search.samples_via_internal_from(model, search_internal)
            │         except (FileNotFoundError, NotImplementedError, AttributeError): paths.samples
            │   samples.samples_above_weight_threshold_from() → paths.save_samples  (samples.csv, samples_info.json, covariance.csv)
            │   samples.summary() → paths.save_samples_summary (samples_summary.json)
            ├─ _compute_latent_samples → analysis.compute_latent_samples → latent/samples.csv, latent/latent_summary.json
            ├─ visualize → analysis.visualize(+_combined); then _samples_from(...) AGAIN  [conversion #2] → search.plot_results
            └─ _profile_and_summarize → fitness.call_wrap(max-LH) timing → model.results, latent.results, search.summary
  └─ samples.summary() → analysis.make_result(samples_summary, samples, search_internal) → Result
  └─ analysis.save_results(+_combined); paths.completed()
fit() → post_fit_output → output_search_internal (or remove search_internal/) → paths.zip_remove()
```

Each per-search `samples_via_internal_from` performs the same five steps:

1. Resolve `search_internal` (in memory, or a backend or paths load).
2. Extract `parameter_lists`, `log_likelihood_list` (or `log_posterior_list`) and weights.
3. Compute the `log_prior_list`.
4. Call `Sample.from_lists(...)`.
5. Wrap the result in a `Samples*` class with `samples_info=self.samples_info_from(...)`.

### 5.2 Per-backend specifics

| Search | Internal object | Raw → lists | Log-prior call | Weights | Samples class |
|---|---|---|---|---|---|
| Emcee | `HDFBackend` / `EnsembleSampler` | `get_chain(discard,thin,flat)`, `get_log_prob(...)`; LL = logpost − logprior | `model.log_prior_list_from` | 1.0 | `SamplesMCMC` + `AutoCorrelations` |
| Zeus | `zeus.EnsembleSampler` (dill) | same as Emcee, plus a fallback when burn-in removes everything (**Emcee lacks this fallback**) | same | 1.0 | `SamplesMCMC` |
| NUTS | dict (pickle) | positions (S,C,D) → chain-major flatten; LL history | same | 1.0 | `SamplesMCMC` (autocorr synthesised from ESS) |
| SMC | dict (pickle) | particles, LL list | same | normalised importance weights | `SamplesSMC` |
| Dynesty | `NestedSampler` (dill) | `results.samples`, `logl`, `exp(logwt − logz[-1])` | same | nested weights | `SamplesNest` |
| Nautilus | `Sampler` (dill, pools stripped) | `posterior()` | **`sum(model.log_prior_list_from_vector(v))` per vector** | `exp(log_w)` | `SamplesNest` |
| NSS | `_NSSInternal` (dill) | positions, LL, log weights (renormalised) | per-vector, same as Nautilus | normalised | `NSSamples` |
| BFGS | `OptimizeResult`-ish dict | history if `should_plot_start_point`, else the single `x` | `log_prior_list_from` | 1.0 | `Samples` |
| Drawer | dict saved **inside `_fit`** | `parameter_lists`, `log_posterior_list` | per-vector | 1.0 | `Samples` (**ignores the `search_internal` argument and always reads from disk**, `drawer:159`) |
| MultiStart | dict (dill) | lane histories | `log_prior_list_from` | 1.0 | `Samples` |

### 5.3 Inconsistencies

1. **Two log-prior APIs**: `model.log_prior_list_from(parameter_lists=…)` in 7 searches versus a
   per-vector `sum(model.log_prior_list_from_vector(...))` loop in Nautilus, NSS and Drawer. Their
   performance differs and their semantics possibly differ too (`log_prior_list_from` may apply
   different summation or assertions). There should be one helper.
2. **Five persistence strategies for `search_internal`**:
   - (a) the default dill through `paths.save_search_internal` (Dynesty, Zeus, NSS, BFGS,
     MultiStart);
   - (b) a native HDF backend with a **no-op** `output_search_internal` (Emcee);
   - (c) a hand-rolled pickle that bypasses `paths` (NUTS and SMC, duplicated;
     `nuts/search.py:509-527`);
   - (d) a save during `_fit` (Drawer `:150`, BFGS `:330`, MultiStart `:1713`);
   - (e) stripping un-picklable members before dill (Nautilus `:673`).
3. **`paths` knows about emcee**: `DirectoryPaths.load_search_internal` probes for
   `search_internal.hdf` and returns an `emcee.backends.HDFBackend`. The code is commented "This is
   a nasty hack…" (`paths/directory.py:238-246`).
4. **Global config mutation**: Emcee (`emcee/search.py:108`), NUTS (`nuts/search.py:235`) and SMC
   (`smc/search.py:286`) set `conf.instance["output"]["search_internal"] = True` in `__init__`.
   This leaks to every later search in the process. Merely *constructing* an `af.Emcee()`
   silently changes whether a later `af.Nautilus` fit keeps its `search_internal/`.
5. **`search_internal` means two things**: a resume checkpoint (written mid-run by NUTS, SMC, BFGS
   and MultiStart) and a post-hoc results archive (written by `post_fit_output`). The config key
   `output.search_internal: false` (`config/output.yaml:56`) deletes the folder at the end. That is
   why some searches have to force it on.
6. **Samples-class persistence contract**: `Samples.__init__` stamps
   `samples_info["class_path"]` (`samples/samples.py:59-62`). Both
   `DirectoryPaths.samples` (`paths/directory.py:274`) and the aggregator
   (`aggregator/search_output.py:369`) re-instantiate that class. Moving `SamplesSMC`
   (`search/mcmc/blackjax/smc/samples.py`) or `NSSamples` (`search/nest/nss/samples.py`) therefore
   breaks every stored output unless an alias is kept. Search-specific Samples subclasses also
   live inside search packages while the generic ones live in `samples/`. This is inconsistent
   and matters for the refactor.
7. **The `samples_from` fallback swallows `AttributeError`** (`abstract_search.py:1622`). A typo
   inside any `samples_via_internal_from` silently degrades to `paths.samples`, which reads the
   *previous* `samples.csv`. During a run, that means visualising stale samples without warning.
8. **The MLE family has no `SamplesMLE`**. It returns the base `Samples`, so "point-estimate"
   semantics are implicit. This works, but it is asymmetric.

### 5.4 Proposed single adapter layer

```python
# autofit/non_linear/samples/adapter.py
@dataclass(frozen=True)
class RawSamples:                       # the ONE thing a backend must produce
    parameters: np.ndarray              # (N, D) physical space
    log_likelihood: np.ndarray | None   # (N,)  — give either LL …
    log_posterior: np.ndarray | None    # (N,)  — … or log-posterior (LL derived)
    weights: np.ndarray | None = None   # None ⇒ uniform; normalised here, once
    info: dict = field(default_factory=dict)   # backend-specific samples_info keys

def samples_from_raw(model, raw: RawSamples, samples_cls, **cls_kwargs) -> Samples:
    """Single place for log-prior (one API), LL⇄posterior, weight normalisation,
    length-correspondence checks (#1628), `time` injection, Sample.from_lists."""

class InternalState(Protocol):          # per-search (or per-backend) adapter
    def raw_samples(self, search, model) -> RawSamples: ...
    def info(self, search) -> dict: ...
```

A search then declares `posterior_kind = ChainPosterior` (→ `SamplesMCMC` + burn-in/thin +
autocorrelation helper shared by Emcee, Zeus and NUTS) and implements a single
`raw_samples_from(search_internal) -> RawSamples`. The base implements `samples_via_internal_from`
once. Emcee's and Zeus's 80-line blocks collapse into a shared `ChainPosterior.thin(chain,
log_prob, times)` with Zeus's empty-chain fallback applied to both.

Persistence becomes a `Checkpointer` strategy chosen on the spec:

| Strategy | Used by |
|---|---|
| `DillCheckpointer` | default |
| `PickleCheckpointer` | NUTS, SMC |
| `NativeFileCheckpointer(filename, loader)` | emcee HDF, dynesty savestate, nautilus hdf5, NSS pkl |

Each strategy exposes `save(obj)`, `load()`, `exists()` and `finalize()`. `finalize()` covers
checkpoint deletion and stripping un-picklable members. `paths` then only provides
`search_internal_path`, which removes the emcee hack. The `output.search_internal` retention
decision moves to `Checkpointer.retain_after_completion` (a class attribute per strategy), which
removes the global-config mutation.

---

## 6. Result / output pipeline

| File (under `output/<prefix>/<name>/<identifier>/`) | Writer | When | Generic or search-specific |
|---|---|---|---|
| `.identifier`, `files/search.json`, `files/model.json`, `model.info`, `files/info.json`, start-point info | `paths.save_all` (`paths/directory.py:373`) via `pre_fit_output` (`abstract_search.py:737`) | before fit | generic. `search.json` = `to_dict(search)` (constructor-arg attributes). |
| `files/<analysis attrs>`, `image/` before-fit visuals | `analysis.save_attributes`, `visualize_before_fit(_combined)` | before fit | analysis |
| `search_internal/.start_time`, `.time` | `Timer` | start and each update | generic, but lives *inside* `search_internal/`, so it is removed with it |
| `search_internal/<native>` | per search (§5.3) | mid-run (some) and end | **search-specific, 5 strategies** |
| `files/samples.csv`, `files/samples_info.json`, `files/covariance.csv` | `paths.save_samples` (`directory.py:309`) | every update | generic. `covariance.csv` only for `SamplesPDF`. |
| `files/samples_summary.json` | `paths.save_samples_summary` | every update | generic |
| `files/latent/samples.csv`, `latent/latent_summary.json`, `latent.results` | updater `_compute_latent_samples` | every update (config-gated) | generic |
| `image/…` analysis visuals | `analysis.visualize(+_combined)` | every update (gated) | analysis |
| `image/search/corner*.png`, traces | `search.plot_results` (family base) | every update | family-specific |
| `model.results`, `search.summary` | `paths.save_summary` (`paths/abstract.py:620`) | every update | generic. Includes the LH-call timing done by `updater._profile_and_summarize`. |
| `search.log` | `configure_handler` | during `start_resume_fit` | generic |
| `.completed` | `paths.completed()` | end | generic |
| `<identifier>.zip` (and removal of the folder) | `paths.zip_remove` | end | generic |
| `files/samples*` (aggregator inputs) | — | — | the aggregator reads `samples_info.json["class_path"]` + `samples.csv` (`aggregator/search_output.py:352`) and `samples_summary` |

Search-specific output is limited to: `search_internal/` contents, `samples_info` keys, the
Samples subclass and `plot_results`. **Everything else is already generic.** That is the strongest
argument that the remaining per-search code can shrink to "make raw samples, plus a checkpoint
strategy, plus run the backend".

Duplication and inefficiency in the pipeline:

- **Samples are converted 2–3 times per update.** `updater._save_samples` converts once
  (`updater.py:225`), `updater.visualize` converts **again** just to call `plot_results`
  (`updater.py:184`), and Emcee and Zeus convert a third time inside their loop for the
  convergence check (`emcee:225`, `zeus:~275`). For Emcee, each conversion computes
  autocorrelation times **twice**: once in `samples_info_from` (`emcee:267`) and once in the
  `SamplesMCMC(...)` constructor arguments (`emcee:353`). That is up to 6 autocorrelation
  computations per update. Fix: `update()` converts once and passes `samples` to `visualize`.
- `_log_process_state` runs on every update and at fit start, iterating over every OS process
  through psutil (`updater.py:339`, `abstract_search.py:716`). This is duplicated code, and it is
  expensive on shared nodes. Gate it behind `logging.total_files_open`.
- The test-mode bypass (`_fit_bypass_test_mode`) re-implements the tail of `start_resume_fit`
  (save samples, summary, `make_result`, `save_results`, `completed`). The two have drifted before
  (#1519, and the comments at `:1238-1255`). Once extracted, both should call one shared
  `finalize_result(samples)`.

---

## 7. Adding a new search today: touch points

Worked example: a new nested sampler `Foo` wrapping the external library `foo`.

| # | File | What | Required? |
|---|---|---|---|
| 1 | `autofit/non_linear/search/nest/foo/__init__.py` | empty package file | yes |
| 2 | `autofit/non_linear/search/nest/foo/search.py` | class: `__init__` (re-declare the 9 base kwargs plus backend kwargs, store every one as `self.x` for `search.json`, `__identifier_fields__`, test-mode tail), `apply_test_mode`, `_fit` (Fitness, pool/JAX branch, initializer, resume, chunk loop, `perform_update`), `samples_info_from`, `samples_via_internal_from`, `output_search_internal`, `checkpoint_file`, optional-dependency import guard with install message | yes (~400–700 lines when copied from Nautilus or NSS) |
| 3 | `…/foo/samples.py` | `Samples` subclass if the backend has extra diagnostics (e.g. `NSSamples`) | sometimes |
| 4 | `autofit/__init__.py` | eager import, **or** `_LAZY_ATTRS` entry if it imports JAX or a heavy dependency | yes |
| 5 | `pyproject.toml` | add to `[optional]`, with notes on PyPI git-URL constraints | yes if new dependency |
| 6 | CI workflow(s) | install extra / post-extras step if not on PyPI | sometimes |
| 7 | `autofit/config/visualize/plots_search.yaml` | only if new plot keys are needed | sometimes |
| 8 | workspace configs (`autofit_workspace/config/…`, `autolens_workspace/config/…`, …) | mirror new config keys (workspace configs override library defaults) | sometimes, ×N workspaces |
| 9 | `docs/api/searches.rst` | autosummary entry (**currently forgotten for 7 of 15**) | should |
| 10 | `test_autofit/non_linear/search/nest/test_foo.py` | unit tests (numpy-only); no shared conformance suite exists | yes |
| 11 | `test_autofit/non_linear/search/test_quick_update_wiring.py` | exemption entry if the Fitness call deviates | sometimes |
| 12 | `autofit_workspace_test/scripts/searches/Foo.py` (+ `Foo_jax.py`) | end-to-end integration script | yes (per `sampler_pipeline/reference.md` Stage 4) |
| 13 | `autofit_workspace/scripts/searches/nest.py` | user-facing example section | should |
| 14 | `autofit_workspace` notebooks (generated) | regenerated by Hands | follows 13 |
| 15 | Brain `samplers` faculty / `sampler_pipeline` records | registry / benchmark rows | process |

**Count:** 6 hard touch points in PyAutoFit (1, 2, 4, 9, 10, plus 5 for a new dependency), 2–3
in workspaces (12, 13, plus 8 when needed), and about 15 in total. The real cost is **#2: about
10 implicit duties re-derived by copying a peer**. That is where the reliability bugs came from
(#1420/#1422/#1628/#1630).

Target after the refactor:

- Touch points: (1) a `search.py` of roughly 120–250 lines implementing `SearchSpec`, `run(ctx)`
  and `raw_samples_from(internal)`; (2) one line in a **registry**. The `af.` export, docs
  autosummary, lazy-import entry and conformance-test parametrisation all derive from that
  registry.
- Plus (3) the integration script.

---

## 8. Code health

**Bugs or latent bugs**

- Global config mutation: `conf.instance["output"]["search_internal"] = True` in the Emcee, NUTS
  and SMC `__init__` (`emcee:108`, `nuts:235`, `smc:286`). A process-wide side effect of
  constructing an object.
- Drawer reads `self.timer.time` unguarded (`drawer/search.py:147`). `timer` is `None` under
  `NullPaths`, so a no-output Drawer fit raises `AttributeError`.
- Drawer's `samples_via_internal_from` ignores its `search_internal` argument (`drawer:158-159`).
  Under `NullPaths`, `load_search_internal` returns `None` → `TypeError`. The broad `except` in
  `samples_from` does not catch this.
- Nautilus `call_search` permanently mutates `self.iterations_per_full_update`
  (`nautilus:582-586`). This changes the search object, and therefore `search.json`, after
  construction.
- `AbstractNest.__init__(number_of_cores=None)` (`abstract_nest.py:28`) conflicts with the base
  check `number_of_cores > 1` (`abstract_search.py:271`). It is latent because every concrete
  class passes `1`.
- `samples_from` swallows `AttributeError` (§5.3, item 7).
- Emcee has no "burn-in removed everything" fallback, while Zeus has one (`zeus:358-377`). An
  unconverged short Emcee run can produce empty samples.

**Dead or half-finished code**

- `make_sneakier_pool` (`abstract_search.py:1672`): no callers. `SneakierPool` is used only there.
- `NonLinearSearch.iterations` (`:262`): never read. The updater tracks `_iterations` separately
  (`updater.py:59`).
- `self.kwargs` (`:269`): stored, never read. Unknown constructor kwargs (typos such as
  `n_lives=`) are **silently swallowed** by `**kwargs` in every search. `SettingsSearch.search_dict`
  (`settings.py`) passes `use_jax_vmap` to *every* search, which relies on this swallowing.
- Zeus `_fit` computes `discard`, `thin` and `chain` and never uses them (`zeus:283-290`). This is
  a wasted autocorrelation computation per chunk.
- `Nautilus.vectorized` versus `fitness.use_jax_vmap`: the x1-CPU path passes
  `vectorized=fitness.use_jax_vmap` (`nautilus:434`) and the multiprocessing path passes
  `self.vectorized` (`:530`). Two sources of truth.
- `AbstractNest` docstring describes a removed "auto-terminate when stuck" feature.
- The `apply_test_mode` base docstring says it is called during `__init__`, but it is not (each
  subclass calls it).
- `config/non_linear/README.md` documents `mcmc.yaml`/`nest.yaml`/`mle.yaml`, which no longer
  exist.
- `general.yaml` still has `output.search_internal` (`config/general.yaml:22`) alongside
  `output.yaml: search_internal` (`config/output.yaml:56`). Only the latter is read
  (`abstract_search.py:1135`).
- Tests for the MLE searches live in `test_autofit/non_linear/search/optimize/` (an old family
  name), separate from `search/mle/`.
- The Brain `sampler_pipeline/reference.md` refers to an `[nss]` extra that `pyproject.toml` no
  longer has (NSS now uses mainline `blackjax>=1.6`).

**Inconsistent naming and shapes**

- Budget names: `nsteps` (Emcee/Zeus), `num_samples` (NUTS), `maxcall` (Dynesty/Zeus),
  `n_like_max` (Nautilus), `maxiter` (BFGS), `total_draws` (Drawer), `n_steps`/`max_steps`
  (MultiStart). Each `apply_test_mode` shrinks a different field. A spec-level
  `budget_field = "nsteps"` would let one generic `apply_test_mode` work.
- Checkpoint file names: `savestate.save`, `checkpoint.hdf5`, `nss_checkpoint.pkl`,
  `search_internal.{dill,pickle,hdf}`.
- Single-core control flow in Dynesty is driven by `raise RuntimeError` inside a `try`
  (`dynesty/abstract.py:249-251`). That `except RuntimeError` also catches genuine dynesty runtime
  errors and silently reruns serially.
- `resample_figure_of_merit` is `-np.inf` for posterior-FOM searches and `-1.0e99` for LL-FOM
  searches. This is a rule (it depends on `fom_is_log_likelihood`) that every author must remember.

**Conditionals leaking into generic code**

- Test mode:
  - about 380 lines in `abstract_search.py`;
  - `is_test_mode()` inside samples conversion (Emcee `:296`, Zeus `:339`: hard-coded
    `discard=thin=5`) and inside `AutoCorrelationsSettings` (`auto_correlations.py:45`);
  - `initializer.py:86`;
  - `paths/abstract.py:27-37`;
  - `plot_util.skip_in_test_mode`.
- JAX:
  - device logging in `fit()` (`:643-656`);
  - `getattr(analysis, "_use_jax", False)` probes in `optimise`, Dynesty, Nautilus and MultiStart
    (private-attribute access on `Analysis` from 5 places);
  - `np.array(figure_of_merit)` to force asynchronous JAX execution in `updater.py:315`.
- Parallel:
  - the EP `number_of_cores` guard (`:384-408`);
  - the threading-environment warning in `__init__`;
  - per-search pool selection.
- Type checks on paths:
  - `isinstance(self.paths, DatabasePaths/NullPaths)` for timer start/update
    (`abstract_search.py:833`, `updater.py:201`);
  - `isinstance(self.paths, NullPaths)` in Dynesty, Nautilus and NSS to decide budget and
    checkpointing.

  A `paths.supports_checkpointing` / `paths.has_timer` capability would remove all of them.

**Churn signal:** 77 commits touched `search/` since 2026-06-01, 26 of them in
`abstract_search.py` alone, many of them cross-search fixes applied N times.

---

## 9. Proposed target architecture (phased, behaviour-preserving)

### Target shape (recommended design)

```
NonLinearSearch (public base; ~400 lines)        ← af.<Search>(...) and .fit() unchanged
 ├─ spec: SearchSpec (class attr, declarative)   ← budget_field, posterior_kind, capabilities,
 │                                                  checkpointer, fitness_profile, test_mode_budget
 ├─ settings: SearchRuntimeSettings              ← frozen, from config once
 ├─ hooks a search implements (the WHOLE contract):
 │     run(ctx: FitContext) -> internal            # drive the backend; ctx gives fitness,
 │                                                 #   pool, start points, resume state,
 │                                                 #   schedule.chunks(), ctx.update(internal)
 │     raw_samples_from(model, internal) -> RawSamples
 │     info_from(internal) -> dict                 # optional extra samples_info keys
 └─ collaborators (composition, all in non_linear/search/_runtime/ or similar):
       FitLifecycle      (fit/pre/post/resume/completed — today's fit()+start_resume_fit+…)
       FitnessFactory    (make_fitness(spec.fitness_profile, settings, analysis, paths))
       PoolFactory       (none | fork pool | sneaky | backend-native; EP guard lives here)
       Checkpointer      (Dill | Pickle | NativeFile; owns search_internal/ & retention)
       SamplesAdapter    (samples_from_raw + posterior_kind → Samples class, burn-in helpers)
       SearchPlotter     (per posterior_kind; replaces family plot_results)
       SearchUpdater     (exists; receives samples, not callables)
       TestModeBypass    (levels 2/3 + mode-1 repair; generic apply_test_mode via budget_field)
       SearchFactorOptimiser (EP adapter; NonLinearSearch.optimise delegates)
 AbstractMCMC / AbstractNest / AbstractMLE       ← kept as thin shims that set spec defaults
 SEARCH_REGISTRY                                 ← name → (module, class, lazy, docs section)
```

`FitContext` is the key abstraction. It hands `run()` everything a backend needs and nothing it
has to construct itself:

| Member | Replaces |
|---|---|
| `ctx.fitness` | the 11 `Fitness(...)` call sites |
| `ctx.pool` | the 4 pool idioms |
| `ctx.start_points(n)` | 8 initializer calls plus the manual `plot_start_point` |
| `ctx.resume` | the 7 resume idioms (loads through the `Checkpointer`) |
| `ctx.schedule` | `_steps_until_full_update` / `iterations_from` |
| `ctx.update(internal)` | `perform_update(during_analysis=True)` and checkpoint save |
| `ctx.log` | per-search logging |

Searches whose backend owns its loop (Dynesty and Nautilus, which take `maxcall`/`n_like_max`)
use `ctx.schedule.next_budget(done)` instead of chunk iteration.

Alternatives considered:

- **(a) Status quo plus a written checklist.** Cheapest, but it does not stop the bug class.
- **(b) Full flatten to capability mixins** (`class Emcee(ChainPosteriorMixin, PoolMixin,
  NonLinearSearch)`). Mixin MRO, `__init__` chaining and `to_dict` arg discovery
  (`get_arguments` walks `__bases__` when `**kwargs` is present) make this brittle.
- **(c) Separate "backend" objects held by a single generic `Search` class.** Cleanest in theory,
  but it breaks `isinstance(search, af.Emcee)`, `search.json` class paths and identifier hashes.

The recommended design is (c)'s composition *inside* the existing public classes.

**Invariants every phase must hold:**

- Identifier hashes stay unchanged: class `__name__` and `__identifier_fields__` values.
- `files/search.json` stays round-trippable: constructor args readable as attributes, class path
  stable.
- `samples_info["class_path"]` values for existing Samples classes stay unchanged, or are aliased.
- On-disk layout and filenames stay unchanged, including `search_internal/*` names so old runs
  resume.
- `af.` export names stay unchanged.

### Phase 0 — Conformance harness (tests only; prerequisite)

- **Scope:**
  - New `test_autofit/non_linear/search/test_conformance.py`, parametrised over every public
    search, with `pytest.importorskip` for optional dependencies.
  - Each search runs a tiny numpy Gaussian (MockAnalysis) at `PYAUTO_TEST_MODE=1` and real
    `DirectoryPaths` in `tmp_path`.
  - It asserts:
    - the output file set (`samples.csv`, `samples_info.json` with `class_path`,
      `samples_summary.json`, `model.results`, `search.summary`, `.completed`);
    - a round-trip of `search.json` → `from_dict`;
    - identifier stability against a **frozen golden table** of today's identifiers;
    - resume (a second `fit()` takes the completed path);
    - `NullPaths` fits;
    - that `samples_from(model, None)` after completion works or falls back cleanly;
    - that `conf.instance` is unchanged after construction (this fails today for
      Emcee/NUTS/SMC; mark it xfail until Phase 3).
  - Also snapshot the per-search `samples_info` key sets.
- **Files:** tests only, plus a `searches_under_test()` helper.
- **Risk:** none (tests). This is the safety net for every later phase.
- **Verify:** `pytest test_autofit/non_linear` (the JAX searches skip or are numpy-only per the
  repo rule).

### Phase 1 — Hygiene and dead code (small, mechanical)

- **Scope:**
  - Delete `make_sneakier_pool` and `NonLinearSearch.iterations`.
  - Dedupe `_log_process_state` into one module.
  - Delete the unused Zeus `discard/thin/chain` computation.
  - Guard Drawer's timer and honour the `search_internal` argument.
  - Fix the `AbstractNest` `number_of_cores=None` default.
  - Fix the stale `config/non_linear/README.md`, the `AbstractNest` docstring and the
    `apply_test_mode` docstring.
  - Move `test_autofit/non_linear/search/optimize/` to `search/mle/` (move-only PR).
  - Add the missing Nautilus/NSS/Drawer/MultiStart entries to `docs/api/searches.rst`.
  - Narrow `samples_from`'s `except` to `(FileNotFoundError, NotImplementedError)` and log the
    fallback at WARNING.
  - Convert samples **once** per update: `SearchUpdater.update` passes `samples` to `visualize`.
  - Emcee: compute autocorrelation once per conversion.
- **Risk:** low. Narrowing `except AttributeError` may surface hidden errors; that is intended.
  Run the conformance suite first.
- **Verify:**
  - Phase 0 suite and `pytest test_autofit`.
  - `autofit_workspace` smoke (`searches/mcmc.py`, `nest.py`, `mle.py`).
  - `autofit_workspace_test/scripts/searches/{Emcee,Zeus,DynestyStatic,Nautilus,LBFGS}.py`.

### Phase 2 — `make_fitness`, `PoolFactory`, `start_points` (remove the `_fit` copy-paste)

- **Scope:**
  - Add `NonLinearSearch.make_fitness(analysis, model, **overrides)`. It reads a class-level
    `fitness_profile` (`fom_is_log_likelihood`, `resample_figure_of_merit` derived from it,
    `convert_to_chi_squared`) and always forwards the quick-update, background and live-visual
    settings.
  - Replace all 11 call sites. Retire `test_quick_update_wiring.py` in favour of a unit test of
    `make_fitness`.
  - Add `PoolFactory` (move `check_cores`, `make_pool`, `make_sneaky_pool`, the Dynesty fork pool
    and the Nautilus `_LikelihoodWorkerPool`/`fork_context` into `parallel/`). It should have one
    method, `pool_for(search, fitness, kind)`. The EP `number_of_cores` guard moves there.
  - Add `start_points(model, fitness, n)`, which wraps `initializer.samples_from_model` and calls
    `plot_start_point` once.
  - Replace Dynesty's `raise RuntimeError` control flow with an explicit `use_pool` boolean.
- **Files:** `abstract_search.py`, `parallel/*`, all 10 `search.py`, `fitness.py` (no API change).
- **Risk:** medium-low. Pool paths are where hangs historically lived (#1442/#1630); keep the
  semantics byte-for-byte and add `test_fork_context.py` coverage.
- **Verify:**
  - Phase 0, `test_sneaky_map.py`, `test_fork_context.py`, `search/nest/test_dynesty.py`,
    `test_nautilus.py`.
  - Workspace_test `Emcee.py`, `Zeus.py`, `DynestyStatic.py`, `Nautilus.py`, `Nautilus_jax.py`,
    `Dynesty_jax.py` with `number_of_cores=2`.

### Phase 3 — Samples adapter and Checkpointer (one persistence and conversion path)

- **Scope:**
  - Add `samples/adapter.py` (`RawSamples`, `samples_from_raw`, one log-prior helper).
  - Add `ChainPosterior.thin(...)`, shared by Emcee, Zeus and NUTS, with Zeus's empty-chain
    fallback.
  - Base `samples_via_internal_from` is implemented once in terms of
    `raw_samples_from(model, internal)` plus `info_from(internal)`. `time` and `class_path` are
    injected centrally.
  - Add `Checkpointer` strategies (`Dill`, `Pickle`, `NativeFile`), selected per search through a
    class attribute. Delete the NUTS/SMC duplicate pickle code and Emcee's no-op override.
  - Delete the emcee hack in `DirectoryPaths.load_search_internal`: the emcee checkpointer owns
    HDF loading, and `Result.search_internal` goes through `search.checkpointer.load()`, falling
    back to the dill path for old runs.
  - Replace the three `conf.instance[...] = True` mutations with
    `Checkpointer.retain_after_completion`.
  - Keep existing filenames.
  - Optionally move `SamplesSMC` and `NSSamples` into `samples/`, leaving **re-export aliases at
    the old module paths** so stored `class_path` values resolve.
- **Files:** `samples/adapter.py` (new), `samples/*`, `paths/directory.py`, `result.py`, all
  `search.py`.
- **Risk:** medium. Numerical equivalence of samples matters (weights normalisation, log-prior
  API unification). Add golden tests that compare `samples.csv` before and after on fixed
  internals (pickled small fixtures for emcee, dynesty and nautilus results).
- **Verify:**
  - Phase 0 (flip the `conf.instance` xfail to pass), `samples/test_*`, `test_emcee.py`,
    `test_zeus.py`, `test_blackjax_nuts.py`, `test_blackjax_smc.py`, `nss/test_checkpoint.py`.
  - Resume checks: kill and restart each workspace_test search (`MultiStartResurrect.py`,
    `MultiStartResumeNaNCounters.py`).
  - Aggregator: load an output folder written *before* the phase (`database` scripts in
    `autofit_workspace_test/scripts/database`).

### Phase 4 — Decompose `NonLinearSearch` (lifecycle, test mode, EP out)

- **Scope:**
  - Extract `TestModeBypass` (`search/test_mode_bypass.py`). Bypass and the real path share one
    `finalize_result(samples)`.
  - Add a generic `apply_test_mode` driven by `spec.test_mode_budget = {"nsteps": 10,
    "nwalkers": 20}`. Call it from the base `__init__` after subclass attributes are set, via a
    `__init_subclass__`-installed post-init hook or by making the base call
    `self._post_init()`. This removes 8 tails and gives BFGS, LBFGS and Drawer a reduction.
  - Extract `SearchFactorOptimiser` (the EP adapter) to `graphical/expectation_propagation/`.
    `NonLinearSearch.optimise` delegates to it, and the EP visual flags move onto the adapter.
  - Extract `SearchRuntimeSettings` and `paths_from(...)`.
  - `FitLifecycle` takes `fit`, `pre_fit_output`, `start_resume_fit`, `result_via_completed_fit`
    and `post_fit_output`. The public method names stay as delegates.
  - Replace `isinstance(paths, NullPaths/DatabasePaths)` checks with paths capabilities
    (`paths.has_timer`, `paths.supports_checkpointing`).
- **Files:** `abstract_search.py` (target ≤ 600 lines), new modules, `updater.py`, `paths/*`,
  `graphical/expectation_propagation/*`.
- **Risk:** medium.
  - EP has subtle path-mutation and memory-release logic (RAL job comments at `:470-505`). Keep
    `release_search_internal` and the updater cache-invalidation semantics, and add an EP test
    that runs 2 factor steps with a MockSearch.
  - Test-mode changes affect every smoke run in every workspace.
- **Verify:**
  - `test_abstract_search.py` (all the `TestBypass*` classes), `test_updater.py`,
    `test_autofit/graphical/*`.
  - Smoke: `autofit_workspace` `smoke_tests.txt`, `autolens_workspace` smoke (bypass levels 2/3
    are heavily used there), EP scripts in `autofit_workspace_test/scripts/graphical`.

### Phase 5 — `SearchSpec` + `FitContext` + registry (the "new search in one file" phase)

- **Scope:**
  - Introduce `FitContext` (fitness, pool, `start_points`, resume state from the Checkpointer,
    schedule, `update(internal)`) and the `run(ctx)` hook. The base `_fit` becomes
    `ctx = FitContext(...); internal = self.run(ctx); return internal, ctx.fitness`. Existing
    searches keep overriding `_fit` until migrated, and both paths are supported.
  - Migrate the simple searches first (Drawer, Emcee, Zeus, BFGS), then Dynesty, Nautilus, NSS,
    NUTS and SMC, and MultiStart last. MultiStart's 829-line `_fit` should be split internally
    regardless.
  - Add `SEARCH_REGISTRY` in `non_linear/search/registry.py`. `autofit/__init__.py` builds its
    eager exports and `_LAZY_ATTRS` from it, and a test asserts that `docs/api/searches.rst`
    lists every registry entry.
  - Family bases become spec-default providers: `posterior_kind`, default initializer, plotter.
    SMC switches to the weighted/evidence posterior kind (corner plot via anesthetic-style
    weighting) without moving its module.
  - Add a `cookiecutter`-style template `search/_template/search.py` plus a contract doc in the
    module docstring. Update the Brain `sampler_pipeline/reference.md` Stage 3 to the new
    6-item-to-3-item anatomy.
  - Unknown-kwarg guard: warn (not raise, to stay behaviour-preserving) on kwargs not consumed by
    any `__init__` in the MRO. Make `SettingsSearch` filter `use_jax_vmap` to searches that accept
    it.
- **Risk:** medium per migrated search, but each search is migrated in its own PR, gated by the
  Phase 0 conformance suite plus that search's workspace_test script.
- **Verify:** Phase 0 suite per migrated search, the per-search unit tests, the
  `autofit_workspace_test/scripts/searches/<Name>.py` (+ `_jax`) end-to-end runs, and the
  `autolens_workspace` smoke for Nautilus (the most-used production search).

### Expected outcome

| Metric | Today | After Phase 5 |
|---|---|---|
| `abstract_search.py` lines | 1,691 | ~400–600 |
| Lines a new search writes | ~400–700 (copying a peer) | ~120–250 (backend-specific only) |
| Implicit duties per `_fit` | ~10 | 0 (supplied by `FitContext`) |
| PyAutoFit touch points for a new search | ~6 (+ docs drift) | 2 (search file + registry line) |
| `Fitness(...)` call sites | 11 | 1 |
| `search_internal` persistence strategies | 5 + paths hack + config mutation | 3 named `Checkpointer`s |
| Cross-search conformance tests | none | every search, every PR |

Suggested ordering for AI-assisted throughput: **Phases 0 and 1 immediately** (cheap, and they
unblock everything). Phases 2 and 3 can then run in parallel worktrees (they touch different
seams). Phase 4 follows, then Phase 5 as one framework PR plus one PR per search migration. New
samplers proposed during the epic should wait for Phase 5's `run(ctx)` hook, or be written
against it on a branch, to avoid adding a sixteenth copy of the old pattern.
