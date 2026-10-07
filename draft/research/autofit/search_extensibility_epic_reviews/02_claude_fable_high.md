# Independent review — search extensibility epic report (Fable, high effort)

Reviewed 2026-10-07 against PyAutoFit `main` @ e807cc531 (the commit the surveys cite), read-only.
Report: `organs/PyAutoMind/draft/research/autofit/search_extensibility_epic_report.md`.
Paths below are relative to `fit/PyAutoFit/autofit/non_linear/` unless prefixed.

## §1 Verdict

The diagnosis is accurate (29 of 31 spot-checked claims hold exactly; the two misses are a path and a line
drift) and the architecture is the right shape: declared contract + composition inside the existing public
classes, one objective factory, one adapter, named checkpointers. Two things must change before work starts:
(1) the A1 fail-fast gate and the A3 preflight are placed "in `fit()` before `_fit`" without noticing that the
Heart smoke matrix runs every integration script with `PYAUTO_TEST_MODE=2` + `PYAUTO_DISABLE_JAX=1` (so the
gate must sit *after* the test-mode bypass return or every JAX-required smoke script goes red), and (2) the
registry must be lazy/declarative or it breaks the `_LAZY_ATTRS` import design and the Heart `unittest-nojax`
leg. The seed ruling (R4 / human §5.4) also collides with Nautilus and NSS already hashing `seed` by name,
which the golden table would catch but the plan does not anticipate.

## §2 Factual spot-checks

