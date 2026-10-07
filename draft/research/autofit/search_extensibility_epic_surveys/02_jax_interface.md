# 02 — JAX interface across PyAutoFit non-linear searches (read-only audit)

Repo: `fit/PyAutoFit` @ `main` (e807cc531). Paths below are relative to `fit/PyAutoFit/` unless
prefixed. Auditor ran four small probes (scratchpad `jaxprobe.py`, `fgprobe.py`); no file in any repo
was edited. Line numbers are as of that commit.

**One-line verdict.** No search declares how it relates to JAX. The only switch is one boolean on the
*Analysis* (`Analysis(use_jax=...)`). Each of the 15 concrete searches reads that switch in its own
way: four different attribute probes, three different per-search knobs, and four different ways of
building the compiled callable. As a result, a JAX analysis handed to five of the searches runs as
**eager, un-jitted `jax.numpy`** with no warning (measured 27x slower than jit on the toy Gaussian).
Two searches crash deep inside a trace instead of failing fast. And the one generic gradient builder,
`Fitness.grad`, is dead code.

---

## 1. Mechanism map — every door JAX comes through

### 1.1 The switch: `Analysis(use_jax=...)` (not config, not search)
- `autofit/non_linear/analysis/analysis.py:88-118`. `__init__(use_jax=False)` sets `self._use_jax`.
  `PYAUTO_DISABLE_JAX=1` forces False (`:94-95`). If JAX is missing, it warns and falls back to numpy (`:97-116`).
- `_xp` property (`analysis.py:155-159`) returns `jax.numpy` or `numpy`. Everything downstream branches
  on either `_use_jax` or `_xp.__name__.startswith("jax")`. These are two probes for one fact (§3.1).
- There is **no `use_jax` key in `autofit/config/`** (grep of all yaml: zero hits). The brief guessed
  `general.yaml` would hold one. It doesn't.
- **The defaults disagree across the stack.** `af.Analysis` defaults to `use_jax=False` (`analysis.py:90`),
  `af.ex.Analysis` likewise (`autofit/example/analysis.py:71`). But every PyAutoGalaxy/PyAutoLens dataset
  analysis defaults to **True**: `galaxy/PyAutoGalaxy/autogalaxy/analysis/analysis/analysis.py:36`,
  `.../imaging/model/analysis.py:48`, `.../interferometer/model/analysis.py:187`,
  `.../ellipse/model/analysis.py:46`, `lens/PyAutoLens/autolens/analysis/analysis/dataset.py:50`,
  `.../imaging/model/analysis.py:53`, `.../interferometer/model/analysis.py:54`,
  `.../point/model/analysis.py:66`. `AnalysisWeak` is the exception at False
  (`lens/PyAutoLens/autolens/weak/model/analysis.py:37`).
- `FactorGraphModel` and `HierarchicalFactor` each have **their own** `use_jax=False`
  (`autofit/graphical/declarative/collection.py:22`, `abstract.py:25`, `factor/hierarchical.py:29`).
  `AnalysisFactor` never runs `Analysis.__init__`, so it has **no `_use_jax` attribute at all**.
  Probe result: `child True factor MISSING graph False numpy`. A graph of JAX analyses fitted as one
  model therefore reports `_xp = numpy` unless the user passes the flag a second time.

### 1.2 `autonerves.jax_wrapper` is environment setup, not a numpy/jax switch
`organs/PyAutoNerves/autonerves/jax_wrapper.py` (re-exported at `autofit/__init__.py:1,187`) does five things:
- warns if JAX is absent (`:8-21`);
- appends XLA flags: `constant_folding` off (`:23-56`), GPU autotune 0 and Triton GEMM off (`:58-85`);
- forces `JAX_ENABLE_X64=True` (`:87-105`);
- sets the persistent compile cache dir (`:107-131`);
- provides lazy `register_pytree_node[_class]` helpers (`:135-163`).

All of these env vars only bite if they are set **before the first `import jax`**. Nothing later
checks `jax.config.jax_enable_x64` (see §3.5).
(Side finding: `organs/PyAutoNerves/build/lib/` holds a recursively nested `build/lib/build/lib/...`
tree more than 20 levels deep. That is packaging debris for the hygiene skill.)

### 1.3 `Fitness` (`autofit/non_linear/fitness.py`) — the shared wrapper
- Constructor knobs: `use_jax_vmap`, `use_jax_jit`, `batch_size`, `gradient_mode` (`:180-186`). They are
  **passed per call by each search**. `Fitness` never derives them from the analysis.
