## fitness-vmap-outer-jit
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1636
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1638
- summary: |
    `Fitness._vmap` is now `jax.jit(jax.vmap(self.call))` instead of
    `jax.vmap(jax.jit(self.call))`: the conventional order, the one
    `analysis/latent.py` already used, and the last vmap-of-jit site in
    PyAutoFit. The whole batch is one XLA program keyed on the batch shape; a
    same-shape repeat call is served from jit's C++ fast path with no Python
    batching trace. The inner jit is dropped (a nested jit is inlined).
    `log_on_first_compile`'s wrapper carries the jitted callable on
    `__wrapped__` so `_cache_size()` is a compile-count probe. Four new tests
    in `test_autofit/non_linear/test_fitness_vmap_cache.py`: traced once per
    batch shape, one cache entry after a same-shape repeat, one more per new
    batch length, `jit(vmap)` bitwise equal to `vmap(jit)` on the example
    analysis (max abs diff 0.0), `call_wrap` promotes `(d,)` to a length-1
    batch equal to the numpy value, cache rebuilt after a pickle round-trip.
    Full serial suite 2807 passed / 48 skipped; CI Tests 3.12 / 3.13 / nojax
    and Docs green on f28e986; merged as 3abbc13. Log strings and the
    jax_compile.py heartbeat contract unchanged.
- premise-correction: |
    The prompt claimed the outer jit "halves the exposure" to the Eigen-pool
    deadlock because the second call becomes a cache hit. It does not, by
    construction: the executable was already cached on main (the inner pjit's
    jaxpr and lowering caches key on the per-example avals; `batch_jaxpr2` is
    `weakref_lru_cache`d), so the compile count was 1 either way, and the
    deadlock (PyAutoFit#1530, XLA CPU FftThunk re-entering the Eigen pool via
    ducc0) fires at execution, which still happens once per call under either
    order. What the ordering changes is the HLO (one fused batch program
    instead of a batched inner pjit). The only measurement of that is the
    2026-08-23 A/B on rectangular_mge.py from `experiment/jax-vmap-jit-ordering`
    (complete/2026/08/jax-compile-stall-slow-vs-stall-audit.md): control 8/10
    stalls vs 3/10 for jit-of-vmap, Fisher p=0.070, contributory not causal.
    Recorded on the issue, the PR and the docstring so nobody reads "halves
    exposure" as measured. The witness was re-worded onto what is observable
    (the trace-count assertion alone passes on main too; the outer jit's
    cache size is what distinguishes the two compositions).
- measurement: |
    autogalaxy_workspace_test retime.yml, multi_dataset/jax_likelihood/delaunay.py,
    5 repeats, 300 s cap, smoke profile (eigen flag in force), both Python legs.
    jit(vmap) arm = run 35248541614 on the empty same-named branch
    feature/fitness-vmap-outer-jit (chain checkout picked the PyAutoFit branch;
    the feature arm wrote 33 new compile-cache entries per leg vs 22 for
    control, the new HLO being compiled). Control = run 35248545944 on main.
    All four legs: NEITHER, 5/5 completed, slowest 16-19 s. First _vmap
    compile 1.5-1.7 s in both arms (persistent cache restored in both), so the
    "outer jit adds one compile" cost is below the noise. Printed _vmap batch
    identical across all four legs at print precision; the script's
    full-precision jit scalar 2223.242597233474 byte-identical in all four.
    Second-call time unchanged (~0.40 s for a batch of 3). Stall rate not
    measurable here: 0/20 hangs in both arms under the smoke profile. The
    delaunay.py no_run.yaml quarantine stays.
- traps: |
    - autogalaxy_workspace_test's retime.py has no `--arm` (the ABAB overlay
      lives in autolens_workspace_test's copy), so an A/B there is two
      dispatches minutes apart, not ABAB within one dispatch.
    - The measurement branch in autogalaxy_workspace_test is an empty branch
      off main e8b2f38 with no PR; it exists only so the chain checkout picks
      the PyAutoFit branch. GitHub does not delete it (no PR merged), so it is
      branch_sweep.yml's.
    - `functools.wraps` was avoided for `__wrapped__`: it copies `__dict__`
      and would alias the jit object's attributes onto the wrapper.
    - `git merge-base --is-ancestor origin/feature/<task> origin/main` fails
      with "couldn't find remote ref" after the merge because GitHub deletes
      the merged head; prove against the local branch (or the PR state).
- adjacent-not-folded: |
    draft/bug/autofit/vmap_jit_recompiles_per_nautilus_batch_length.md (same
    line of code; the outer jit keys on batch length exactly as the inner one
    did, neither fixed nor worsened; the `_cache_size()` read is its probe).
    draft/refactor/autofit/ep_analysis_level_compile_cache.md and
    split_fitness_batch_size_lh_vs_latent.md unaffected. intake reconcile
    over draft/refactor/autofit: 0 suspects of 205.
- provenance: |
    Planned, shipped and closed out in one web-github session (no task
    worktree; session clones). Fable session planned and judged; an Opus
    execution-tier subagent implemented and ran the suite. Heart not
    consulted (pyauto-heart unreachable from the web container); the full
    serial suite plus CI was the substitute gate; freeze flag unreadable, an
    absent flag is not a freeze. Shadow row: tier notify, stage 1,
    merged-unchanged, answered from the merge evidence (single commit, head sha
    unchanged since PR-open, merged at expectedHeadSha) rather than by asking.

## Original prompt

# Fitness._vmap re-traces and eagerly executes the batched pjit on every call — wrap it in an outer jit

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: notify
Witness: `Fitness._vmap` called twice on the same shapes traces once (assert via `jax.make_jaxpr` count or a trace-counter callback), all PyAutoFit JAX tests pass, and the multi_dataset jax_likelihood scripts in autolens_workspace_test / autogalaxy_workspace_test produce bit-identical likelihoods before and after.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-07
Issued: 2026-09-17

CI forensics on autogalaxy_workspace_test#118 (2026-09-07): the two Release Integrate
hangs of `multi_dataset/jax_likelihood/delaunay.py` (runs 34018429178 and 34094964905)
park in jax `_pjit_call_impl` reached via
`vmap_f -> flatten_fun_for_vmap -> cache_miss -> _pjit_batcher` — the inner pjit that
`Fitness._vmap = jax.vmap(jax.jit(self.call))` executes eagerly under the batching trace.

With no outer jit every call re-traces, so a script that calls `_vmap` twice gets two
independent exposures to the intermittent xla-cpu-eigen-pool-deadlock (epic), and the two
CI hangs landed on the first and the second call respectively. Wrapping the vmap in an
outer `jax.jit` (or caching the batched executable) makes the second call a cache hit and
halves the exposure for every composite-vmap script in the workspace_test repos.

Not a fix for the deadlock itself; a real reduction in how often it is rolled.

Measure compile time before/after on one script (the outer jit adds one compile) and
confirm no change to `jax_compile.py`'s heartbeat contract in PyAutoNerves/PyAutoHands.

Related quarantines: autolens_workspace_test and autogalaxy_workspace_test
`config/build/no_run.yaml` eigen-pool entries.