| # | Claim (report/survey) | File:line | Holds? |
|---|---|---|---|
| 1 | `abstract_search.py` is 1,691 lines; MultiStart `search.py` 2,258; only `@abstractmethod` is `_fit` | `search/abstract_search.py` (wc 1691; `:1376-1377`), `search/mle/multi_start_gradient/search.py` (2258) | yes |
| 2 | `af` exports at `autofit/__init__.py:98-113`; NSS/SMC lazy via `_LAZY_ATTRS` `:211-215` | `fit/PyAutoFit/autofit/__init__.py:98-113`, `:211-213` | yes |
| 3 | emcee "nasty hack" in paths | `paths/directory.py:238-246` | yes (verbatim comment at :238) |
| 4 | `search.json` written from `to_dict(self.search)` | `paths/directory.py:385` | yes |
| 5 | `conf.instance["output"]["search_internal"] = True` set in Emcee/NUTS/SMC constructors | `search/mcmc/emcee/search.py:108`, `mcmc/blackjax/nuts/search.py:235`, `mcmc/blackjax/smc/search.py:286` | yes, all three |
| 6 | `samples_from` swallows `AttributeError` | `search/abstract_search.py:1622` | yes |
| 7 | `make_sneakier_pool` dead at `:1672` | `search/abstract_search.py:1672`; no callers anywhere in PyAutoFit | yes |
| 8 | Drawer reads `self.timer.time` unguarded, ignores `search_internal` arg | `search/mle/drawer/search.py:147`, `:158-159` | yes |
| 9 | Nautilus mutates `iterations_per_full_update` in `call_search` | `search/nest/nautilus/search.py:584-586` | yes |
| 10 | Nautilus strip-then-dill at `:673` | actual `:686-697` | **line drift** (claim true, line off by ~13) |
| 11 | Dynesty `raise RuntimeError` as control flow at `dynesty/abstract.py:249-251` | actual `search/nest/dynesty/search/abstract.py:249-250` | **path wrong** (`dynesty/search/abstract.py`), claim true |
| 12 | `AbstractNest(number_of_cores=None)` vs `> 1` check | `search/nest/abstract_nest.py:28`, `abstract_search.py:271` | yes |
| 13 | Zeus computes `discard/thin/chain` unused; has empty-chain fallback | `mcmc/zeus/search.py:283-290`, `:358-377` | yes |
| 14 | `Fitness` dispatch chosen once; `_grad` has no callers | `fitness.py:281-286`, `:926-947`; `grep "fitness.grad\|\.grad("` over autofit/autolens/autogalaxy finds none | yes |
| 15 | `Analysis(use_jax=False)` default; lens dataset analyses default True | `analysis/analysis.py:90`, `lens/PyAutoLens/autolens/analysis/analysis/dataset.py:50` | yes |
| 16 | `AnalysisFactor` has no `_use_jax`; `FactorGraphModel` False | probe reproduced: `child True factor MISSING graph False`; MRO `AnalysisFactor→AbstractModelFactor→FactorKW→Factor…` never reaches `AbstractDeclarativeFactor.__init__` (`graphical/declarative/abstract.py:25-28`) | yes |
| 17 | Test modes ≥2 skip `_fit` | `search/abstract_search.py:839-844` | yes |
| 18 | `samples_info["class_path"]` re-instantiated by aggregator | `aggregator/search_output.py:369`; also `paths/directory.py:281`, `samples/efficient.py:44` | yes |
| 19 | Identifier hashes class `__name__` + `__identifier_fields__` | `mapper/identifier.py:136-141` | yes |
| 20 | Workspace says "use_jax=False is required by LBFGS" | `fit/autofit_workspace/scripts/searches/mle.py:84` | yes |
| 21 | NUTS hand-pickle at `nuts/search.py:509-527` | `:511-527` | yes |
| 22 | `_log_process_state` duplicated in updater | `search/updater.py:339-358` vs `abstract_search.py:716` | yes |
| 23 | SMC accepts meaningless `auto_correlation_settings` | `mcmc/blackjax/smc/search.py:78` | yes |
| 24 | 77 commits to `search/` since 2026-06-01, 26 to `abstract_search.py` | `git log --since=2026-06-01` → 77 / 26 | yes, exact |
| 25 | No `isinstance(…Abstract{Nest,MCMC,MLE})` anywhere | grep over fit/, lens/, galaxy/, cti/, organs/ → zero | yes |
| 26 | `CONFIG_NAME_RE` at `_inference_cli.py:47`; exporter hard-codes `not_assessed` at `:152` | `lens/autolens_inference/_inference_cli.py:47-49`; `scripts/misc/tooling/export_inference_summary.py:152-153` | yes (exporter path is `scripts/misc/tooling/`, report omits it) |
| 27 | Insight accepts producer-asserted convergence/acceptance | `organs/PyAutoInsight/insight/summary.py:239-243` (validates enum only) | yes |
| 28 | Brain profiling conductor hard-wired to autolens_profiling | `organs/PyAutoBrain/agents/conductors/profiling/_profiling.py:107` | yes |
| 29 | Pulse label hack | `organs/PyAutoPulse/pulse/setup_browser.py:43` | yes |
| 30 | `_point_runner.py:543-544` passes `use_jax_vmap=True` | `lens/autolens_inference/scripts/misc/searches/_point_runner.py:543` | yes |
| 31 | Eager JAX in Emcee is ~27× slower than jitted | measured here on 3-Gaussian toy: eager 5.1 ms, jit 0.096 ms (≈53×), numpy 0.32 ms | yes (direction and magnitude) |
| 32 | Pulse task `autofit_profiling_bootstrap` is `needs-decision` | `organs/PyAutoPulse/campaigns.yaml:74-80`, `:191-199` | yes |
| 33 | HowToFit `gaussian_x3` co-centred | `fit/HowToFit/scripts/simulators/simulators.py:39-101` (all `centre=50.0`) | yes |

## §3 Findings

**F1 (blocker) — The fail-fast gate/preflight placement collides with the Heart smoke matrix.**
`fit/autofit_workspace_test/config/build/profile_smoke.yaml:12-13` sets `PYAUTO_TEST_MODE: "2"` and
`PYAUTO_DISABLE_JAX: "1"` as defaults for *every* script; `analysis/analysis.py:94-95` turns `use_jax=True`
into False under that env var. Today NSS/NUTS/SMC/MultiStart integration scripts pass because `fit()` returns
from `_fit_bypass_test_mode` at `abstract_search.py:841-844` *before* the per-search JAX check (NUTS's is
inside `_fit`, `nuts/search.py:267`). A1's "REQUIRED search + numpy analysis raises `SearchException` in
`fit()` before `_fit`" and A3's `eval_shape` preflight, if placed before the bypass, turn every JAX-required
smoke script red in the next nightly. Change: specify the gate as *after* the test-mode bypass return (or `if
test_mode_level() >= 2: skip gate`), add a unit test "REQUIRED search + `PYAUTO_DISABLE_JAX=1` +
`PYAUTO_TEST_MODE=2` completes", and name `PYAUTO_DISABLE_JAX` in §1.2 — the report says "the only switch is
`Analysis(use_jax=...)`; no config key exists", which misses this documented harness override
(`organs/PyAutoNerves/autonerves/test_mode.py:256-271`).