- Pytrees: if `analysis._use_jax`, it calls `enable_pytrees()` + `register_model(model)` (`:275-279`).
  This happens implicitly, so the docs' instruction to "call enable_pytrees()/register_model" is redundant (§6).
- Dispatch is picked once (`:281-286`): `_call = call`, else `_vmap` if vmap, else `_jit` if jit.
  **With `use_jax=True` and neither flag set, `_call` is plain `call`, i.e. eager `jnp`** (§3.2).
- `call` (`:365-519`) branches on `self._is_jax`, which is `_xp.__name__` (`:356-363`):
  - JAX branch: `instance_from_vector(..., ignore_assertions=True, xp=jnp)`, then assertions applied
    as a traced `xp.where` on the final figure of merit (`:430-446, :512-517`);
  - numpy branch: try/except `FitException` (`:448-454`);
  - NaN/inf/ceiling guards apply to the **value only, never the gradient** (`:456-492`, docstring `:385-412`);
  - the ceiling-fired warning is numpy-only (`:483-492`).
- `call_wrap` (`:566-613`) is the Python-side wrapper for history and quick updates. With vmap it adds a
  batch axis (`:593-595`); with jit it calls `float()` (`:599-600`). **Every search that passes
  `fitness._jit` / `fitness.call` straight to a sampler bypasses it** (BFGS-JAX, NUTS, SMC, NSS, MSG).
- `_vmap = jax.jit(jax.vmap(self.call))` as a cached_property (`:866-903`). It recompiles for each
  distinct batch *length* (`:890-893`).
- `_jit = jax.jit(self.call)` (`:906-923`).
- `_grad` / `grad` = `gradient.grad_from(self.call, mode)`, **not jitted** (`:926-947`).
  **No library caller exists**: grep finds no `fitness.grad` / `._grad` user anywhere in `autofit/`.
- `__call__` is decorated `@timeout(timeout_seconds)` (`:785-805`) and routes through `call_wrap`.
- Pickling: `__getstate__` strips `_call/_jit/_vmap/_grad` (`:835-841`). `__setstate__` re-selects
  `_call` from the stored flags (`:843-863`). Jitted callables are rebuilt lazily after a resume or fork.
- Resume sanity check: `check_log_likelihood` runs **inside `__init__` whenever `paths` is set**
  (`:319-320, :949-1046`). On a resumed JAX run, the first compile therefore happens at Fitness construction.
- Visualization warm-up: if `iterations_per_quick_update` is set and the backend is JAX, it eagerly
  runs `fit_for_visualization` at construction (`:322-349`).

### 1.4 `jax_compile.py` — compile logging only
`log_on_first_compile(func, description)` (`autofit/non_linear/jax_compile.py:252-366`) wraps an
already-transformed callable. On its first call it logs the compile and materialize halves
separately, runs a heartbeat, and arms a faulthandler watchdog. It compiles nothing itself.
Callers: `Fitness._vmap/_jit/_grad` (`fitness.py:900,920,941`) and
`analysis/latent.py:168,173`. **These search-built jits do not use it:**
- NUTS `log_density` (`nuts/search.py:314`);
- SMC `vmapped_log_likelihood` (`smc/search.py:509`);
- NSS `one_step` (`nss/search.py:456`);
- MSG `_vmapped` (`multi_start_gradient/search.py:1145`), which has its own `_compile_message` (`:724`).

Compile visibility therefore depends on which search you run.

### 1.5 Pytrees / model registration (`autofit/jax/pytrees.py`)
- `enable_pytrees()` (`:39-77`) registers the priors, `Model`, `Collection` and `ModelInstance`.
- `register_model(model)` (`:80-139`) walks the tree, registers each user `cls`, and keeps
  **process-global** classifiers (`_CLASS_FIELD_CLASSIFIERS`, `setdefault` "earliest classification wins",
  `:105-111`). A second model that frees or fixes a different attribute set of the same class
  inherits the first model's classification. This is latent cross-fit state.
- Only `Fitness.__init__` calls it (`fitness.py:275-279`). **NSS samples before it builds its `Fitness`**
  (`nss/search.py:560`, after the run), so NSS relies on the user or another import having registered.
  MSG's docs say no registration is needed (`autofit_workspace/scripts/searches/mle.py:233-235`).

### 1.6 Gradient mode (`autofit/jax/gradient.py`)
- `Analysis.gradient_mode = "reverse"` class attribute (`analysis.py:86`). `AnalysisPoint` overrides it
  with `"forward"` (`lens/PyAutoLens/autolens/point/model/analysis.py:56`).
