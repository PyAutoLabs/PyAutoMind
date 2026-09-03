## numba-vs-jax-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/513 (closed, completed 2026-09-01T19:39:28Z)
- completed: 2026-09-01
- library-pr: none by design — a research verdict, no code shipped
- verdict: https://github.com/PyAutoLabs/PyAutoArray/issues/513#issuecomment-5483142802
- batch: 2026-08-31-pm — member `numba-vs-jax-sparse`, tier `judge`, 20 review-minutes; `--auto`, effective level supervised (= min(header safe, research work-type cap)); parked at verdict per the research cap. `batches/reviews/2026-08-31-pm.md` records `decision: UNREVIEWED`
- shipped: the verdict — **"same linear algebra, deliberately different machines; keep
  both, port nothing."** The numba CPU positive-only solve (the #498/#501 warm-start
  memo, the #505/#507 curvature-F work, the `SparseLinAlgImagingNumba` preload) and the
  JAX `ImagingSparseOperator` + `jaxnnls` PDIP path compute the same object by different
  machinery, each tuned to its own hardware; the numba levers do not carry to GPU and
  unifying them would cost both paths their tuning.
- verified: no code changed, so no test/smoke gate ran — the deliverable is the written
  verdict on the issue, and the review *is* the judgement. The `--auto` research cap held
  exactly as designed: the run parked for a human rather than shipping a decision
  unattended.
- traps: a judge-tier research member produces no PR, so nothing in the merge machinery
  ever retires its `active.md` row — this row sat in `awaiting-input` for two days after
  the issue was closed. Research verdicts need an explicit close-out; a green PR does not
  stand in for one.
- notes: **Ledger reconciliation 2026-09-03** — issue closed as completed 2026-09-01,
  `active.md` row never retired. Written by `mind-post-cortex` phase 1 (PyAutoMind#389).
  The `research` autonomy cap is explicitly out of scope for the `mind-post-cortex`
  epic — it stays, and this is the live example the epic ledger cites.

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
