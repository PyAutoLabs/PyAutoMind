**§1 Verdict**

**Amend before implementation:** the direction is sound, but the current phase contracts do not reliably preserve compatibility or produce defensible benchmark rankings.  
The blockers are the conformance design, seed/identifier migration, checkpoint semantics, and benchmark target/prior definitions.  
I read the report and surveys, inspected source and CI configuration, and ran no tests or code probes; their measured performance claims remain unverified.

**§2 Factual spot-checks**

Paths below are relative to `/home/jammy/Code/PyAutoLabs`; `F/` abbreviates `fit/PyAutoFit/`. “Holds” means supported by source inspection, not runtime reproduction.

| Claim | file:line | Holds? |
|---|---|---|
| Fifteen concrete searches are exported; NSS/SMC are lazy. | `F/autofit/__init__.py:98`, `:212` | **Yes.** Thirteen eager exports plus two lazy exports. |
| Fitness without either compilation flag uses eager `call`. | `F/autofit/non_linear/fitness.py:271` | **Yes.** Dispatch does not infer compilation from the analysis. |
| JAX Emcee is 27× slower without JIT. | Survey 02 §3.1; `F/autofit/non_linear/fitness.py:281` | **Mechanism holds; timing unverified.** One toy measurement cannot establish a general factor. |
| BFGS passes a jitted function without `jac=`. | `F/autofit/non_linear/search/mle/bfgs/search.py:298` | **Yes.** |
| `force_x1_cpu` can select Nautilus’s JAX-vmap flag for a NumPy analysis. | `F/autofit/non_linear/search/nest/nautilus/search.py:330` | **Yes.** The proposed failure mechanism is supported. |
| NSS bypasses Fitness during sampling and constructs it afterward. | `F/autofit/non_linear/search/nest/nss/search.py:407`, `:560` | **Yes.** |
| NSS’s sampling sentinel belongs to the report’s `−1e99` group. | `F/autofit/non_linear/search/nest/nss/search.py:42` | **No.** Its actual sampling sentinel is `−1e30`; post-fit Fitness uses `−1e99`. |
| Emcee, NUTS and SMC constructors mutate global retention configuration. | Their `search.py`: `108`, `235`, `286` | **Yes.** |
| DirectoryPaths contains an emcee-specific HDF loader. | `F/autofit/non_linear/paths/directory.py:237` | **Yes.** |
| Drawer ignores supplied internals and reads an unguarded timer. | `F/autofit/non_linear/search/mle/drawer/search.py:147`, `:159` | **Yes.** |
| Nautilus mutates its full-update cadence during fitting. | `F/autofit/non_linear/search/nest/nautilus/search.py:582` | **Yes.** |
| `samples_from` catches `AttributeError`, potentially masking implementation errors. | `F/autofit/non_linear/search/abstract_search.py:1619` | **Yes.** Actual handler is at `:1623`. |
| Samples are independently converted for saving and plotting. | `F/autofit/non_linear/search/updater.py:184`, `:225` | **Yes.** |
| Samples class paths are persisted and dynamically loaded. | `F/autofit/non_linear/samples/samples.py:59`; `paths/directory.py:281` | **Yes.** |
| Family bases are themselves persisted as part of concrete search class paths. | `organs/PyAutoNerves/autonerves/dictable.py:221` | **No, as stated.** Serialization stores the concrete class path, not its inheritance chain. |
| No family-base `isinstance` dispatch exists. | Family definitions and references under `F/autofit/non_linear/search/` | **Holds in the inspected libraries/workspaces.** This does not establish absence in external plugins. |
| SMC’s inherited corner plot uses unweighted semantics. | `F/autofit/non_linear/plot/samples_plotters.py:98` | **No.** `corner_cornerpy` already passes `samples.weight_list`. |
| Per-search unit-test directories are essentially empty. | `F/test_autofit/non_linear/search/mcmc/test_blackjax_smc.py:458`, plus Emcee/Zeus/NUTS tests | **No.** Substantial tests exist, including an actual JAX SMC fit. |
| Test modes ≥2 bypass backend `_fit`. | `F/autofit/non_linear/search/abstract_search.py:839` | **Yes.** “Therefore CI cannot catch JAX failures” is too broad. |
| RTD API roster contains eight of fifteen searches. | `F/docs/api/searches.rst:27`, `:40`, `:55` | **Yes.** |
| PyAutoFit’s Sphinx configuration has no optional-dependency mocks. | `F/docs/conf.py:20`, `:94`; `F/.readthedocs.yaml:8` | **Yes.** RTD installs `[docs]`; Heart’s docs job installs `[optional,docs]`. |
| Insight accepts producer-declared scientific verdicts. | `organs/PyAutoInsight/insight/summary.py:236` | **Yes.** Schema acceptance is not scientific validation. |
| Pulse consumes the lens producer’s v2 catalogue. | `organs/PyAutoPulse/registry.yaml:11` | **Yes.** |
| The profiling conductor defaults to autolens_profiling. | `organs/PyAutoBrain/agents/conductors/profiling/_profiling.py:104` | **Yes.** An explicit workspace override also exists. |
| Hands currently generates `llms-full.txt`. | `organs/PyAutoHands/autohands/navigator.py:18`, `:345` | **Yes.** It explicitly does **not** modify curated `llms.txt`. |
| NUTS/SMC backend persistence constitutes interrupted-run resume support. | NUTS `search.py:290`, `:321`, `:499`; SMC `search.py:494`, `:653` | **No.** Their backend loaders serve sample reconstruction; `_fit` initializes fresh sampling state. |