- `resolve_gradient_mode` (`gradient.py:45-57`). **The only consumer is MultiStartGradient**
  (`multi_start_gradient/search.py:466-475, 1028, 1126`).
- NUTS and SMC differentiate through blackjax's internal `jax.grad` (reverse), so they **silently ignore a
  `"forward"` declaration**.
- `Analysis.batched_memory_bytes(gradient=True)` always uses `jax.value_and_grad` (`analysis.py:414`),
  so MSG's memory guard (`multi_start_gradient/search.py:885-896`) measures reverse mode even when it
  will run forward mode.

### 1.7 Bijector / Scaler / Clipper
- `AbstractMLE.__init__` owns `clipper` (`search/mle/abstract_mle.py:16-22`). That gives it to BFGS/LBFGS
  (as scipy `bounds`, `bfgs/search.py:119-140, 296-315`) and to MSG (`xp.clip` projection,
  `clipper.py:148-204, 384-425`).
- Scaler and Bijector are **MSG-only** (`multi_start_gradient/search.py:1060-1110`). They are xp-dispatched
  and trace under jit (`bijector.py:103-118, 271-291`), composed as `fitness.call(_to_physical(phi))`.
  The NUTS/SMC metric is learned by blackjax instead (`scaler.py:33,54`).
- Unit cube versus physical: nested samplers hand physical vectors to `Fitness` via their own prior
  transform (Nautilus `PriorVectorized`, `nautilus/search.py:430`; NSS `vector_from_unit_vector(xp=jnp)`,
  `nss/search.py:416-421`). MCMC/MLE pass physical vectors. `Fitness` always expects physical.

### 1.8 Initializer under JAX
- `samples_from_model` (`initializer.py:57-145`). With `n_cores==1` it calls `samples_jax` (`:89-95`). The name
  is misleading: it is a plain serial Python loop that calls `fitness(...)` once per point (`:147-197`), so
  it uses whatever `_call` the search configured (eager for NUTS/SMC/Emcee/Zeus/Drawer, jit for BFGS-JAX).
- RNG is the global Python `random` (`initializer.py:298`, `mapper/prior_model/abstract.py:887`),
  **unseeded and separate from the search's `seed`**. `InitializerParamStartPoints` jitter is the
  exception: it uses its own `np.random.RandomState(seed)` (`:554`).
- `n_cores>1` takes the `SneakyPool` multiprocessing path (`:96-135`) even when `use_jax=True` (§3.6).

### 1.9 Test mode
- `test_mode_level() >= 2` skips `_fit` entirely (`abstract_search.py:839-844`). `_fit_bypass_test_mode`
  calls `analysis.log_likelihood_function(instance)` directly (`:1146-1230`). **No search's JAX path
  (jit, vmap or grad) is exercised in test modes 2 and 3.** CI therefore cannot catch the §3 crashes.
- Mode 1 calls each search's `apply_test_mode` (shrinks iterations, e.g. NUTS `nuts/search.py:240-242`).

---

## 2. Per-search matrix

Legend: **Req** = raises without JAX; **Opt** = has a JAX path; **Ign** = no JAX path (JAX analysis
runs eager). "jit/grad/vmap" means *the likelihood* is compiled, differentiated or batched by that search.

