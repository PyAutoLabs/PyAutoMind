# Fitness._vmap re-traces and eagerly executes the batched pjit on every call — wrap it in an outer jit

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Witness: `Fitness._vmap` called twice on the same shapes traces once (assert via `jax.make_jaxpr` count or a trace-counter callback), all PyAutoFit JAX tests pass, and the multi_dataset jax_likelihood scripts in autolens_workspace_test / autogalaxy_workspace_test produce bit-identical likelihoods before and after.
Unattended: ready
Filed: 2026-09-07

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
