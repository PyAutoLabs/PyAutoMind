# Phase 3: root-cause the XLA vmap compile stall and clear every NEEDS_FIX it caused

Type: bug
Target: ci
Repos:
- @PyAutoFit
- @autogalaxy_workspace_test
- @autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Epic: jax-compile-stall
Phase: 3
Campaign: bug/ci/jax_vmap_jit_compile_stall.md (Phase 3 — the fix; blocked on phases 1 and 2)
Filed: 2026-08-23
Issued: 2026-08-27

## Blocked on phase 1

Do not start this before phase 1's watchdog has shipped and a CI stall has
actually dumped a traceback. Diagnosing a hang that leaves no evidence is what
produced three quarantines and no root cause; repeating it without the
instrumentation would be a fourth.

## Reproduce deliberately

Loop `imaging/jax_likelihood/mge_group.py` under its declared CI env profile
until it hangs, rather than waiting for CI to hit it. Attach `py-spy dump` to
the hung process as well as reading phase 1's own `faulthandler` output — the
two see different things, and `py-spy` can read native frames the in-process
dump cannot.

## Hypotheses, in the order they are cheapest to test

1. **`vmap` of `jit`, the inverted ordering.** `Fitness._vmap`
   (`autofit/non_linear/fitness.py`) builds `jax.vmap(jax.jit(self.call))`;
   `autofit/non_linear/analysis/latent.py` builds
   `jax.jit(jax.vmap(compute_latent_for_model))`, the conventional order. The
   stalling path is exactly the `vmap` path, and the `_jit`-only scripts in the
   same directories do not stall. One-line A/B — try it first.
2. **Persistent compilation cache contention.** `JAX_COMPILATION_CACHE_DIR` has
   defaulted on since PyAutoConf#128 (merged 2026-07-17). Both NEEDS_FIX stalls
   post-date it; the eight SLOW entries predate it. A/B with the cache dir set
   to empty (which disables it) and see whether the stall probability moves.
3. **JAX/XLA version interaction.** This repo has form: `delaunay_mge.py` is
   disabled outright because `jax 0.7` removed
   `jax.interpreters.xla.pytype_aval_mappings`, and the smoke installer once
   clobbered a working `tfp-nightly`. Pin-bisect jax/jaxlib across a run set.
4. **Runner CPU contention.** `complete/2026/07/jax-compile-time-research.md`
   records that XLA compiles on **host** CPUs and that compile timing is
   load-sensitive by up to 7×, which is why a hosted runner is the place this
   reproduces and a workstation is not.
5. **Graph size in the vmap trace.** The affected set has a shape: plain `mge.py`
   passes in 9.4s, while the *composite* variants — group, rectangular-MGE,
   delaunay-MGE — stall or are already out. Complexity-driven compile blowup was
   argued against by the autolens_profiling#71 research ("compile cost is
   op-pattern-driven, not complexity-driven"), so treat this as the hypothesis
   of last resort, not the first.

## Then restore the coverage

The point of the campaign. Quarantining removes exactly the heaviest JAX paths,
which are the ones most worth testing.

1. Clear the NEEDS_FIX markers this campaign inherits — including the
   2026-08-01 `multi_dataset/jax_likelihood/rectangular.py` one and the
   `autolens_workspace_test` `delaunay.py` entry citing #245.
2. Re-enable `multi_dataset/jax_likelihood/mge.py` and `shared_preloads.py` in
   `autolens_workspace_test`'s `smoke_tests.txt` (folded in from the superseded
   2026-08-22 filing).
3. Anything that stays out after the fix stays out with a **recorded deliberate
   reason**, not as an accumulated one-off.

## Acceptance

- A stated root cause, or an explicit recorded decision that it is an
  infrastructure limit to be worked around rather than fixed. Not another
  quarantine.
- Every entry marked NEEDS_FIX for this signature restored to its suite, or
  re-marked with the real reason phase 2 established.
- The `multi_dataset/jax_likelihood/` family back under CI coverage in both test
  workspaces, or its absence recorded as a deliberate choice.
