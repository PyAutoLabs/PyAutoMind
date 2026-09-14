# Fixed lens light on the numba CPU path — the whole programme again, off the GPU

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- cpu
- numba
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — the phases route through /start_dev ONE at a time, in order; this file is never issued itself and nothing here is bulk-issued
Epic: fixed-lens-light-numba-cpu
Consequence: judge
Witness: On the numba CPU path at HST Delaunay N=1500, the measured decomposition of the whole
likelihood call sums to the measured call to within 5 %, and every S3 route returns the library's
own log likelihood to <= 1e-9 relative (the GPU epic's equivalence pins, re-asserted on numba).
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-14

The `fixed-lens-light-profiling` epic is COMPLETE (six phases, merged 2026-09-14,
verdict `results/notes/fixed_lens_light_verdict_2026_09.md`). It settled the GPU: fix the
lens light, solve only the source, use the certified active set at pass budget 7 on
Delaunay with a PDIP fallback, fp64, and never drop positivity. On an A100 that is
65.10 -> 25.39 ms on Delaunay at HST N=1500, at the library's own answer to 1e-10.

That whole programme ran on JAX. Every CPU row in it is **JAX-CPU** or a **numpy**
kernel. The production CPU path in PyAutoArray is **numba**, and it was never measured.
This campaign runs the same six-phase programme again on the numba path.

## Why this is an open question and not a port

Phase 2 (`complete/2026/09/fixed-light-hardware.md`) measured the one CPU row that
exists and it went the other way:

- the numpy certified active set **does not beat** the library's own `fnnls` NNLS;
- both are **1.9-3.6x slower at 8 BLAS threads than at 1**;
- the a -> d prize shrinks monotonically with the hardware: 2.03x/2.56x/2.01x on the
  A100, 1.28x/1.48x/1.46x on an RTX 2060, 1.16-1.22x on one CPU thread.

The reason is phase 1's finding, which is the through-line of the whole epic: once the
solve is 4-11 ms **it is no longer the call**. ~21 ms of the 25.39 ms certified Delaunay
A100 call is mesh, mapper and assembly. The slower the device, the more that residue
dominates and the less a better solver is worth. On numba, where the assembly and mapper
are jitted loops rather than BLAS, the balance could land anywhere — and nobody has
looked.

So the question this campaign answers is not "does the GPU result port" but:
**on the numba CPU path, where does the likelihood actually spend its time, and is
fixing the lens light plus a certified active set worth anything at all?**

## The phases — mirror the GPU epic, one at a time, in order

Each phase's grid is chosen from the previous phase's answer. Issue ONE at a time; never
bulk-issue. File each phase's own prompt when the campaign reaches it.

**Amended 2026-09-14, before phase 1 was issued.** Two changes, both consequences of the
GPU epic's own findings rather than of anything measured here yet:

1. **The original phase 0 (numba kernel measurement) is folded into phase 1.** GPU phase 2
   already measured the CPU kernel rows and concluded, in its own words, that a CPU
   assessment "should score the library's `fnnls` path, not the certified active set". A
   numba kernel phase would re-answer a settled question and delay the decomposition this
   campaign's `Witness:` demands. The campaign is five phases, numbered 1-5.
2. **Phase 3 is repurposed.** It was premised on the certified active set's pass budgets —
   but the certified scheme is not what CPU scores, so "do the GPU's budgets 7 / 11 hold on
   numba?" is not a question this campaign can ask. The numba equivalent is better: the
   library's `fnnls` is seeded from a passive-set **memo**, so does that warm start survive
   low-likelihood draws, or does it fall back and cost what a cold solve costs?

| # | Phase | Mirrors | Prompt |
|---|---|---|---|
| 1 | The whole `AnalysisImaging.log_likelihood_function` on the numba path, routes a/b/c x {dense, numba-sparse}, with a decomposition measured in ONE process and a sparse-operator parity pin | GPU phases 0+1 (#248, #251) | `fixed_light_numba_phase1_whole_call.md` — ISSUED 2026-09-14 |
| 2 | Thread scaling: 1 / 2 / 4 / 8 threads, and the numba-vs-BLAS thread interaction GPU phase 2 flagged (both CPU solvers ran 1.9-3.6x SLOWER at 8 BLAS threads than at 1) | GPU phase 2 (#253) | — |
| 3 | The `fnnls` memo warm start over the seeded 41-model graded draw set: `seed_source`, `warm_start_fallback`, outer/inner iteration counts — does the warm start hold when the model is bad? | GPU phase 3 (#255), repurposed | — |
| 4 | Source-pixel scaling, and which term overtakes which as N grows | GPU phase 4 (#257) | — |
| 5 | HST + Euclid verdict: the production CPU configuration per core count | GPU phase 5 (#259) | — |

## What must be carried across, and what must not

**Carries.** The library subsets `F + lambda*H` and `D` to `solve_ids_to_keep` *before*
calling its positive-only solver (`abstract.py:607-618`) — the solver sees n=1369, not
1521, on rectangular. The positivity prohibition carries and is stronger than the GPU
knew: +109.1 nats on Euclid at N=2500, and the trend with N reverses between HST and
Euclid. Dense inversion only.

**Does not carry.** The `lax.cond`-becomes-`select`-under-`vmap` trap is a JAX
constraint and is meaningless here — but numba has its own, and phase 1 should name
them rather than assume there are none. The GPU's batching story (`@vmap 16`) has no
numba counterpart. Mixed precision is not a numba question.

**Out of scope throughout**, as in the GPU epic: JWST, and the sparse operator (blocked
on `draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`).

**Guard the thread count.** Phase 2 measured both CPU solvers running 1.9-3.6x SLOWER
at 8 BLAS threads than at 1. Every leg must record its thread settings (`NPROC`, BLAS,
numba's own) and no comparison may cross them silently.

## Execution

This is a Fable / Astra campaign: a top-tier session plans and decomposes each phase and
judges its results, delegating execution. Every phase is a measurement with a written
verdict note under `results/notes/`, pins recorded where no pin exists, and a provenance
and gate table — the GPU epic's six notes are the format to match.