**§3 Findings**

1. **[blocker] A0a cannot satisfy its stated witness.**

   A tiny **NumPy** analysis cannot run every search: NUTS explicitly rejects it, and MultiStart/SMC also require JAX.
   `importorskip` does not help when dependencies are installed but the supplied analysis is incompatible.
   Moreover, A0a requires Drawer/NullPaths to pass before A0b fixes the acknowledged failure.

   Evidence: [NUTS’s guard](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py:262), [Drawer’s failure](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mle/drawer/search.py:147), report `:423`.
   **Change:** split metadata/serialization conformance from actual backend execution; use NumPy and JAX analysis fixtures by capability, explicit backend budgets, and narrowly identified baseline xfails.

2. **[major] The actual CI matrix needs an explicit coverage contract.**

   Heart’s Python 3.12/3.13 jobs install `[optional]`; a separate no-JAX job uninstalls JAX, optax and blackjax.
   Some test comments claiming extras are absent from the Python matrix are stale.
   Unqualified `importorskip` can turn a required coverage leg green while silently dropping the search being migrated.

   Evidence: [extras installation](/home/jammy/Code/PyAutoLabs/organs/PyAutoHeart/.github/workflows/lib-tests.yml:114), [no-JAX leg](/home/jammy/Code/PyAutoLabs/organs/PyAutoHeart/.github/workflows/lib-tests.yml:578).
   **Change:** require every backend in the full-extras job, explicitly skip JAX execution in the no-JAX job, retain import/metadata checks there, and add a true base-install check if optional-dependency isolation matters.

3. **[blocker] Seed unification conflicts with the identifier invariant.**

   NUTS and SMC default to `seed=42`, but their identifier fields omit seed.
   NSS already includes seed. Consequently, “hash seed whenever non-None” changes default NUTS/SMC paths even when the user supplies no new argument.
   Moving all defaults to `None` instead changes historical random behavior and potentially NSS identifiers.

   Evidence: [NUTS fields/default](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py:37), [SMC fields/default](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/smc/search.py:52), NSS `search.py:195`.
   **Change:** retain the human’s seed ruling, but specify the legacy migration exception explicitly; test default, explicit-None, explicit-seed, old JSON and old incomplete-output cases separately.