**F2 (blocker) — The registry as described would import every search module eagerly.**
`_LAZY_ATTRS` exists because NSS/SMC pull blackjax→jax (>1 s, `autofit/__init__.py:207-213`), and the Heart
`unittest-nojax` leg (`organs/PyAutoHeart/.github/workflows/lib-tests.yml:520-600`) strips jax/blackjax/optax
and asserts every module still imports. A `registry.py` that "collects class attributes" by importing the 15
classes breaks both. Change: make the registry declarative (entries are `(class_path, lazy: bool, …)` strings
with attributes mirrored from the class; a test — run only where the optional dep is importable — asserts
registry entry == class attributes), and make the docs generator run in the `[optional]` env. Note survey 01
§9's own `SEARCH_REGISTRY  name → (module, class, lazy, docs section)` already had the `lazy` bit; the report
dropped it in §3.1.

**F3 (major) — The seed ruling (R4 / human §5.4) is under-specified against today's identifiers.**
Nautilus and NSS already carry `"seed"` in `__identifier_fields__` (`nest/nautilus/search.py:166`,
`nest/nss/search.py:200`), and the identifier adds the *field name* even when the value is None: the frozen
golden for `af.Nautilus()` is `[..., "n_like_new_bound", "seed", "n_shell", ...]`
(`test_autofit/database/identifier/test_identifiers.py:423-440`). So (a) a search-level `seed` added to the
base `__identifier_fields__` would add `"seed"` to the hash of the other 13 searches even when None (forks
every output path — exactly what the ruling forbids), and (b) Nautilus/NSS must keep their static `"seed"`
entry to hold the golden. Change: implement "only when not None" in the identifier walk (skip a field whose
value is None *only* for the new base-level seed) or via an instance-level `__identifier_fields__` property
that appends `"seed"` conditionally and dedupes against Nautilus/NSS; add the golden-table assertion that
`Nautilus().hash_list` is byte-identical post-A4. Also note Nautilus's existing `seed` kwarg must become an
alias of the new base seed, not a second knob.

**F4 (major) — Family bases: the report's "no isinstance anywhere" is true but the clipper tripwire makes
AbstractMLE load-bearing for identifiers.**
`test_identifiers.py:486-494` (`test_nested_samplers_have_no_clipper`) pins PyAutoFit#1493: `clipper` must
live on `AbstractMLE`, never on `NonLinearSearch`, or nested-sampler identifiers re-key. BFGS/MultiStart put
`"clipper"` in `__identifier_fields__` (`mle/bfgs/search.py:34`, `multi_start_gradient/search.py:46`).
Deleting the bases is fine only if `clipper`/`initializer` defaults move to a *per-posterior-kind defaults
object* that is applied by concrete class, never by the shared base — the report's R3 "capability objects"
must say this explicitly. See §5 Q6 for the recommendation.

**F5 (major) — Three external subclasses of the family bases exist and are not in the invariant list.**
`fit/autofit_workspace_developer/searches/{nss,ultranest}/search.py` subclass `abstract_nest.AbstractNest`
(`:125`, `:14`), `pyswarms/abstract.py:48` subclasses `AbstractMLE`, and Brain
`skills/sampler_pipeline/reference.md:128-129` tells new-sampler authors to subclass the family abstract.
Deleting the bases without aliases breaks the archive tier the Brain samplers faculty scans
(`agents/faculties/samplers/_samplers.py:15-20`). Whatever §5 Q6 decides, A4/A5 must keep importable names at
the three module paths for one release and update `reference.md` in the same PR.

