# Phase 3: root-cause the JAX likelihood hang and clear every NEEDS_FIX it caused

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
Campaign: bug/ci/jax_vmap_jit_compile_stall.md (Phase 3 — the fix)
Filed: 2026-08-23
Unblocked: 2026-08-26 (deterministic reproducer found; see below)

## UNBLOCKED 2026-08-26 — start from the deterministic reproducer

This phase carried a gate: *do not start before phase 1's watchdog has shipped
and a CI stall has actually dumped a traceback.* That gate is retired. It existed
because a hang that leaves no evidence cannot be diagnosed — but the evidence
problem has a way around it that nobody noticed.

**`autolens_workspace_test` `imaging/jax_likelihood/mge_group` never completes.**
Its `config/build/no_run.yaml` NEEDS_FIX entry (2026-08-24,
autolens_workspace_test#274) records 3/3 capped at 1800s on **both** Python legs
(run 32758924176) on top of 5/5 at 300s in phase 2 (run 32664682689) — **16/16
lifetime executions, zero completions** — with the compile finishing in ~16s and
the stack sitting in `jax.block_until_ready`.

So do not loop a script until it hangs and do not wait on CI. Run that one, under
`py-spy`, and it hangs on the first attempt. Confirm the 16/16 claim against those
two run IDs before building on it — it is one comment by one author — but if it
holds, the reproduction problem this campaign has had since 2026-08-01 is solved
and was solved two days before this phase was last touched.

**Why the ledger did not know.** That retime wrote its conclusion into a
`no_run.yaml` comment; the campaign ledger was edited on 2026-08-24 and
2026-08-25 and never learned it. Treat both workspaces' `smoke_tests.txt` and
`no_run.yaml` as primary sources for this campaign, not just as its output.

## First question: one defect or two?

Settle this before testing any hypothesis, because the answer changes which ones
are worth testing. Occurrences do not sort cleanly:

| Script | Tail ends on | Behaviour |
|---|---|---|
| al `imaging/jax_likelihood/mge_group` | compile **completed** (~16s), then silence | **deterministic** 16/16 |
| ag `multi_dataset/jax_likelihood/mge_group.py` | compile **completed** (11.7s), then silence | intermittent (passed 41.2s on re-run) |
| ag `imaging/jax_likelihood/mge_group.py` | still `compiling...` | intermittent |
| ag `imaging/jax_likelihood/rectangular_mge.py` | still `compiling...` | intermittent (3.12 stalled, 3.13 passed, same commit) |

A stall *inside* the first compile and a hang *after* it returned are different
loci. The "intermittent XLA compile stall" label was applied to both from a guess
made before any evidence existed (see the ledger's § CORRECTION). One stack from
the deterministic case, plus one from any intermittent one, answers it.

If it is one defect, the deterministic script is simply the best specimen and
everything below applies to all of them. If it is two, split this phase and stop
treating the intermittent rotation and the permanent hang as one problem.

## Then: hypotheses, in the order they are cheapest to test

Ordering note (2026-08-26): hypothesis 1 was the campaign's leading candidate.
It should no longer be. Phase 2's A/B already showed the stall **survives** the
swap (80% -> 30%, p = 0.070, n=10/arm), and at least two occurrences hang after
the compile that ordering governs. Test it for completeness, not first.

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