4. **[major] A seed is not sufficient for the promised reproducibility.**

   Initializer draws use Python’s global `random`; backend RNG APIs differ.
   Exact resumed trajectories also require persisted RNG state, adaptation state and a stable chunk schedule—not merely reconstructing `SeedSequence(seed)`.
   Grid-search children need a policy for independent streams versus deliberately shared randomness.

   Evidence: [initializer draw source](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/mapper/prior_model/abstract.py:875), NUTS `search.py:406` and `:432`.
   **Change:** specify backend RNG adapters, checkpointed RNG state and child-stream derivation; promise bitwise reproducibility only within a pinned backend/platform/configuration where demonstrated.

5. **[blocker] Checkpointing and post-hoc internal loading remain conflated.**

   Three serializer strategies do not define how a sampler resumes.
   NUTS/SMC write reconstructible result dictionaries but do not restore their sampling loops; Dynesty/Nautilus have native checkpoints plus final archives.
   A generic `NativeFileCheckpointer(filename, loader)` also needs backend-specific context, including likelihoods, pools and prior transforms.

   Evidence: [NUTS fresh initialization](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py:290), [Nautilus archive preparation](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/nest/nautilus/search.py:673).
   **Change:** separate `resume_state` from `result_internal`; declare resumability honestly and define atomic writes, corruption handling, compatibility checks, finalization and retention precedence.

6. **[major] Removing the paths loader requires a broader compatibility bridge.**

   `Result` currently receives paths, samples and analysis—not an explicit search/checkpointer.
   `DatabasePaths.save/load_search_internal` are no-ops, while directory outputs support lazy loading and archives.
   A dill-only legacy fallback cannot replace the existing HDF detection.

   Evidence: [Result constructor](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/result.py:331), [database methods](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/paths/database.py:230), directory loader `:237`.
   **Change:** inject a narrow internal-result loader through paths or result construction, retaining format-aware legacy detection; cover directory, database, null, zipped and summary-only outputs.

7. **[major] FitContext needs an ownership and lifetime contract.**

   `copy_with_paths` performs a shallow copy; grid search then changes child paths and settings.
   EP mutates paths between factor steps and deliberately releases sampler-held compiled functions.
   Storing a context, checkpointer, RNG or objective cache on the search risks sharing it across children or retaining every EP executable.

   Evidence: [shallow copying](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:594), [grid children](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/grid/grid_search/__init__.py:329), EP release rationale `abstract_search.py:481`.
   **Change:** create context per fit invocation, keep it out of serialization/copies, guarantee cleanup on exceptions, and define snapshots passed to updates rather than unrestricted mutable internals.

8. **[major] RawSamples is useful, but automatic normalization is not behavior-preserving.**

   Existing chain and point samples commonly use weight `1`; weighted posterior searches use normalized weights.
   Normalizing every search changes serialized weights and interacts with the absolute `samples_weight_threshold`.
   A flat `(N,D)` array also cannot preserve chain identity, warmup, divergence diagnostics or multi-start lane histories by itself.

   Evidence: [weight filtering](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/samples/samples.py:514), [SMC weighted conversion](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/smc/search.py:740).
   **Change:** preserve existing representations first; specify weight semantics, parameter ordering, chain/lane metadata and diagnostic ownership before sharing conversion or thinning.

9. **[major] Objective semantics need more than callable shape.**

   `scalar`, `batched` and gradient variants describe execution, not the statistical target.
   BFGS/MultiStart minimize `−2 log posterior`; nested searches consume likelihood; SMC needs separate prior and likelihood terms.
   Invalid-value handling cannot safely be derived only from `fom_is_log_likelihood`: minimization direction and backend arithmetic matter.

   Evidence: [Fitness target/sign conversion](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/fitness.py:495), [NSS’s deliberate finite sentinel](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/nest/nss/search.py:42).
   **Change:** document target, coordinates, sign, normalization and rejection policy independently of execution kind; share pure numerical construction while retaining backend-specific invalid-value policies.