| Search (file) | JAX relation | jit | grad | vmap / batch | use_jax=False | use_jax=True | How selected |
|---|---|---|---|---|---|---|---|
| DynestyStatic / DynestyDynamic (`nest/dynesty/search/abstract.py`) | Opt | yes via `Fitness._jit` (`:228`) | no | no | numpy; fork pool if cores>1 (`:249-271`) | jit, pool forced off (`:249`) | ctor kwarg `use_jax_jit=True` (`:93,159`) **AND** `getattr(analysis,"_use_jax",False)` |
| Nautilus (`nest/nautilus/search.py`) | Opt | yes (inside `_vmap`) | no | yes, `Fitness._vmap`, `vectorized=fitness.use_jax_vmap` (`:341,434`) | numpy; multiprocessing pool (`:352-365`) | jit(vmap) batched, `fit_x1_cpu` (`:330-345`) | ctor `use_jax_vmap=True` (`:198`) **AND** runtime `analysis._use_jax` (`:330`) |
| NSS (`nest/nss/search.py`) | Req **but no check** | own `@jax.jit one_step` (`:456`) | no (slice sampling is gradient-free) | blackjax vmaps / `lax.map` chunks (`_chunked_*.py`) | **crashes mid-trace** (TracerArrayConversionError, probe 2) | runs; **bypasses Fitness** (own guard closure `:88-100`) | none, unconditional |
| Emcee (`mcmc/emcee/search.py`) | Ign | **no** | no | no | numpy (+pool) | **eager jnp per call** (`:138-147`), fork pool still allowed (`:149`) | none |
| Zeus (`mcmc/zeus/search.py`) | Ign | **no** | no | no | numpy (+pool) | **eager jnp**, pool allowed (`:174-185`) | none |
| BlackJAXNUTS (`mcmc/blackjax/nuts/search.py`) | Req | own `@jax.jit log_density` (`:314`); `lax.scan` chunks unjitted (`:405-412`) | yes (blackjax, reverse only) | `jax.vmap` over chains (`:351,394`) | ValueError, fail-fast on `_xp` (`:263-272`) | runs; initializer eager (`:285-291`) | runtime `_xp` probe |
| SMC (`mcmc/blackjax/smc/search.py`) | Req | own `jax.jit(jax.vmap(...))` (`:509`) | yes (MALA/HMC, reverse) | yes | ValueError on `_xp` (`:322-330`) | runs | runtime `_xp` probe |
| BFGS / LBFGS (`mle/bfgs/search.py`) | Opt | yes, `fun=fitness._jit` (`:298-306`) | **no: no `jac=` passed, scipy does finite differences on a jitted fn** | no | numpy via `fitness.__call__` (`:307-315`) | jit, **bypasses `call_wrap`** so no quick update / history | runtime `analysis._use_jax` |
| Drawer (`mle/drawer/search.py`) | Ign | no | no | no | numpy | **eager jnp** (`:114-124`) | none |
| MultiStartAdam / ADABelief / Lion / Prodigy (`mle/multi_start_gradient/search.py`) | Req | own `jax.jit(jax.vmap(value_and_grad))` (`:1145`) | yes, honours `gradient_mode` (`:1028,1126`) | yes; `batch_size` chunks (`:1147-1165`) | ValueError on `_use_jax` (`:958-964`) | runs; Fitness built with no jit flag (`:983-994`) | runtime `_use_jax` probe + ImportError on jax/optax (`:944-956`) |

### Inconsistencies (numbered for the epic)
I1. **Four probes for "is this JAX?"**: `getattr(analysis,"_use_jax",False)` (Dynesty, MSG, abstract_search
    `:416,:643`), bare `analysis._use_jax` (Nautilus `:330,:419`, BFGS `:298`; AttributeError on analyses
    without it), `analysis._xp.__name__` (NUTS, SMC, Fitness `_is_jax`), and *none* (NSS, Emcee, Zeus, Drawer).
I2. **Three per-search knobs that each mean "compile it"**: Dynesty `use_jax_jit`, Nautilus
    `use_jax_vmap` (plus an unrelated numpy-pool `vectorized`, `:184`), and `SettingsSearch.use_jax_vmap=True`
    (`settings.py:18,59`). The last is splatted into **every** search, where `**kwargs` swallows it
    silently for any search that doesn't use it (`abstract_search.py:160`).
I3. **Four ways to build the compiled callable**: `Fitness._jit/_vmap` (Dynesty, Nautilus, BFGS);
    search-local closure over `fitness.call` (NUTS, SMC, MSG); a closure that bypasses Fitness
    entirely (NSS, `nss_log_likelihood_from`); none (Emcee, Zeus, Drawer).
I4. Failing fast: NUTS/SMC/MSG raise `ValueError` up front. NSS, the one other JAX-only search, does not.
    The error messages also differ, and NUTS/SMC tell users to call `enable_pytrees()/register_model()`,
    which `Fitness` already does.
I5. Gradient mode is honoured by MSG only. `Fitness.grad` exists and is unused.
I6. The NaN/ceiling/assertion guards are implemented twice: in `Fitness.call` and in NSS's
    `nss_log_likelihood_from` (`nss/search.py:88-100`). The NSS copy **has no assertion handling** (§3.3).
I7. Sentinels: `-inf` (Emcee, Zeus, BFGS, Drawer, NUTS `-jnp.inf`, MSG) versus `-1e99` (Dynesty,
    Nautilus, SMC, NSS). Same purpose, chosen per search.

---

## 3. Failure modes and surprises (with evidence)

