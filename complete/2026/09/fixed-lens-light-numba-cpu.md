## fixed-lens-light-numba-cpu
- completed: 2026-09-18
- summary: CPU fixed-lens-light campaign closed at the user's request. Phases1–6, including4b and5b, completed; phase7 explicitly shelved. No further benchmark or memo-policy work is required by this epic.
- final-workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/277
- scaling-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/283

## High-level findings

1. Fixed lens light/source-only likelihood:932→459ms (2.03x) on the measured HST DelaunayN1500 single-thread numba CPU cell, both memo-off. This changes what is held fixed; apply only when the modelling workflow permits it, and account for light preparation separately.
2. Three library optimizations shipped: compiled split-regularization assembly, sparse regularization log-determinant, and reuse of the NNLS factor plus cached curvature+regularization matrix. Phase3 whole call413.3→230.0ms (1.80x) in its memo-on HST fixture. Preserve that scope; do not multiply this with phase2 into a universal speedup. A100 controls were unchanged.
3. Further curvature-kernel and permutation prototypes did not justify promotion. Phase4b226.772ms production versus228.576ms permuted. Retain the current positive-only solver and kernel.
4. Memo can help nearby calls but hurt broad draws; residual precheck was NO_LEVER. User decision: assume no usable memo benefit under changing sampler order for current planning, shelve phase7; production defaults remain unchanged.
5. Larger source systems become NNLS-dominated. Phase6 cold nearby/broad: N1500 0.275/0.436s; N2500 0.710/1.429s; N4000 2.138/4.312s. AtN4000 NNLS is ~81%/~88% of cold whole-call time. These are conditional source-only synthetic-sequence measurements, not sampler throughput predictions.

## Recommendation

Use the tested fp64 numba `_sparse` imaging assembly with positive-only NNLS and one BLAS/Numba thread per likelihood process. Use independent processes for throughput within a measured memory budget. Keep merged regularization/determinant improvements; no new solver or memo policy is warranted by this campaign. Treat memo speed benefit as zero in budgeting. Fix lens light only where scientifically justified. Select source resolution by reconstruction fidelity, then budget using cold timings; reducing pixels was not validated as scientifically equivalent.

Stop this optimization campaign. If later production profiles demonstrate a remaining large-N bottleneck, scope solver work as a separate measured task. Euclid-wide recommendations and full sampler speedups were not established because phase7 was shelved.

## Completion evidence and retained obligations

Phase records: fixed-light-numba-phase1, fixed-light-numba-solver,
fixed-light-numba-levers, fixed-light-numba-s4, fixed-light-numba-s4b,
fixed-light-numba-s5, fixed-light-numba-s5b, fixed-light-numba-s6 under complete/2026/09/.
Phase7 proposal remains complete/archive/shelved/fixed_light_numba_s7_cpu_verdict.md.
Numerical tests, raw timings, plots and source/job provenance are committed in autolens_profiling.