10. **[major] The proposed factory cannot directly supply NUTS’s promised gradient mode.**

    Current NUTS supplies a scalar log density to blackjax adaptation and kernels.
    Blackjax’s installed integrator builds its own `jax.value_and_grad`; substituting a factory returning `(value, gradient)` is not a compatible call.
    MultiStart’s transformed-coordinate objective additionally returns finite-gradient and constraint diagnostics.

    Evidence: [NUTS adaptation/kernel calls](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py:335), [MultiStart transformed objective](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:1125).
    **Change:** scope a separate blackjax gradient-injection investigation; retain an unjitted composable objective and a reusable batching helper instead of forcing every backend through four fully compiled return types.

11. **[major] “NONE still gets JIT” is a good default, not an unconditional lifecycle rule.**

    It fixes silent eager execution, but short runs may pay more compilation than they save.
    Completed fits should not compile merely to load results, and test modes 2/3 should retain their deliberate bypass.
    Stripping Fitness caches during pickle does not automatically strip externally retained bound compiled callables.

    Evidence: [completed-fit branch](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:689), [pickle handling](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/fitness.py:835).
    **Change:** use lazy JIT by default, retain an explicit execution/debug escape hatch, and verify sampler-held callable serialization; name the capability “backend requires JAX” rather than implying `NONE` means no JAX execution.

12. **[major] The multiprocessing rule must cover the whole execution topology.**

    Guarding the search’s `number_of_cores` misses outer grid/sensitivity workers and analysis-level parallelism.
    A child search can report one core while running inside a process forked after JAX initialization.
    Silently forcing one core also changes requested behavior and benchmark resource accounting.

    Evidence: [grid worker dispatch](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/grid/grid_search/__init__.py:266), its child-core override `:345`, and `analysis/multiprocessing.py`.
    **Change:** audit outer and inner pools together, enforce before device initialization/forking, prefer an explicit refusal over an unnoticed downgrade, and record effective worker/thread counts.