3.1 **A JAX analysis on a gradient-free search with no JAX path runs eager and silently slow.**
    Emcee/Zeus/Drawer build `Fitness` without `use_jax_jit` (`emcee/search.py:138`, `zeus/search.py:175`,
    `drawer/search.py:114`), so `_call is call` (probe: `True`) and each evaluation dispatches op by op.
    Probe on `af.ex.Gaussian`: **7.80 ms eager vs 0.29 ms jitted per call**. Because PyAutoLens/PyAutoGalaxy
    analyses default to `use_jax=True` (§1.1), `af.Emcee` on an `al.AnalysisImaging` hits this by default.
    The only per-call compilation left is whatever PyAutoArray decorators jit internally
    (`analysis.py:125-128`). NUTS's and SMC's initializer points and BFGS's resume `fitness(...)` calls also
    go eager for the same reason.
3.2 **`Nautilus(force_x1_cpu=True)` with a numpy analysis crashes.** The `force_x1_cpu or _use_jax`
    branch (`nautilus/search.py:330-341`) always passes `use_jax_vmap=self.use_jax_vmap` (default True), so
    a numpy `Fitness.call` gets traced by `jax.jit(jax.vmap)`. Probe 1: `TracerArrayConversionError`.
3.3 **NSS fails late, not fast.**
    (a) With a numpy analysis it raises `TracerArrayConversionError` inside blackjax init (probe 2). There is
    no `_use_jax` check anywhere in `nss/search.py`.
    (b) With **any model assertion** it raises `TracerBoolConversionError`, because
    `instance_from_vector(xp=jnp)` keeps the raising assertion check (`nss/search.py:94`;
    `mapper/prior_model/abstract.py:990`) (probe 4). `Fitness` solved this with traced assertions; NSS never adopted it.
    (c) NSS builds its `Fitness` *after* sampling (`nss/search.py:560-567`), so the resume
    likelihood-sanity check (`fitness.py:319`) runs at the end of a resumed run, not the start.
3.4 **BFGS on JAX is jit plus finite differences.** `optimize.minimize(fun=fitness._jit, ...)` passes no
    `jac=` (`bfgs/search.py:298-306`). scipy makes about n_params+1 jitted calls per gradient, while an exact
    `jax.grad` sits unused (`Fitness.grad`). The workspace also says `use_jax=False` "is required by LBFGS"
    (`fit/autofit_workspace/scripts/searches/mle.py:84`), which contradicts the code's JAX branch.
    On the JAX branch, `store_history` and the quick update never fire (the `call_wrap` bypass), so
    `should_plot_start_point` history is empty there (`:316-319`).
3.5 **dtype.** x64 is forced only through an env var at `autonerves` import (`jax_wrapper.py:87-105`).
    If the user imports `jax` first, fp32 runs silently. No search asserts `jax.config.jax_enable_x64`
    (the SMC docstring says it needs float64, `smc/search.py:102`). The mixed-precision ("mp") lever lives
    in PyAutoArray, so the search has no view of which precision a likelihood actually uses.
3.6 **multiprocessing combined with JAX.** Dynesty and Nautilus deliberately drop the pool under JAX
    (`dynesty/.../abstract.py:249`, `nautilus/search.py:330`). Emcee (`make_sneaky_pool`, `emcee/search.py:149`),
    Zeus (`make_pool`, `zeus/search.py:174`), the initializer (`initializer.py:96`) and
    `abstract_search.make_pool` (`:1632-1643`, `fork_context().Pool`) **fork with JAX already initialised**
    when `number_of_cores>1`. Forking after JAX init is a known deadlock pattern; compare the EP 27-hour
    hang rationale at `abstract_search.py:388-404`.
