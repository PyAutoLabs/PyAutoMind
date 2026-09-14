# The non-solver residue — optimise the HST GPU likelihood breakdown around the certified solve

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- hpc-gpu
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — the phases route through /start_dev ONE at a time, in order; this file is never issued itself and nothing here is bulk-issued
Epic: hst-gpu-non-solver-residue
Consequence: judge
Witness: A measured (not attributed) decomposition of the certified Delaunay A100 call at HST
N=1500 whose terms sum to the measured 25.4 ms within 5 %; and any optimisation landed returns
the library's own log likelihood to <= 1e-9 relative, asserted on every fp64 leg.
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-14

The `fixed-lens-light-profiling` epic is COMPLETE and it ended by naming its own successor.
Every one of its six phases optimised **positivity**. Having done so, the solve stopped being
the call:

| Term, certified Delaunay route, A100 fp64, HST N=1500 | ms |
|---|---:|
| whole `AnalysisImaging.log_likelihood_function` | **25.39** |
| the certified active-set solve | 4.21 |
| curvature + regularization build (`F + lambda*H`) | 4.92 |
| `log det(F + lambda*H)` | 1.17 |
| `log det(H)` | 1.20 |
| **unattributed — mesh construction, the mapper and its weights, imaging, blurring** | **~13.9** |

**~21 of the 25.4 ms is not the solver**, and on DelaunayNN it is ~32 of 36 ms (69 % of the
call). Phase 4 sharpened it: on the A100 every solver row fits alpha ~ 1 (launch- and
bandwidth-bound) while the dense `F + lambda*H` build fits **alpha ~ 1.69 and overtakes the
certified solve between 2500 and 4000 source pixels**. Another factor of two on the solver
buys ~2 ms. This campaign goes after the other 21.

## Phase 1 is a measurement, not an optimisation — do not skip it

The 13.9 ms above **is not a measured number**. It is phase 1's attribution: phase-0 kernel
rows (a different cell, a different process) subtracted from phase-1 library calls, and that
note flags it as arithmetic rather than a decomposition. Optimising against a subtraction is
how a campaign spends a month on the wrong term.

The first deliverable is therefore a **cell that times the real call's internals in one
process** — mesh construction, mapper and mapping-matrix build, the mapper weights, the
over-sampled image and blurring, the `Lambda^T N^-1 Lambda` assembly, both log-dets and the
solve — summing to the measured call within a few per cent, on the A100 in fp64, HST,
Delaunay at the production budget 7. Only then does the campaign know which term to attack.

Carry the warning from a sibling programme: fusing calls moves work between `--split-setup`
prefix rows, so judge on the params -> H prefix rather than on a single row's ms.

## The levers, in the order the evidence ranks them

1. **The Delaunay mesh, the mapper and its weights** — the largest term and the least
   examined. Mesh construction is per-call because the source-plane grid moves with the mass
   model; what part of it genuinely must be?
2. **The dense `F + lambda*H` assembly** — alpha ~ 1.69, overtaking the solve above N ~ 2500,
   so it is the term that decides the affordable N ceiling (4000 on an A100 today).
3. **The two log-dets** — 2.4 ms together, small but Cholesky-bound; the matrix-free CG+SLQ
   work (`results/notes/matrix_free_pixelized_2026_09.md`, #247) already circled this and
   deferred it because the log-det needs a Cholesky. Re-read that verdict before re-opening it.

## Constraints — this campaign may not change the answer

- **fp64, budget 7 on Delaunay, PDIP fallback, positivity never dropped.** Those are the GPU
  verdict's settled conclusions and this campaign inherits them; it is optimising the terms
  *around* a solver whose configuration is decided.
- **Every optimisation carries an equivalence pin** against the library's current answer at
  <= 1e-9 relative, asserted on every fp64 leg — the standard all six phases of the previous
  epic met.
- **HST and the A100 first.** Euclid costs 2.1-2.6x less than HST at equal N on every
  hardware measured, so HST is the harder case; the Euclid column follows once a lever lands.
- The certified solver is still a **harness monkeypatch**; no library implementation exists.
  This campaign must say, per lever, whether it is a harness experiment or a real
  PyAutoArray change, and land no silent library edit.

## Known traps that bear on these terms

- `reg_adapt` cannot jit on the Delaunay family — relevant, since `adapt_split` is the
  Delaunay cell's shipped default regularization.
- A non-uniform over-sample map **triples** jit compile time; the over-sampling of the image
  term is inside the residue this campaign is measuring.
- The JAX/GPU pixelized route fits the plain dataset and never applies the sparse operator;
  the sparse path is CPU-only and out of scope here (and blocked on the PyAutoArray
  weight-map bug).

## Execution

A Fable / Astra campaign: a top-tier session plans each phase, judges the results and
delegates execution. Every phase ends in a `results/notes/` verdict note with a provenance
and gate table, in the format the six fixed-lens-light notes set. A100 phases have a
submit -> wait -> harvest step, which is a human resume point, not a park.