13. **[major] `eval_shape` is a trace check, not a likelihood-validity certificate.**

    It can catch tracing/type/shape failures, but cannot validate callback execution, finite likelihoods or numerical gradients.
    PyAutoArray’s Delaunay path declares callback output shapes and uses `stop_gradient`; that can trace successfully even when a particular host computation fails.
    The report’s prior-median probe is especially weak for ordered centres: all three medians coincide.

    Evidence: [Delaunay callback](/home/jammy/Code/PyAutoLabs/array/PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py:139); JAX documents [shape-only evaluation](https://docs.jax.dev/en/latest/_autosummary/jax.eval_shape.html) and [callback transformation limits](https://docs.jax.dev/en/latest/external-callbacks.html).
    **Change:** call it a trace preflight; apply it after analysis/model preparation, test the actual scalar/batched/gradient transform, and separately offer a synchronized numerical probe at a valid point.

14. **[major] Analysis backend propagation is underspecified beyond FactorGraphModel.**

    `ModelAnalysis` defaults independently to `use_jax=False` while forwarding likelihood evaluation to its wrapped analysis.
    Hierarchical factors also have their own backend flag, and graph flattening introduces generated factors.
    “All children equal or raise” may reject currently valid mixed EP configurations even though factors are optimized separately.

    Evidence: [ModelAnalysis](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/analysis/model_analysis.py:9), hierarchical factor `:81`, graph flattening `collection.py:146`.
    **Change:** distinguish whole-graph fitting from per-factor EP; define inherited versus explicit backend choices, mixed-child behavior, gradient-mode propagation and wrapper serialization.

15. **[major] The registry needs a dependency-light published representation.**

    One authoritative declaration is sensible; arbitrary live class imports are a poor cross-repository exchange format.
    Collecting all classes can defeat lazy loading, and Nerves importing Fit’s registry would invert the dependency direction.
    Facts such as `resumable`, gradient support and valid evidence can also depend on configuration.

    Evidence: [lazy exports](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/__init__.py:212), [SMC evidence/initializer constraint](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/smc/search.py:364).
    **Change:** generate a versioned JSON manifest from validated declarations; let Fit apply its own test budgets using Nerves’ generic mode API, and distinguish static capabilities from effective run capabilities.

16. **[major] Generated documentation needs release provenance and consumer ownership.**

    Workspace `main`, assistant guidance and installed PyAutoFit need not describe the same release.
    A library unit test cannot require sibling repositories to exist, and a generated roster can advertise an unreleased search.
    Current RTD does not mock optional dependencies; Heart’s fuller environment can conceal RTD-specific import failures.

    Evidence: [RTD installation](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/.readthedocs.yaml:8), [Heart docs dependencies](/home/jammy/Code/PyAutoLabs/organs/PyAutoHeart/.github/workflows/docs-build.yml:75).
    **Change:** version/pin the manifest and anchors, generate checked-in consumer blocks with provenance, validate each consumer against its declared version, and test both minimal RTD and full-extras docs environments.

17. **[minor] The claimed onboarding reduction contradicts retained manual exports.**

    A1 explicitly keeps `af` exports hand-written, yet A5 promises a new search with only its file and one registry entry.
    New dependencies, unit tests and integration coverage also remain real work.
    The “51 files” count includes conditional changes and a generated API stub, so it is an upper-bound inventory rather than measured mandatory effort.

    Evidence: report `:272`, `:582`, `:688`; survey 03 §3; [current exports](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/__init__.py:98).
    **Change:** either include export generation or correct the witness; measure required edits and working conformance, not file length or a grep count.

18. **[blocker] Ordered assertions leave the benchmark’s evidence convention unresolved.**

    Three exchangeable components yield six equivalent label permutations.
    Rejecting five regions through the likelihood gives evidence one-sixth of the unconstrained symmetric model unless the ordered prior is renormalized.
    Conversely, initializers that reject invalid draws condition their starting distribution on the assertions.

    Evidence: [assertion penalty](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/fitness.py:512), [initializer rejection](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/initializer.py:51), SMC prior normalization `search.py:821`.
    **Change:** specify the prior measure and evidence normalization explicitly; validate on a constant-likelihood constrained example. The potential `log(6)≈1.79` offset exceeds the proposed one-nat tolerance.

19. **[blocker] The optimizer success criterion targets the wrong objective.**

    The report calls LBFGS/MultiStart “MLE” and judges them solely against reference maximum likelihood.
    Their actual Fitness uses log posterior; the proposed LogUniform normalization priors contribute `−log(normalization)`.
    A correct MAP solution need not meet the same likelihood threshold as an MLE.

    Evidence: [BFGS Fitness](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mle/bfgs/search.py:225), MultiStart `:987`, [LogUniform density](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/mapper/prior/log_uniform.py:113).
    **Change:** benchmark MAP against a MAP reference, or explicitly configure a genuine likelihood-only optimization target; record both maximum likelihood and maximum posterior without treating them as interchangeable.

20. **[major] Reference agreement and marginal checks do not establish posterior correctness.**

    Two nested-sampling implementations can miss the same mode.
    Medians within one reference sigma and widths within a factor of two permit substantial error, including wrong correlations or mode occupancy.
    Such agreement also does not establish chain convergence, despite the proposed exporter setting `scientific.convergence`.

    Evidence: report `:370–375`; [Insight’s distinct verdict fields](/home/jammy/Code/PyAutoLabs/organs/PyAutoInsight/insight/summary.py:236).
    **Change:** separate accuracy acceptance from convergence diagnostics; add joint/predictive checks, mode coverage, appropriate chain diagnostics and reference Monte Carlo uncertainty. Freeze thresholds after a declared pilot, before scored runs.

21. **[major] Ten seeds support a pilot, not confident search recommendations.**

    Even 10/10 successes have a roughly 72% lower bound in a two-sided 95% Wilson interval.
    Reference scatter from three seeds per method is a weak basis for calibrating a ten-parameter acceptance rule.
    `mean wall / success rate` needs a restart interpretation, inclusion of failed attempts and an explicit zero-success outcome.

    Evidence: report `:370`, `:376`, `:381`; survey 04 itself records the earlier five-versus-200-seed calibration failure.
    **Change:** label wave 1 exploratory; preregister timeout/censoring rules and adaptive replication. Use Wilson intervals for proportions and a separate uncertainty method for wall-per-success.

22. **[major] Copied timing instrumentation would produce misleading comparisons.**

    MLTracker’s JAX fallback assigns evenly spaced times to retained history and targets each run’s own final maximum.
    That is neither actual evaluation count nor measured time to a common scientific target.
    The existing inference runner also performs its admission-bar compilation before starting the `search.fit` clock.

    Evidence: [MLTracker fallback](/home/jammy/Code/PyAutoLabs/fit/autofit_workspace_developer/searches_minimal/_metrics.py:61), [pre-fit timing](/home/jammy/Code/PyAutoLabs/lens/autolens_inference/scripts/misc/searches/_point_runner.py:535).
    **Change:** distinguish observed from estimated metrics; use a shared reference target, include warm-start provider cost, separate cold/warm cache runs, and report likelihood-share estimates as estimates rather than measured decomposition.

23. **[major] Track B’s claimed independence is false for scored wave 1.**

    B2 scaffolding can proceed early, but NSS with ordered assertions depends on its Fitness migration.
    Reproducible multi-seed comparisons need the seed work or an explicitly validated temporary harness.
    Comparisons made while A2/A3 change compilation and gradient behavior mix materially different implementations.

    Evidence: NSS `search.py:94`; report B2 `:616`, B3 `:625`, A4 `:550`.
    **Change:** allow early harness/pilot work, but freeze a scored-wave library/backend revision after required correctness and RNG changes; rebenchmark affected searches after semantic/performance migrations.

24. **[major] The phase sizes and parallelism claims need rewriting.**

    A0b depends on A0a; A0c includes executable integration scripts and Brain parser changes despite being called docs-only.
    A2/A3 both touch Fitness construction, all search implementations, pooling and NSS, so they are not independent seams.
    A5 delays the new-sampler hook until after broad lifecycle work, conflicting with the immediate need to develop against it.

    Evidence: report `:450`, `:463`, `:467`, `:518`, `:563`, `:584`.
    **Change:** expose a minimal `FitContext/run(ctx)` bridge early; split objective dispatch, gradient integration, sample adaptation, persistence, lifecycle extraction and consumer generation into separate deliverables.

25. **[major] Catalogue grouping and coverage do not yet support the maintainer’s goal.**

    Weighted/chain/point are output representations, not sufficient recommendation categories.
    Nested sampling and MCMC can legitimately be compared for posterior-only accuracy; evidence comparisons require evidence-capable configurations.
    Wave 1 omits SMC, BFGS, ADABelief and Lion, and initially excludes the Emcee/Zeus JAX behavior this epic specifically fixes.

    Evidence: report `:252`, `:381–386`, `:628`; the exported roster at `autofit/__init__.py:98`.
    **Change:** group by requested task—point/MAP, posterior, evidence—and record every registered search as measured, unsupported, deferred or failed. Add a cheap analytic control before broad assistant recommendations.

26. **[minor] Keep the two repos, but define the sharing boundary now.**

    The approved separate profiling repo has a real purpose: EP, aggregator, serialization, plotting and framework overhead exceed inference ranking.
    Co-location would reduce setup duplication, but would not remove the need for different measurement protocols and Insight/Pulse schemas.
    B4’s port can start after B1; its stated table depends on B2/B3 data if that is the chosen input.

    Evidence: [existing profiling task](/home/jammy/Code/PyAutoLabs/organs/PyAutoPulse/tasks/autofit_profiling_bootstrap.md:35), report `:644`.
    **Change:** retain both approved repos; share or pin the same model/dataset specification, use stable run IDs between outputs, and split B4 baseline port from the measured bottleneck campaign.

27. **[major] Several consequential policy choices were never made explicit.**

    Missing decisions include external subclass compatibility, the seed-identifier exception, exact-resume versus statistical-resume guarantees, and old-output support duration.
    Benchmark decisions also include MAP versus ML, timeout budgets, acceptable false-acceptance rates, cold versus warm cost, and funding repeat runs after releases.
    None is answered by the eight existing questions.

    Evidence: report invariants `:276`, benchmark protocol `:371`, and open questions `:698`.
    **Change:** record these as named decisions with proposed defaults before implementation; do not reopen the already-approved repo creation, SMC classification, deprecation, Dynesty example or in-flight hook rulings.

28. **[minor] R9–R11 are not identifiable rulings in the supplied report.**

    The report labels R1–R8 and R12, then claims R1–R12 are reflected throughout.
    There is no explicit text assigning R9, R10 or R11 to a decision.
    Reviewers should not invent the missing mapping.

    Evidence: report architecture headings `:242–362`, expected outcomes `:681`, resume note `:742`.
    **Change:** add a short ruling register with one stable statement and section pointer per ID.

**§4 Ruling-by-ruling assessment**

| Ruling | Assessment |
|---|---|
| **R1** — Insight/Pulse ownership and adopting the existing task | **Agree.** Correct organ split; creation is already authorized. |
| **R2** — One class-derived registry | **Amend.** Keep one authority, publish a versioned dependency-light manifest, and distinguish static from configuration-dependent capabilities. |
| **R3** — Family shims and invariants | **Amend.** Keep concrete paths/exports; inherited class-path persistence is not a reason to retain the family bases. |
| **R4** — Unified JAX contract | **Amend.** Lazy scalar JIT is sensible; preflight, process safety, gradient injection and legacy controls need separate contracts. |
| **R5** — RawSamples and Checkpointer | **Amend.** Separate conversion, archival loading and true interrupted-run resume; preserve weight and diagnostic semantics. |
| **R6** — Decomposition and `run(ctx)` | **Amend.** Introduce the bridge early and specify per-fit ownership; defer collaborators without demonstrated reuse. |
| **R7** — Generated documentation layers | **Amend.** Add version pinning, consumer-owned updates, RTD import checks and explicit `llms.txt` generation scope. |
| **R8** — Benchmark design | **Amend.** Resolve priors/evidence and MAP semantics, strengthen acceptance, and qualify timing and seed uncertainty. |
| **R9** | **Reject as unauditable.** No explicitly identifiable R9 statement exists. |
| **R10** | **Reject as unauditable.** No explicitly identifiable R10 statement exists. |
| **R11** | **Reject as unauditable.** No explicitly identifiable R11 statement exists. |
| **R12** — Expected outcomes | **Amend.** Replace line-count and two-edit promises with measured onboarding effort and explicit compatibility/coverage outcomes. |

**§5 Answers to open questions 2 and 6**

**Q2 — Use disjoint centre priors for the first scored baseline; retain ordering assertions as a separate stress benchmark.**

Label switching means permuting the three complete Gaussian components leaves the predicted curve unchanged.
An ordered-centre constraint chooses one labeling while preserving all unordered centre configurations.
Disjoint priors instead assign components to predefined regions and exclude some otherwise possible configurations; these are different statistical models.

For the first catalogue benchmark, disjoint centre intervals give an easily specified, normalized product prior and remove the unimplemented constrained-evidence convention.
They do not eliminate amplitude/width/background correlations or the overlap between the second and third components.
Choose and record the intervals before reference/scored runs, and verify posterior mass is not artificially pressed against their boundaries.

Then add an explicitly named ordered-centre challenge using broad shared priors.
That challenge should validate assertion behavior, rejected initialization, gradient behavior at boundaries and evidence normalization.
An eventual normalized ordered transform is attractive, but it needs consistent prior density, prior sampling and Jacobian handling—not merely sorting centre coordinates.

The report’s statement that “right answer” is ill-posed without ordering is too strong.
Component-labelled marginal comparisons become ambiguous, but predictive distributions, evidence and permutation-invariant diagnostics remain meaningful.
The immediate blocker is the undefined comparison convention, not mathematical impossibility.

**Q6 — Recommend deleting the three family bases after migrating their real behavior; retain concrete module paths.**

The inspected uses do not justify permanent compatibility layers:

- **Runtime dispatch:** I found no family-base `isinstance` consumers in the inspected libraries and named workspaces.
- **Exports:** they are not public `af.AbstractMCMC/AbstractNest/AbstractMLE` exports.
- **Persistence:** concrete class paths are stored; removing an intermediate superclass does not itself change them.
- **Documentation:** family concepts and directories can remain without corresponding Python base classes.
- **Downstream imports:** none appeared in the inspected PyAutoGalaxy, PyAutoLens, PyAutoCTI sources or named workspace/tutorial searches.

They nevertheless have behavior that must survive: initializer defaults, nested initializer rejection, autocorrelation settings, clipper defaults and plot configuration.
See [AbstractNest](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/nest/abstract_nest.py:20), [AbstractMCMC](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/abstract_mcmc.py:14) and [AbstractMLE](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mle/abstract_mle.py:14).

Move those defaults and policies deliberately before deleting the bases.
Constructor argument discovery walks `__bases__` when `**kwargs` exists, so compare serialized argument sets as well as hashes: [dictable.py:146](/home/jammy/Code/PyAutoLabs/organs/PyAutoNerves/autonerves/dictable.py:146).
Keep the genuinely useful shared backend bases, such as AbstractDynesty, unless separately shown redundant.

External subclass users remain an unknown, not evidence for indefinite shims.
If the maintainer explicitly promises compatibility for those internal import paths, use temporary behavior-preserving deprecated wrappers.
Do **not** alias all three names to `NonLinearSearch`: that would collapse distinct type identities and silently lose their former constructor behavior.

**§6 Top 5 changes before work starts**

1. **Rewrite A0 as an executable compatibility matrix.**  
   Separate metadata, serialization, actual backend execution and interrupted resume; cover full-extras and no-JAX CI, database/null/directory paths, and old outputs.  
   Start from the real [CI install contract](/home/jammy/Code/PyAutoLabs/organs/PyAutoHeart/.github/workflows/lib-tests.yml:114), not stale test comments.

2. **Put a minimal `run(ctx)` bridge near the beginning.**  
   Define per-fit ownership and preserve `_fit` compatibility; migrate one simple search and one native-checkpoint search before extracting the entire lifecycle.  
   Explicitly protect [shallow-copy behavior](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:594) and EP’s executable-release contract.

3. **Write the persistence and seed migration specification before implementation.**  
   Distinguish result archives from resume state, retain all legacy formats, and document the approved exception to identifier preservation.  
   Include the concrete [NUTS seed/default conflict](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mcmc/blackjax/nuts/search.py:37).

4. **Replace the current benchmark protocol with a pilot-plus-scored design.**  
   Fix prior normalization and MAP targets, separate accuracy from convergence, account for failures/provider cost, and distinguish measured timing from estimates.  
   Correct the assumptions exposed by [BFGS’s target](/home/jammy/Code/PyAutoLabs/fit/PyAutoFit/autofit/non_linear/search/mle/bfgs/search.py:225) and [MLTracker’s interpolation](/home/jammy/Code/PyAutoLabs/fit/autofit_workspace_developer/searches_minimal/_metrics.py:61).

5. **Specify the versioned registry exchange and corrected dependency graph.**  
   Keep Nerves independent of Fit, pin generated consumer facts, test RTD’s actual environment, and split B4/B5 into independently reviewable deliverables.  
   Preserve the approved two-repo split and DynestyStatic example; correct the report’s missing R9–R11 and incompatible “two touch points” witness.