3.7 **Dynesty swallows `RuntimeError`.** `except RuntimeError` is used as control flow (`abstract.py:250,273`),
    so any RuntimeError from a pooled run (XLA's `XlaRuntimeError` subclasses it) silently restarts the run
    single-core.
3.8 **Retracing.** `Fitness._vmap` recompiles for each distinct Nautilus batch length (`fitness.py:890-893`).
    NUTS `run_chunk` is unjitted around `lax.scan` (`nuts/search.py:405-412`); chunk lengths come from
    `_steps_until_full_update`, so a ragged final chunk recompiles. MSG pads chunks to avoid exactly this
    (`:1147-1165`), so the fix exists in one search but not the others.
3.9 **Double-jit.** Not found in the library: the outer jits wrap `fitness.call`, never `fitness._jit`.
    Inner PyAutoArray per-function jits inline under the outer jit, which is harmless.
    `batched_memory_bytes` builds a `Fitness(use_jax_vmap=True)` but then ignores `_vmap` and re-jits by hand
    (`analysis.py:399-416`), which is wasted but harmless.
3.10 **RNG.** The seed lives in four different places:
    - JAX `PRNGKey(self.seed)`: NUTS (`:321`, default 42), SMC (`:494`, 42), NSS (`:413`, 42);
    - numpy `SeedSequence`: MSG (`:1933-1954`, default None mapped to hardcoded 0/1 streams);
    - passed to the sampler: Nautilus (`:443`, None);
    - unseeded: Emcee, Zeus, Dynesty (no `seed`/`rstate` anywhere in their files) and the shared Initializer
      (global `random`).
    So "seed=42" does not make a NUTS run reproducible: its starting points come from the unseeded initializer.
3.11 **Pickling and resume.** `Fitness` strips its jitted attributes and rebuilds them (`fitness.py:835-863`).
    That is sound, but every resume and every fork pays a full recompile, softened only by the persistent
    compile cache (`jax_wrapper.py:107-136`). NSS checkpoints go through numpy (`nss/search.py:~105-145`) and
    are portable. NUTS, SMC and MSG keep their JAX closures outside `Fitness`, which is fine for pickling
    because they are rebuilt in `_fit`.
3.12 **Silent fallbacks.**
    - `use_jax=True` without JAX installed: warns and downgrades (`analysis.py:97-116`), after which NUTS,
      SMC and MSG raise further down, with messages that do not mention the missing install.
    - `PYAUTO_DISABLE_JAX=1` downgrades without logging anything (`analysis.py:94-95`).
    - The ceiling guard warns only on numpy (`fitness.py:79-85`).
3.13 **Process-global pytree classifier** (`pytrees.py:105-111`), see §1.5.

---

## 4. How downstream declares JAX-compatibility

- The **only** declarations are `use_jax` (a runtime choice, not a capability) and `gradient_mode`
  (`AnalysisPoint` forward). There is no `supports_jax`, `jax_traceable` or `differentiable` attribute on
  `af.Analysis`. The two nearest relatives are:
  - `supports_jax_visualization`, which just echoes `_use_jax` (`analysis.py:357-359`);
  - `supports_background_update` (`:352`).
- PyAutoLens has per-component checks that never reach the search. For example,
  `lens/PyAutoLens/autolens/point/solver/implicit_diff.py:105` `tracer_is_jax_compatible` and
  `ShapeSolver` "rejects use_jax=True" (`shape_solver.py:584`) both raise at likelihood time.
- `latent_batch_mode` ("vmap" / "jit" / "none") on Analysis (`analysis.py:40-52`) is the one existing
  precedent for an analysis declaring a *traceability level*, but only for latents.
- **The search cannot know in advance whether a likelihood is traceable.** The nearest thing to a
  probe is `batched_memory_bytes`, which lowers the batched likelihood (`analysis.py:391-420`) but runs only
  in MSG's memory guard. Today a non-traceable likelihood surfaces as a tracer error at the first compile.
  That compile happens inside sampler internals for NSS/Nautilus, or inside `Fitness.__init__` for resumed runs.
- In practice:
  - `autolens_inference` currently configures **only Nautilus** with `use_jax=True` and
    `use_jax_vmap=True, batch_size=N_BATCH` (`lens/autolens_inference/scripts/misc/searches/_point_runner.py:515,543-544`);
    `scripts/imaging/searches/README.md` says the gradient searches are "phase later".
  - Gradient searches are exercised in `fit/autofit_workspace_test/scripts/searches/{MultiStart*,BlackJAXNUTS,NSS}.py`
    and `lens/autolens_workspace_developer/searches_minimal/` (which hand-rolls `jax.grad` around a separate
    objective, `_grad_setup.py:280`, so it bypasses `Fitness` too).

---

## 5. Proposed unified contract

### 5.1 Declarations
```python
class JaxUse(enum.Enum):
    NONE = "none"          # sampler is pure Python/numpy; JAX analysis still gets a jitted scalar fn
    OPTIONAL = "optional"  # has a batched/jitted fast path when the analysis is traceable
    REQUIRED = "required"  # cannot run without a traceable likelihood

class Gradient(enum.Enum):
    NONE = "none"; USES = "uses"   # USES implies JaxUse.REQUIRED (or OPTIONAL for BFGS: jac when available)

class NonLinearSearch:
    jax_use: ClassVar[JaxUse] = JaxUse.NONE
    gradient: ClassVar[Gradient] = Gradient.NONE
    batched: ClassVar[bool] = False      # consumes a vmapped likelihood
    honours_gradient_mode: ClassVar[bool] = False
```
These are class attributes, so docs, the search summary (`search.json` / `model.info` header) and the
Samplers faculty can read them without running anything.

On the analysis side:
- `Analysis.use_jax` stays the user's *choice*;
- add a read-only `Analysis.is_jax` property, the **single probe** that replaces I1's four;
- optionally add `Analysis.jax_traceable: bool | None` (a capability declaration, default `None` = unknown).

### 5.2 One factory
Add `Fitness.objective(kind)` (or a module function `build_objective(fitness, kind)`) where
`kind ∈ {"scalar", "batched", "value_and_grad", "batched_value_and_grad"}`:
- on numpy it returns the plain callable for "scalar"/"batched" (Python loop) and **raises** for grad kinds;
- on JAX it returns the jitted variant, wrapped in `log_on_first_compile`, honouring `gradient_mode`, and
  padding to a fixed batch shape (MSG's chunk logic lifted out);
- it is cached per kind and stripped on pickle as today.

Every search calls this factory. That deletes `use_jax_jit` / `use_jax_vmap` as search knobs, which
become deprecated aliases. `SettingsSearch.use_jax_vmap` goes away.
The rule for `jax_use=NONE` searches given a JAX analysis: **they still get the jitted scalar**. That
fixes §3.1, so Emcee, Zeus and Drawer become effectively "OPTIONAL-scalar".

### 5.3 Fail-fast gate (in `NonLinearSearch.fit`, before `_fit`)
- If `jax_use is REQUIRED and not analysis.is_jax`, raise `SearchException`, with one shared message.
- If `analysis.is_jax`, run a **trace preflight**: `jax.eval_shape(objective, prior-median vector)`, plus
  `jax.eval_shape(grad)` when `gradient is USES`. That costs one trace, with no compile or execution. On
  failure, raise a message naming the tracer error and the search. This catches §3.2, §3.3 and
  non-traceable PyAutoLens components before any sampler state exists.
- If `analysis.is_jax and number_of_cores > 1` and the search would fork, refuse (as EP does) or force
  cores=1 with an INFO line. One rule instead of three.
- If `analysis.is_jax and not jax.config.jax_enable_x64`, warn once (or raise when the search declares
  `requires_fp64`).

### 5.4 Ruling on RNG
- **A single `seed` on `NonLinearSearch`** (not per subclass).
- The search derives `np.random.SeedSequence(seed)`. Stream 0 goes to the Initializer, which then **stops
  using global `random`**. Stream 1+ go to the sampler: a numpy `Generator` for Emcee/Zeus/Dynesty `rstate`
  and Nautilus, and `jax.random.key(int)` for blackjax/NSS.
- `seed=None` keeps today's behaviour. JAX keys live only inside `_fit` and are checkpointed alongside
  sampler state, as NSS already does for `run_key`.

### 5.5 Single guard path
NSS adopts `Fitness.call` (via the factory) instead of `nss_log_likelihood_from`. That gives it traced
assertions and one ceiling/NaN implementation. The resample sentinel also becomes a class attribute
(`resample_figure_of_merit`) per search instead of a literal at each call site.

### 5.6 Migration phases
**Phase 1 — Declare and gate (no behaviour change for valid runs).**
- Add `jax_use/gradient/batched/honours_gradient_mode` class attributes and `Analysis.is_jax`. Replace the
  four probes (I1).
- Add the REQUIRED fail-fast gate and the shared message.
- Fix `AnalysisFactor` lacking `_use_jax`, and derive `FactorGraphModel.use_jax` from its children (all
  equal, else raise).
- Surface the capabilities in the search summary and in `model.info`.
- *Searches touched:* all 15 (attributes only). Logic changes in NSS (gate), NUTS, SMC and MSG (shared
  message), Nautilus (`force_x1_cpu`+numpy: pass `use_jax_vmap=False`, fixing §3.2).
- *Tests:* parametrised over every search class, asserting the declared attributes; REQUIRED search plus
  numpy analysis raises `SearchException`; FactorGraphModel inherits use_jax; Nautilus
  `force_x1_cpu` with numpy runs.

**Phase 2 — One objective factory.**
- Add `Fitness.objective(kind)`. Port the call sites to it:
  - Dynesty and BFGS → `scalar`;
  - Nautilus → `batched`;
  - Emcee, Zeus, Drawer, initializer → `scalar` (fixes §3.1);
  - MSG → `batched_value_and_grad`, lifting its padding logic;
  - NUTS → `scalar` + blackjax grad, or `value_and_grad` honouring gradient_mode;
  - SMC → `batched`.
- BFGS gets `jac=` from `value_and_grad` on JAX (§3.4) and keeps `call_wrap` bookkeeping via a host-side
  wrapper.
- Deprecate `use_jax_jit` / `use_jax_vmap` kwargs (accept them with a warning). Delete `Fitness.grad`'s
  orphan status by making it the factory's grad kind.
- *Searches touched:* Dynesty×2, Nautilus, Emcee, Zeus, Drawer, BFGS, LBFGS, NUTS, SMC, MSG×4.
- *Tests:* a compile-count probe (`__wrapped__._cache_size()`, existing `test_fitness_vmap_cache.py`
  pattern) showing exactly one compile per kind; an eager-vs-jit timing guard for Emcee+JAX; BFGS-JAX
  `nfev` counts showing no finite differences; `gradient_mode="forward"` honoured by NUTS.

**Phase 3 — Preflight, NSS onto Fitness, multiprocessing and dtype.**
- `eval_shape` trace preflight in `fit()`.
- NSS uses `objective("scalar")` (gets traced assertions; sanity check moves to the start of the run).
- One fork rule for JAX (Emcee, Zeus, initializer, `make_pool`).
- x64 check.
- Dynesty `except RuntimeError` replaced by an explicit sentinel exception.
- *Searches touched:* NSS, Emcee, Zeus, Dynesty×2, plus the Initializer and `abstract_search.make_pool`.
- *Tests:* NSS with assertions under jit; preflight raising on a deliberately numpy-only likelihood
  (`np.asarray` inside); Emcee with cores=2 and JAX refusing or downgrading; fp32 warning.

**Phase 4 — RNG and documentation.**
- Search-level `seed` with SeedSequence fan-out, and an Initializer seeded from stream 0.
- Seed added to the identifier only when not None, so it does not fork existing output paths.
- Docs from §6.
- *Searches touched:* all 15 (seed plumbing); Emcee, Zeus and Dynesty gain reproducibility.
- *Tests:* same seed gives bit-identical initial points and samples for each search on the toy Gaussian;
  `seed=None` preserves the current identifier.

Also recommended: a test-mode level that **does** compile the objective once (`eval_shape` or a
single jitted call), since test modes ≥2 never touch JAX paths today (§1.9).

---

## 6. Documentation gap

| Place | Current state |
|---|---|
| RTD `fit/PyAutoFit/docs/api/searches.rst` | Lists Dynesty, Emcee, Zeus, BlackJAXNUTS, SMC, BFGS, LBFGS. **Omits Nautilus, NSS, Drawer and all four MultiStart searches.** No JAX column, no "requires use_jax". |
| RTD `docs/cookbooks/search.md` | Sections for Emcee, Zeus, Dynesty and LBFGS only (`:22-26`); no JAX mention at all. |
| RTD `docs/general/roadmap.md:8-10` | "Supported for autodiff is nearly implemented". Stale. |
| RTD `docs/overview/python_api.md:428` | One sentence, "GPU and gradient based methods using JAX". |
| `fit/autofit_workspace/scripts/searches/README.md` | Says NSS is in `nest.py`. **`nest.py` contains no NSS and no `use_jax`** (it builds `af.ex.Analysis` without the flag, `:91`). |
| `autofit_workspace/scripts/searches/mcmc.py:241-247,283` | Tells users to call `enable_pytrees()/register_model()` manually. Redundant with `fitness.py:275-279`. |
| `autofit_workspace/scripts/searches/mle.py:84` | "use_jax=False is required by LBFGS". Contradicts `bfgs/search.py:298`. |
| `lens/autolens_workspace/scripts/guides/modeling/searches.py:79-83` | Best existing prose (Nautilus = batched, not gradients). Says `jax.vmap(jax.jit(...))`, but the code is `jax.jit(jax.vmap(...))` (`fitness.py:874-880`). |
| Docstrings | NUTS/SMC/MSG/Nautilus class docstrings mention use_jax. Emcee, Zeus, Drawer, Dynesty and BFGS docstrings say nothing about what happens under JAX. |
| `Fitness.__init__` docstring (`fitness.py:188-249`) | Does not document `use_jax_vmap`, `use_jax_jit` or `batch_size` at all. |

**Proposal:** generate one "Search × JAX" table from the §5.1 class attributes (an autosummary extension
or a small script) into RTD `api/searches.rst` and the workspace `searches/README.md`, so the table cannot drift.