**F6 (major) — "Hand-edited files per new search ~51 → ~5" double-counts what generation can reach.**
Survey 03 §3 says ~16 of 51 are roster lists. The remaining ~35 are prose (cookbook section, HowToFit
mentions, al/ag guides, CITATIONS text). Generation removes the 16; "collapse al/ag
`guides/modeling/searches.py` onto domain advice" removes maybe 4 more; the rest are either legitimately
per-search prose or policy ("teaching stays family-level"). The honest after-number is ~10–12, not 5. Restate
R12's table and the Witness; otherwise the first new sampler will "fail" the epic's own metric.

**F7 (major) — A2 and A3 are not as parallel as claimed.**
A3's "NSS moves onto `Fitness` via the factory once A2 has landed or `fitness.call` before then" and A3's
`Result.search_internal` via checkpointer both touch `Fitness` construction sites that A2 is rewriting to
`make_fitness`/`objective(kind)`. Run them in parallel worktrees and the rebase conflicts land on the 11
`Fitness(...)` sites. Change: A3 is "adapter + checkpointer only" (no Fitness touch); the NSS-onto-Fitness
move, preflight, fork rule and x64 check become A3b after A2 merges. Sizing is then honest: A2 ≈ 1 PR, A3 ≈ 1
PR + goldens, A3b ≈ 1 PR.

**F8 (minor) — A0a cannot be "green with three xfails" as specified under `importorskip`.**
Zeus, Nautilus, blackjax (NUTS/SMC/NSS) are `[optional]` (`pyproject.toml:81-88`); the main CI legs install
`[optional]` (`lib-tests.yml:76-77,114-119`) so the suite runs there, but the no-jax leg skips 6 of 15
searches. Fine — but the Witness must say "green on the `[optional]` legs; NSS/NUTS/SMC/MultiStart skipped on
`unittest-nojax`", and the conformance test module must not import `af.NSS`/`af.SMC` at collection time (use
`pytest.param(lazy_import(...), marks=importorskip)`).

**F9 (minor) — `jax.eval_shape` preflight: sound and effectively free, but the report under-sells one failure
class and over-claims another.**
Measured: fresh `Fitness`, `eval_shape` 0.046 s then first call 0.158 s vs first call alone 0.212 s — jit
reuses the trace, so the preflight adds ~0. On PyAutoLens: `pure_callback` sites
(`array/PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py:161`, `vmap_method="sequential"`) and
custom primitives (`autoarray/util/jax_nnls.py`, `jax_active_set.py`,
`autolens/point/solver/implicit_diff.py`) trace fine under `eval_shape` because tracing is what jit does
anyway. What it does *not* catch: `-inf`/NaN at runtime, the `np.asarray(tracer)` the report cites as a test
*is* caught (TracerArrayConversionError), but a numpy analysis with `use_jax=True` that only fails on a
concrete-value `if` is caught too. The miss: `eval_shape` of `objective("batched")` requires the padded batch
shape, so the preflight must run per *kind* the search declares, not just scalar. Also the report says "raise
a message naming the tracer error" — keep the original traceback chained (`raise … from e`), the
traced-assertion contract in `fitness.py:370-445` is subtle enough that users will need it.

**F10 (minor) — "NONE searches still get the jitted scalar": hidden costs are small but one is real.**
Compile is 0.16–0.2 s on the toy (negligible); `Fitness.__getstate__` already strips `_call/_jit/_vmap/_grad`
(`fitness.py:835-842`) so pickling is fine; forking after jit (Emcee `make_sneaky_pool` `emcee/search.py:149`,
`parallel/context.py` pins "fork") is the real cost — the child inherits XLA state and every worker recompiles
(survey 02 §3.6/3.7). The plan's "one fork rule" is in A3, but the jit-by-default lands in A2: for one phase
Emcee+JAX+`number_of_cores>1` gets *worse* (N recompiles) before it gets refused. Change: ship the fork rule
in A2 with the factory, or have A2 keep eager when `number_of_cores > 1` and log.

