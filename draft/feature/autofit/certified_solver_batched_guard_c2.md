# Certified solver phase C2 — cond-free batched fallback (uncertified-lane guard) under jit(vmap)

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
Themes:
- profiling
- inversion
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft — C1 verdict recorded 2026-09-25 (human: proceed; build rule passes in 3/4 cells; 2026-09-25 human decisions: gate Δ = 100 / 0.1 nats adopted, rectangular pix1 stays on PDIP vmap — see "Human decisions (2026-09-25)"); still blocked on the PyAutoArray#567 release
Epic: certified-positive-solver
Phase: C2
Consequence: judge
Blocked-by: the PyAutoArray release shipping PyAutoArray#567 (the C1 verdict is recorded: human chose to proceed on 2026-09-25)
Witness: (1) DONE by C1 (autolens_profiling#304): uncertified-lane rate measured on real
Nautilus batches, 1.9-4.9% overall, 0 in the late half. (2) One matched A100 fp64 table (HST
Delaunay N=1500 and rectangular, production B=20) where the guarded batch (certified + fallback
none under `jax.jit(jax.vmap(fn))`, uncertified lanes re-run through the scalar certified+PDIP
program) runs within a few percent of the certified+none batch cost, gated by a gate
PRE-REGISTERED before the run: (a) a near-peak nats pin — every finite lane with log L within
Δ of the batch maximum agrees with scalar library PDIP to within a pinned tolerance in nats
(ADOPTED by the human 2026-09-25: Δ = 100 nats of the batch maximum log likelihood, pin 0.1 nats); (b) a gated
cross-composition check (vmap vs per-lane scalar jit of the same Settings) and a gated capture
check (vs the capture's own Fitness value) on the same near-peak lanes, so a B=50-style
composition fault (draft/bug/autoarray/batched_jit_vmap_b50_wrong_log_likelihood_a100.md) fails
the gate instead of passing it; (c) PDIP `converged` / `iterations` recorded per lane from the
`stats=` dict (PyAutoArray#572); (d) stated NaN handling (a NaN lane is counted and reported per
composition; whether a NaN on a lane outside Δ fails the gate is decided at pre-registration);
plus an injected-uncertified-lane test proving the re-run path fires and replaces the lane's value.
Review-minutes: 30
Unattended: no
Filed: 2026-09-24

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

1. **DONE by C1 (autolens_profiling#304, 2026-09-25) — see "C1 findings".** **Measure first (autolens_profiling).** The phase-B lanes were one seeded draw family near the
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

## C1 findings (autolens_profiling#304, RAL array 350768)

Note: `autolens_profiling/results/notes/certified_solver_phase_c1_lane_rate_2026_09.md` (its
"Decisions (human, 2026-09-25)" section records the choices below).

- The C1 pre-registered gate (own-composition 1e-9 pin) FAILED and stays recorded as failed. The
  failures are lanes about 6e4-2.2e5 nats below the batch peak, where PDIP disagrees with itself
  between compilations (<= 0.86 nats gated, up to 1.8 nats across programs), and the designed
  uncertified iterates of `certified_fallback=none` (up to 57 nats timed, 141 nats in the rate
  replay), which the PDIP fallback catches.
- Uncertified rate (certified+none, B=20 chunks, budget 16): 1.97% / 4.88% / 1.88% / 2.46%
  (Delaunay pix1 / Delaunay pix2 / rectangular pix1 / rectangular pix2); prior phase 11.7-20.6%;
  late half 0 in every cell. "Near zero" is arguable.
- At B=50 `jit(vmap)` returns wrong values on 44-50/50 lanes and the own-composition gate is blind
  to it: filed as `draft/bug/autoarray/batched_jit_vmap_b50_wrong_log_likelihood_a100.md`.
- Build rule, from the C1 B=20 timings. Guarded = certified+none vmap + overall rate x scalar
  certified+PDIP. Best safe zero-code option = library PDIP `jit(vmap)` (unguarded certified+none
  is not safe, so it is excluded):

  | cell | certified+none vmap | rate | scalar cert+PDIP | guarded | library PDIP vmap | saving | >= 15%? |
  |---|---:|---:|---:|---:|---:|---:|---|
  | Delaunay pix1 | 30.5 | 1.97% | 44.3 | 31.4 | 43.0 | 27% | yes |
  | Delaunay pix2 | 13.2 | 4.88% | 43.6 | 15.3 | 22.8 | 33% | yes |
  | rectangular pix1 | 26.5 | 1.88% | 44.7 | 27.3 | 30.6 | 11% | **no** |
  | rectangular pix2 | 11.5 | 2.46% | 35.7 | 12.4 | 17.0 | 27% | yes |

  At the prior-phase rates the guard loses on rectangular (pix1 26.5 + 14.3% x 44.7 = 32.9 vs 30.6;
  pix2 11.5 + 20.0% x 35.7 = 18.6 vs 17.0) and roughly ties on Delaunay pix2 (22.2 vs 22.8).
  The human chose to proceed with 3/4 cells passing.

## Human decisions (2026-09-25)

Recorded from the human's "do these:" reply to the agent's items on 2026-09-25.

1. **Near-peak gate values ADOPTED.** C2's pre-registered near-peak nats pin checks every finite
   lane within Δ = 100 nats of the batch maximum log likelihood against scalar library PDIP, pinned
   at 0.1 nats. These values were adopted by the human on 2026-09-25 and are no longer a proposal.
   The gated cross-composition and capture checks, the per-lane PDIP `converged` / `iterations`
   records and the NaN handling in Witness (2) stay as written.
2. **Per-mesh policy: rectangular pix1 STAYS on library PDIP `jit(vmap)` in C2.** The guard saves
   only ~11% there, which is below the 15% build rule, and it is slower at prior-phase rates (32.9
   vs 30.6). The guard targets Delaunay pix1, Delaunay pix2 and rectangular pix2. Rectangular pix2
   is also slower than PDIP at prior-phase rates (18.6 vs 17.0). That is left as a C2 measurement
   question and has not been decided.

## Open questions for C2

- ~~**Per-mesh policy** (rectangular pix1)~~ — CLOSED 2026-09-25: rectangular pix1 stays on
  library PDIP `jit(vmap)`; see "Human decisions (2026-09-25)".
- ~~Gate parameters Δ and the nats pin~~ — CLOSED 2026-09-25: adopted Δ = 100 nats, pin 0.1 nats.
- Rectangular pix2 at prior-phase rates: the guarded batch is slower than PDIP (18.6 vs 17.0).
  Should the guard apply only after the prior phase? This is for C2 to measure and has not been decided.
- Do the catastrophic-lane PDIP disagreements coincide with `converged=False` / `iterations =
  max_iter` (C1 open question 4)? Does one executable re-run on those lanes return identical bits?
- NaN on catastrophic lanes in some compositions only (C1 open question 5): does production care,
  given Fitness resamples non-finite values?

## Design sketched at C1 planning (2026-09-24)

- PyAutoArray: `AbstractInversion.reconstruction` passes a local `stats=` dict to
  `reconstruction_positive_only_from` and keeps it (like `_nnls_factor`); new traced property
  `positive_only_needs_rerun` = `~certified & certified_fallback == "none"` (False for PDIP /
  NumPy / non-mapper).
- PyAutoGalaxy / PyAutoLens: fits expose the flag; dataset analyses implement an opt-in
  `log_likelihood_function_with_aux(instance) -> (log_likelihood, needs_rerun)` (factor
  `AnalysisImaging.log_likelihood_function` body, scalar contract unchanged) and
  `fallback_analysis()` (same analysis, `certified_fallback="pdip"`).
- PyAutoFit: `Fitness._vmap_aux = jit(vmap(call_aux))`, lazily `_fallback_jit`; `call_wrap`
  re-evaluates only flagged lanes host-side and splices; analyses without the hook unchanged.
- No aux channel exists today: `stats=` is a Python dict of traced scalars and the profiling
  harness extracts it via `jax.debug.callback`.
