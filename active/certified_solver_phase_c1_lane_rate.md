# Certified solver phase C1 — uncertified-lane rate and batched timing on real Nautilus batches

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- inversion
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: sliced 2026-09-24 — measurement only; release block overridden by the human ("Build it now against main", then "yes meaurement only"): runs against library mains incl. unreleased PyAutoArray#567, no library edits
Epic: certified-positive-solver
Phase: C1
Consequence: judge
Witness: captured real Nautilus proposal batches at production n_batch=20 (euclid pipeline source_pix stages) for HST Delaunay N=1500 and rectangular; A100 fp64 replay under library certified+fallback none jit(vmap) reporting the uncertified-lane rate (overall and by Nautilus phase) and max passes vs budget 16; matched timing table at B=16/20/50/100 (PDIP vmap, certified+none vmap, scalar certified+PDIP, scalar PDIP) with every lane <= 1e-9 against scalar library PDIP; a verdict note deciding C2 (`draft/feature/autofit/certified_solver_batched_guard_c2.md`).
Review-minutes: 20
Unattended: no
Filed: 2026-09-24
Issued: 2026-09-24

## Scope (sliced 2026-09-24)

Only item 1 (measure) and item 4 (vmap policy stated with batch size) of the original What below.
Items 2-3 (flag + Fitness fallback) moved to C2. Verdict rule: build C2 only if projected guarded
cost (certified+none batch + rate x scalar certified+PDIP re-run) at B=20 is >= 15% below the best
zero-code option (library PDIP vmap; or scalar certified via config opt-in + use_jax_vmap=False on
the pixelized stages), with the rate near zero.

## Why

Certified-solver phase B (autolens_profiling#300, PR #302; note
`autolens_profiling/results/notes/certified_solver_policy_phase_b_2026_09.md`) measured the library
solvers under the production composition `jax.jit(jax.vmap(fn))` on an A100. Under vmap the
certified solver's PDIP fallback `lax.cond` becomes a `select`, so every lane pays both solvers:
certified+PDIP is slower than library PDIP at every B (B16: 45.6 vs 38.9 ms/lane Delaunay, 38.6 vs
30.7 rectangular). Certified with `certified_fallback="none"` is the fastest batched row (B16 1.50x
Delaunay / 1.25x rectangular over PDIP vmap) and passed the 1e-9 gate with 0 uncertified lanes, but
with `none` an uncertified lane silently returns the last active-set iterate.

The policy adopted by the human on 2026-09-24 ("This sounds good, follow the proposed plan.") keeps
library PDIP as the vmap default now and moves to certified+none only once an uncertified-lane guard
exists. This prompt is that guard (policy item 4), plus the measurement that decides whether it is
worth building.

## What

1. **Measure first (autolens_profiling).** The phase-B lanes were one seeded draw family near the
   fiducial. Measure the uncertified-lane rate (and max passes vs the packaged budget 16) on real
   Nautilus batches: lanes drawn across the prior / from an actual Nautilus run's proposal batches,
   Delaunay and rectangular, at the batch size Nautilus uses in production. At a rate near zero the
   guard is cheap; at a high rate the host-side second pass erodes the gain and the vmap default
   should stay PDIP. Record the verdict before any library work.
2. **Per-lane certified flag (small PyAutoArray / PyAutoGalaxy surface).** The vmapped likelihood
   also returns the per-lane `certified` flag of the positive-only solve (the library already
   exposes it through the `stats=` out-dict), threaded out through the fit so `Fitness` can see it
   without changing the scalar return contract.
3. **Cond-free fallback (PyAutoFit).** `Fitness._vmap` (`autofit/non_linear/fitness.py`) runs the
   batch with certified + fallback none, then re-evaluates only the uncertified lanes through the
   scalar certified+PDIP program (a rare, host-side second pass outside the traced program) and
   splices their values back. Result: certified+none batch cost with PDIP semantics.
4. **State the vmap policy with the batch size** (policy item 5): against the scalar certified
   default the best batch wins only at B16 (1.14x / 1.15x), ties at B8 and loses at B4 — the policy
   must name the Nautilus batch size it applies to; small batches stay scalar.

## Context

- Epic: certified-positive-solver. Phase A = PyAutoArray#566 / PyAutoArray#567 (opt-in certified solver).
  Phase B = autolens_profiling#300 (policy grid, A100 array 350588).
- The scalar default flip (certified + PDIP fallback on `jit(fn)` only) was retired 2026-09-24 as
  superseded by this phase (`complete/2026/09/certified-solver-scalar-default-flip.md`): production
  always runs `jit(vmap)`, so this phase is the lever that reaches real fits.
- Delaunay carries a ~2e-10 run-to-run nondeterminism floor and a ~2.5e-9 cross-composition
  residual (program properties, not solver); do not draw pins tighter than 1e-9 on Delaunay.