**F11 (minor) — Grid search and EP are only half in the plan.**
`grid/grid_search/__init__.py:330` uses `search.copy_with_paths` which is a shallow `copy.copy`
(`abstract_search.py:594-600`); a `FitContext` must therefore be per-call and never cached on `self`
(Nautilus's `self.iterations_per_full_update` mutation at `:584` is the existing counter-example, fixed in A0b
— good). EP: `NonLinearSearch(AbstractFactorOptimiser)` (`abstract_search.py:138`) — moving `optimise` to
`graphical/` must keep that base class on `NonLinearSearch` or `af.Emcee()` stops being accepted by
`EPOptimiser`. Neither constraint is written down; add both to §3.2 invariants. Also absent: `Result` classes
are *not* per-search (`result.py:330`, one `Result`), so the brief's "managing results with Samples after a
search runs" is really the Samples adapter — say so, the report's §2 Ask 2 narrowing is correct but should
cite this.

**F12 (minor) — Benchmark protocol details.**
(a) Criterion (b) `σ_run/σ_ref ∈ [0.5, 2]` at 10 seeds cannot distinguish a search that under-reports σ by
1.8× from one that is right; the ratio band should be calibrated from the reference runs' own scatter (the
report says this, but then fixes the band — pick one). (c) "Expected wall per right answer = mean wall /
success rate" with 10 seeds has a Wilson interval on the denominator of roughly [0.55, 1.0] at 9/10 — fine for
a *catalogue* but useless for ranking; the report should say wave 1 ranks nothing, wave 2 (50 seeds) ranks.
(d) The 3-Gaussian with σ 3/6/10 at centres 25/45/60: components 2 and 3 at 45±6 and 60±10 overlap heavily;
with LogUniform normalization priors the blend has a real degenerate ridge (g1 absorbs g2). Good as a hard
test, but the `gaussian_x3_separated` control should be wave 1 not wave 2 — otherwise a 60% success rate
cannot be attributed to the search vs the problem. (e) Reference posterior "Nautilus n_live=2000 and
DynestyStatic nlive=1000 agree on log Z within 0.2 nat": with ordered-centre assertions implemented as a JAX
`where` penalty (`fitness.py:441-445`) vs numpy's raise→resample, the two paths see *different* prior volumes
unless the penalty returns exactly `-inf`-equivalent; the reference runs must be done on the same backend as
the benchmarked run or the logZ criterion is biased by the sentinel (`-1e99` vs `-inf`, survey 02 I7).

