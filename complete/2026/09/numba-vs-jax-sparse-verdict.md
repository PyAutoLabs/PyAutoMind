- shipped: 2026-09-01 — verdict of record on
  https://github.com/PyAutoLabs/PyAutoArray/issues/513 (closed on acceptance); no PR by
  design (research, no library changes).
- classification: research (PyAutoArray) — batch 2026-08-31-pm member numba-vs-jax-sparse;
  also the numba-cpu-likelihood epic's post-completion next step (successor curvature-F
  work already shipped as PyAutoArray#505/#507).
- summary: the numba CPU positive-only solve and the JAX sparse-operator mode solve the
  identical regularised normal equations but realise them differently at every layer, each
  difference deliberate for its hardware: explicit 177 MB sparse preload + branchy
  active-set fnnls + cross-evaluation warm-start memo (CPU cache/state levers) vs
  matrix-free FFT operator + fixed-shape PDIP with a differentiable relaxed-KKT VJP
  (GPU/vmap/grad levers). Every transplant was already measured and failed (warm-start
  hurts PDIP 17→38 iterations; BPP/ADMM slower/fail). VERDICT: keep two deliberately
  different paths — no port, no unification. Two scholar-mode candidates left unfiled
  (a two-modes design note; landing/retiring the solver ledger's pending A100 rows).
- lifecycle: dispatched 18:53Z as an unattended batch member (parked for judgement per the
  judge tier); verdict accepted in the 2026-09-01 15:13 batch review; recorded 2026-09-01.

## Original prompt

# Is the numba positive-only solve the same linear algebra as the JAX sparse-operator mode?

Type: research
Target: autoarray
Repos:
- PyAutoArray
Themes:
- numba-cpu
- jax
Difficulty: medium
Autonomy: safe
Priority: normal
Status: issued
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-31
Issued: 2026-08-31

Intake from the 2026-08-31-am batch review, prompted by the subhalo_validation
end-to-end runs (numba CPU path ~x8 faster than the old code end to end). Human,
verbatim:

"""
1) End to end runs are good in general, with numba speed up run times roughly x8
faster than old code, incredible. Do an intake to investigate if the linear algebra
approach taken for this is the same as the sparse operator mode alreasdy implemented
for JAX, and if it is not ask whether it is amenable to GPU JAX speed up or if there
is some sparsity exploitation that means this is suited to CPU.
"""

Deliverable is a written verdict (no library changes):

1. Characterise the linear algebra of the numba CPU positive-only solve as shipped
   (the NNLS warm-start/memo lineage — PyAutoArray #501, epic `numba-cpu-likelihood`;
   curvature-matrix F work #505/#507; the 177 MB sparse operator per process).
2. Compare against the sparse-operator mode already implemented for JAX: same
   formulation (operator storage, curvature assembly, solve strategy) or different?
3. If different: is the numba approach amenable to a GPU-JAX port (batched/dense
   enough, no data-dependent control flow), or does its speed rest on sparsity
   exploitation / branchy active-set iteration that is intrinsically CPU-suited?
4. Verdict + recommendation: unify, port, or keep two deliberately different paths —
   with the evidence for whichever it is.

Ground against the installed stack and the numba-cpu epic's memory/notes; do not
re-profile from scratch — the breakdown JSONs and `nnls_warm_start_memo.md` in
autolens_profiling already carry the numbers.