Library release obligations remain owned by the phase3 completion record (PyAutoArray#553/#554/#555). Closing this epic does not clear those pending-release entries, declare Heart healthy, authorize a release or close unrelated GPU work. The standalone operated-mapping-matrix harness issue is a different cache and remains separate. Retained worktrees/data need their own explicit cleanup approval; they do not keep the research epic active.

## Original prompt

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
   campaign's `Witness:` demands. The campaign was five phases at that point; it is **six**,
   numbered 1-6, since the 2026-09-16 amendment below inserted the non-solver levers as phase 3.
2. **Phase 3 is repurposed** (that repurposed phase is **now phase 4**, per the 2026-09-16 amendment).
   It was premised on the certified active set's pass budgets —
   but the certified scheme is not what CPU scores, so "do the GPU's budgets 7 / 11 hold on
   numba?" is not a question this campaign can ask. The numba equivalent is better: the
   library's `fnnls` is seeded from a passive-set **memo**, so does that warm start survive
   low-likelihood draws, or does it fall back and cost what a cold solve costs?

| # | Phase | Mirrors | Prompt |
|---|---|---|---|
| 1 | The whole `AnalysisImaging.log_likelihood_function` on the numba path, routes a/b/c x {dense, numba-sparse}, with a decomposition measured in ONE process and a sparse-operator parity pin | GPU phases 0+1 (#248, #251) | `fixed_light_numba_phase1_whole_call.md` — COMPLETE 2026-09-14 (#263, PR #264: harness shipped, timing legs NOT run; carried by phase 2) |
| 2 | Source-only solver speed on the numba path: run phase 1's legs, then make the S3 `fnnls` solve as fast as possible (factorisation count, not the active-set scheme) and score the whole call with it. **Single-threaded only** — production runs one single-threaded likelihood per process under multiprocessing, so the original thread-scaling phase is RETIRED (human decision 2026-09-15) | GPU phases 1+2 (#251, #253) | `fixed_light_numba_phase2_source_only_solver.md` — COMPLETE 2026-09-16 (#265, PR #266). Verdict `results/notes/fixed_lens_light_numba_2026_09.md`: headline **2.03x**, **no solver change proposed** |
| 3 | The non-solver levers (split-regularization assembly, the regularization log-det, the shared `F + lambda*H` Cholesky) on numba CPU, each paired with an A100 row | `hst-gpu-non-solver-residue` levers 2+3 | `fixed_light_numba_s3_regularization_logdet_levers.md` — COMPLETE 2026-09-16 (#267; PyAutoArray #553/#554/#555 + autolens_profiling #272; record `complete/2026/09/fixed-light-numba-levers.md`). Verdict `results/notes/fixed_lens_light_levers_2026_09.md`: **1.80x** cumulative, levers 2+3 CPU-only |
| 4 | The curvature-matrix kernel A/B on Delaunay (two-stage vs direct, touched-index stage 2), then A-prime permute-active-last; cell overhead-cap fix first — **4a done (no lever, `complete/2026/09/fixed-light-numba-s4.md`); 4b re-filed as `fixed_light_numba_s4b_permute_active_last.md`** | phase 3's residue (note Next items 1, 6) | `fixed_light_numba_s4_curvature_kernel_ab_and_permute_active_last.md` — FILED 2026-09-16 |
| 5 | The `fnnls` memo warm start over the seeded 41-model graded draw set: `seed_source`, `warm_start_fallback`, outer/inner iteration counts — does the warm start hold when the model is bad? | GPU phase 3 (#255), repurposed | — |
| 6 | Source-pixel scaling, and which term overtakes which as N grows | GPU phase 4 (#257) | — |
| 7 | HST + Euclid verdict: the production single-threaded CPU configuration | GPU phase 5 (#259) | — |

**Amended 2026-09-16, when phase 2 completed.** Phase 2's verdict named the residue as bigger
than the solver, and the human asked for the follow-up round to be paired with the A100. Three
records:

1. **Phase 3 is now the non-solver levers**, filed as
   `fixed_light_numba_s3_regularization_logdet_levers.md`, and the old phases 3, 4 and 5 renumber
   to 4, 5 and 6. The **NNLS round is CLOSED**: the library's cross-evaluation memo (ON by
   default, 1.134x) already delivers what phase 2's factor-reuse kernel reached (1.112x), so the
   conditional PyAutoArray `nnls_seed_factor_reuse` prompt was deliberately **not** filed.
2. **The phase-2 note's "Next" item 1 was never realised as written.**
   `results/notes/fixed_lens_light_numba_2026_09.md` says the work was "filed as
   `PyAutoMind/draft/research/autolens_profiling/fixed_light_numba_s3_regularization_logdet_levers.md`";
   no such file existed until 2026-09-16. **Phase 3's prompt is it** — under that exact name, and
   widened, because item 1 named only the regularization matrix and the log-det factor reuse and
   did not carry the A100 pairing.
3. **Two loose ends phase 2 recorded and did not file**, kept here so they are not lost:
   - the PyAutoArray bug that `abstract_ndarray.__getitem__` imports `jax.numpy`, so a numba-only
     process cannot stay JAX-free after the first `FitImaging` (recorded as `jax_after_rows` in
     every phase-2 JSON) — **unfiled**;
   - the deliberate non-filing of `nnls_seed_factor_reuse` (phase-2 verdict 3) — **a decision,
     not an omission**; reopening it needs a new measurement, not this campaign.

**Amended again 2026-09-16, when phase 3 completed:** phase 4 is the kernel A/B + A-prime round; the memo, scaling and verdict phases renumber to 5, 6 and 7.

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

## Status update — 2026-09-18

Phase 5 (#278, PR #279) and the phase-5b residual-policy follow-up (#280, PR #281)
are merged; records `complete/2026/09/fixed-light-numba-s5.md` and
`complete/2026/09/fixed-light-numba-s5b.md`. The precheck was NO_LEVER; production
memo defaults remain unchanged. Phase 6 (#282, PR #283) is merged; record
`complete/2026/09/fixed-light-numba-s6.md`. All N500/1000/1500/2500/4000 cells PASS.
NNLS dominates larger systems: at N4000 nearby cold/memo2.138/1.289s, broad4.312/10.783s.
The scaling verdict supports investigating the solver and proposal-dependent memo behavior;
it does not establish a global memo default. Phase 7 remains unfiled: HST + Euclid
with representative proposal histories, preserving the numerical and thread gates.

## Phase 7 shelved — user decision, 2026-09-18

The user deferred phase7: assume no usable memo benefit and changing sampler
order for current planning; further memo policy/order/history work is out of
scope. Preserve the completed research and leave production memo defaults
unchanged. The unissued proposal is archived at
`complete/archive/shelved/fixed_light_numba_s7_cpu_verdict.md`; it is not an
active or pickable next task. Reopen only on explicit user request with a fresh
scope. Earlier statements describing phase7 as next are superseded here.

## Retired epic registry entry (historical)

## fixed-lens-light-numba-cpu
- title: Fixed lens light on the numba CPU path — the whole programme again, off the GPU
- ledger: draft/research/autolens_profiling/fixed_light_numba_cpu_programme.md
- notes: successor to `fixed-lens-light-profiling` (COMPLETE 2026-09-14), filed the same day. Six phases mirroring that epic, worked strictly 1 → 2 → 3 → 4 → 5 → 6 — each phase's grid is chosen from the previous phase's answer; issue ONE at a time, never bulk-issued, and file each phase's own prompt when the campaign reaches it. The open question is real, not a port: phase 2 of the GPU epic found the numpy certified active set does NOT beat the library's own `fnnls`, and both run 1.9-3.6x slower at 8 BLAS threads than at 1 — and the numba production path was never measured at all. Every leg must record its thread settings (`NPROC`, BLAS, numba) and no comparison may cross them silently. Out of scope throughout, as in the GPU epic: JWST and the sparse operator (blocked on `draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`). A Fable / Astra campaign.
  Phase 1 COMPLETE 2026-09-14 (#263, PR #264 — harness shipped, timing legs carried by phase 2).
  Phase 2 COMPLETE 2026-09-16 (#265, PR #266): fixed lens light measures **2.03x** on the
  production numba CPU path (RAL job 343311, HST Delaunay N=1500, 1 thread, 932 -> 459 ms;
  405 ms with the memo on). The **NNLS speed-up round is CLOSED** — the library's memo (ON by
  default, 1.134x) already delivers what the factor-reuse kernel would (1.112x), so the
  conditional PyAutoArray `nnls_seed_factor_reuse` prompt is deliberately NOT filed. The
  residue is `regularization_matrix` 112 ms + log-det `F + lambda H` 40 ms + log-det `H`
  37.5 ms (47 % of the call).
  Phase 3 COMPLETE 2026-09-16 (#267; PyAutoArray #553/#554/#555 merged pending-release,
  autolens_profiling #272 merged carrying #269/#271; record
  complete/2026/09/fixed-light-numba-levers.md): three non-solver levers on numba CPU
  **413.3 → 230.0 ms = 1.80x** (1.38x split-reg numba kernels / 1.13x sparse log det H,
  CPU-only / 1.19x log det(F+λH) off the NNLS factor + cached curvature_reg_matrix), A100
  identity on every lever. Residue curvature_matrix 88 ms + fnnls 61 ms ≈ 65 %; lever 4
  candidates (A′ permute-active-last, edge-zeroed, covariance third factorisation) in the
  note's Next, not filed. Old phases 3-5 renumbered to 4-6 stood until phase 4 was filed;
  see below.
  Phase 4 FILED 2026-09-16 — the curvature-matrix kernel A/B on Delaunay (lever 4a,
  measurement first: the two-stage vs direct kernels were never measured on the Delaunay
  fixed-light cell; touched-index stage 2 if neither wins) then A-prime permute-active-last
  (lever 4b, witness design first); cell prerequisite: the 1.03 overhead cap (wave A /
  lever 4a done 2026-09-17 — no lever, record `complete/2026/09/fixed-light-numba-s4.md`;
  wave B / lever 4b prompt
  `draft/research/autolens_profiling/fixed_light_numba_s4b_permute_active_last.md`).
  Inserts ahead of the old phases 4-6, which renumber to 5 (memo warm start), 6 (source-pixel
  scaling), 7 (HST + Euclid verdict).
  Phase 5 and 5b COMPLETE 2026-09-18 (#278/#280, PRs #279/#281 merged): memo helps nearby
  proposals but can be slower on broad draws; residual precheck NO_LEVER, no production policy
  change. Phase 6 COMPLETE (#282, PR #283 merged; `complete/2026/09/fixed-light-numba-s6.md`):
  N500–4000 scaling, all five cells PASS. NNLS dominates large N; at N4000 memo saves
  39.7% nearby but costs 2.50x cold for broad draws. No production policy change.
  Phase 7 SHELVED by user 2026-09-18: assume no usable memo benefit and changing
  sampler order for current planning; further memo/order studies out of scope.
  Production defaults unchanged. Proposal: `complete/archive/shelved/fixed_light_numba_s7_cpu_verdict.md`.