**F13 (minor) — autofit_profiling as a separate repo is right, for one reason the report does not give.**
Pulse's `repo` field must be a Mind `repos.yaml` key and a producer ships its own Pages + `pulse-refresh`
dispatch; a folder inside autofit_inference would make one repo two instances across two organs with one Pages
site. Separate repos it is — but B4 should be *descoped*: port only the Nautilus `search_fit_breakdown.py` +
exporter first (epic 1), and leave the EP/graphical baseline port (the Pulse task's Deliverable 1) as B4b,
because reproducing the committed EP baselines "within tolerance" on a different machine is its own research
task (the Pulse task was filed with a release-sweep host pin for exactly this reason).

**F14 (minor) — Documentation generation across repos with separate release cadences.**
Generated roster blocks in al/ag assistants and the Hands navigator read the *installed* autofit registry. An
al assistant regenerated against autofit `main` will list a search the released autofit does not have until
the next release (memory `F=released`: Colab/RTD audit the released stack). Change: generators pin to the
installed `autofit.__version__` and emit it in the `<!-- generated: search-roster @autofit X.Y -->` fence; the
workspace CI check compares against the pinned version, not `main`. RTD: `.readthedocs.yaml` installs only
`[docs]`, `conf.py` has no `autodoc_mock_imports`; the generated `searches.rst` will autosummary
`Nautilus`/`Zeus`/`NSS`/`SMC` whose modules import optional deps — today's page already lists Zeus/SMC/NUTS,
so verify how those render on RTD (likely the lazy imports save them); add `autodoc_mock_imports =
["nautilus", "zeus", "blackjax"]` to A1's RTD scope defensively. `llms.txt`: Hands' navigator writes
`llms-full.txt` and explicitly *never* writes the curated `llms.txt`
(`organs/PyAutoHands/autohands/navigator.py:18-21`); the report's "llms.txt roster lines via the Hands
navigator" needs either a new navigator mode or a fenced block in the curated file — say which.

**F15 (minor) — Numbering and adoption gaps.**
Rulings jump R8 → R12 (R9–R11 never defined). §1.4 cites `export_inference_summary.py` and `_point_runner.py`
without their `scripts/misc/{tooling,searches}/` paths. Candidate task "root `AGENTS.md` omits PyAutoInsight"
is correct (the routing table above has no Insight row) and should be filed now, since B1's registration path
depends on an agent finding Insight.

## §4 Ruling-by-ruling

| Ruling | Verdict | One line |
|---|---|---|
| R1a autofit_inference → Insight | agree | `inference-summary@1` rows are verdicts; Insight validates producer-asserted `scientific.*` (`summary.py:239`); Pulse axes are timings only (`pulse/summary.py:40-45`). |
| R1b adopt the Pulse task as B4 | agree, amend | Adopt, but split B4 into epic-1 breakdown (now) and EP-baseline port (B4b); see F13. |
| R2 one registry from class attributes | agree, amend | Must be declarative/lazy (F2); keep survey 01's `lazy` bit; exports stay hand-written is right. |
| R3 bases as shims | amend | Human leans delete; see §5 Q6 — delete-with-aliases, with clipper/initializer defaults moved to concrete classes, respecting the #1493 tripwire (F4, F5). |
| R4 NONE searches get jitted scalar; gate in `fit()` | agree, amend | Place gate after the test-mode bypass (F1); ship the fork rule with the factory (F10); preflight per declared kind (F9). |
| R5 RawSamples + three Checkpointers | agree | Correct; `retain_after_completion` deletes the three config mutations cleanly. Add the backend-sentinel unification (`-1e99` vs `-inf`) to the adapter's remit. |
| R6 FitContext + run(ctx) | agree, amend | Per-call ctx only (shallow `copy_with_paths`, F11); keep `AbstractFactorOptimiser` on `NonLinearSearch`. |
| R7 documentation layers | agree, amend | Pin generated blocks to the installed autofit version (F14); correct the ~5 files claim (F6). |
| R8 gaussian_x3_blend protocol | agree, amend | Separated control into wave 1; reference posterior on the same backend as the benchmarked leg; wave 1 ranks nothing (F12). |
| R9–R11 | reject as written | Not defined in the report; renumber or state them. |
| R12 outcome table | amend | ~51→~10–12 hand-edited files, not 5; `abstract_search.py` 400–600 is plausible given 380 lines of test-mode bypass + 187 EP lines leave. |
| Human §5.7 keep DynestyStatic in RTD | agree | Consequence: A0c item (1–2) still adds the Nautilus cookbook section; only the "generic example" stays Dynesty. |
| Human §5.8 in-flight samplers on `run(ctx)` branch | agree | Consequence: the `run(ctx)` signature must be frozen in A1's design note, not A5, or those branches rot for three phases. |

## §5 Open questions 2 and 6

**Q2 — label switching.** Recommend **ordered-centre assertions as the model definition, plus post-hoc
permutation-invariant scoring as the comparison rule** — i.e. both, with distinct roles.

Reasoning. (i) Disjoint priors change the *problem*: three narrow centre priors make the posterior
near-Gaussian and the benchmark stops measuring what a user runs (`_point_runner.py` docstring's
"library-default priors" principle, which the report adopts). (ii) Assertions alone are not backend-neutral:
on numpy an assertion violation raises and the sampler resamples (prior volume excluded); on JAX it is an
`xp.where` penalty to the final figure of merit (`fitness.py:370-445`) with a `-1e99`/`-inf` sentinel that
differs per search (survey 02 I7). Nested samplers see a different effective prior volume on the two paths, so
the log Z criterion (c) is biased between numpy and JAX legs *by the assertion mechanism itself*, and the
reference posterior must be computed per backend. (iii) The third option — run with exchangeable priors and
relabel each posterior sample by sorting centres before comparing medians/σ (and compare log Z after adding
`ln 3! = 1.79` nat for the 3! modes) — is backend-neutral and keeps the real failure mode (multi-modality)
that the report wants to keep, but it changes what MLE searches are judged on (max-logL is already
permutation-invariant, so (a) is unaffected) and it conflates "found one mode well" with "found all six" for
MCMC chains, which is actually the interesting diagnostic. Protocol therefore: model uses assertions (what
users run); the exporter *also* records sorted-centre relabelled statistics and a `modes_found` count from the
chain; the reference posterior is computed on the same backend as each leg; the `separated` control is in wave
1 so the assertion-induced ridge can be separated from search failure. Pre-register all of that in
`protocol_gaussian_x3.md`.

**Q6 — family bases.** Recommend **delete-with-aliases**, not keep-as-shim and not bare delete.

Evidence: zero `isinstance/issubclass` uses across fit/, lens/, galaxy/, cti/, organs/; not exported from `af`
(`autofit/__init__.py` has no `AbstractNest/MCMC/MLE`); not in `docs/api`; the bases are 60–80 lines each
(`abstract_nest.py` 80, `abstract_mcmc.py` 60, `abstract_mle.py` 64) whose only content is default
`initializer`/`clipper`/`auto_correlation_settings` and a `plot_results` keyed on config `should_plot`.
Concrete class paths in `search.json` and the identifier's `__class__.__name__` are unaffected by removing an
intermediate base. So "shim" buys nothing — the report's own §1.1 says the split "carries little weight", then
R3 keeps it anyway for "the documented mental model", which is a *docs* concept
(`searches/{mcmc,nest,mle}.py`, HowToFit t3/6/7) that the registry's `posterior_kind` preserves without a
class. But bare deletion breaks three things: (1) the #1493 clipper tripwire (`test_identifiers.py:486-494`) —
`clipper` must land on each MLE concrete class (or a `PointDefaults` applied by the concrete class), never on
`NonLinearSearch`; (2) the three developer-tier subclasses and the Brain
`sampler_pipeline/reference.md:128-129` instruction (F5); (3) `AbstractMCMC` carries
`auto_correlation_settings` that SMC must *lose* when it becomes `weighted` — a good forcing function.
Therefore: in A4, delete the three classes, leave `abstract_{nest,mcmc,mle}.py` modules exporting
`AbstractNest = NonLinearSearch`-style deprecated aliases that emit a `DeprecationWarning` on subclass (via
`__init_subclass__`), move defaults into per-`posterior_kind` default objects applied in each concrete
`__init__`, keep the clipper tripwire test, and update `reference.md` + the three developer searches in the
same PR set. Remove the aliases one release later.

## §6 Top 5 changes before work starts

1. **Rewrite A1/A3 gate placement**: gate and preflight run *after* the `test_mode_level() >= 2` bypass return
(`abstract_search.py:841`), and name `PYAUTO_DISABLE_JAX` as the second JAX switch; add the smoke-profile
regression test (F1).
2. **Make the registry declarative and lazy** (`class_path`, `lazy`, attributes mirrored), with the
attribute-equality test skipped where the optional dep is absent; generators run in the `[optional]` env (F2,
F8).
3. **Specify the seed-in-identifier mechanism** against the Nautilus/NSS goldens before A4: conditional field
in the identifier walk, Nautilus `seed` becomes an alias of the base seed, golden table asserts byte-identity
(F3).
4. **Decide Q6 as delete-with-aliases** and write the clipper/initializer default relocation +
`__init_subclass__` deprecation + `reference.md` update into A4's scope; add the three developer-tier
subclasses and `AbstractFactorOptimiser` base to the §3.2 invariants (F4, F5, F11).
5. **Re-sequence A2/A3** (A3 = adapter + checkpointer only; A3b = NSS-onto-Fitness, preflight, fork rule, x64
after A2), ship the fork rule with the factory, and fix R12's ~5-files claim to ~10–12; move the
`gaussian_x3_separated` control into wave 1 and compute reference posteriors per backend (F7, F10, F6, F12).
