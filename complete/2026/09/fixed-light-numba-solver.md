# fixed-light-numba-solver — phase 2: fixed lens light on the numba CPU path, and the solver verdict

- Repo: autolens_profiling
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/265 (closed 2026-09-16)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/266 — MERGED, merge commit `c73c86c`
- Epic: `fixed-lens-light-numba-cpu`, phase 2
- Note: `results/notes/fixed_lens_light_numba_2026_09.md` (autolens_profiling)

## What shipped

Phase 2 of the `fixed-lens-light-numba-cpu` campaign: the whole-call measurement of the
fixed-lens-light speedup on the production numba CPU path, plus the solver round it was
authorised to open. Four legs in one SLURM job on an idle RAL host, two corroborating
laptop legs, and a written note; no library edits anywhere.

Code shipped alongside the measurement: the numpy-path solver-injection seam and
factor-reuse NNLS kernel (`scripts/misc/likelihood_breakdown/fixed_light_numpy_solvers.py`),
the `d_np` route and `--nnls-warm-start` flag in
`scripts/imaging/likelihood_breakdown/fixed_light_numba.py`, the solver-kernel cell
`fixed_light_numba_solvers.py`, the four-leg RAL submit script, six result JSON + PNG, and
a repo-wide `--help` fix (a literal `%` in `_profile_cli.py`'s `--memo` help had been
raising `TypeError` on the shared parser for every cell).

## The measurement

**Fixing the lens light is worth 2.03x on the production numba CPU path.** RAL job
**343311** (`euclid-ral-gpu-1`, `gpu` partition CPUs-only, no `--gres`), HST Delaunay
N=1500, sparse numba operator, fp64, one thread (numba 1, BLAS family 1):
`AnalysisImaging.log_likelihood_function` goes from **932 ms** (route a, the joint S0
system the library solves today) to **459 ms** (route b, the source-only S3 system), with
no library change at all; the laptop measures 2.036x independently. Both rows are
memo-off. With the cross-evaluation memo **on**, route b is **405 ms**.

## The solver verdict — the NNLS speed-up round is CLOSED

The factor-reuse NNLS built for this phase is a correct kernel (one factorisation, 15
downdates, equivalent to 1.455e-11 nats) and reaches **1.112x** at whole-call level. The
library's own cross-evaluation memo — **on by default, therefore already in production** —
is **1.134x** by a different mechanism. The two are within 2 % of each other: the memo
already delivers what factor reuse would.

**No PyAutoArray solver prompt is filed.** The conditional `nnls_seed_factor_reuse`
feature prompt this phase was authorised to file is deliberately not filed, and the NNLS
speed-up round is closed.

## The residue, and what comes next

Inside the remaining S3 call the untouched sites are larger than the solver:
`inversion.regularization_matrix` **112 ms**, log-det `F + lambda H` **40 ms**, log-det
`H` **37.5 ms** — about **47 % of the call** — and `log_det_curvature_reg_matrix_term`
re-factorises the very matrix the solver has just factorised.

The next round pairs those numba CPU levers with the A100 non-solver residue: epic
`fixed-lens-light-numba-cpu` **phase 3**, prompt to follow (being intaken as its own
issue). Two further items the note records but does not file here: the memo's behaviour
under bad models over the seeded graded draw set, and the PyAutoArray bug that
`abstract_ndarray.__getitem__` imports `jax.numpy`, so a numba-only process cannot stay
JAX-free after the first `FitImaging`.

## Scope decisions carried

Single-threaded only: production runs one single-threaded numba likelihood per process
under a multiprocessing pool, so per-call multi-core gains were never a target and the
campaign map's thread-scaling phase was retired by that human decision (2026-09-15). The
prompt's `Witness:` line still said "one and eight threads"; it was superseded by that
decision after filing.

## Gates

All structural gates PASS on every leg: P1 sparse-operator re-bake parity (3/3 arrays),
S3 = S0 on the mapper block (log-det terms bit-identical, rel diff exactly 0.0), P2 dense
vs sparse-numba system (max rel diff 3.7e-15), P3 evidence parity (4.6e-15 rel, 0
passive-set differences), P4 injected `d_np` == route b (1.1e-15 rel). Every leg stamps
`timing_status: measured`, `contention_warning: false`, and holds the 1.03 ABBA overhead
gate. CI: `lint` green on head `8388901`.

## Original prompt

# Numba phase 2 — source-only solve on the numba CPU path: measure the fixed-light speedup and make the solver as fast as possible

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- cpu
- numba
- nnls
Difficulty: large
Autonomy: human-required
Priority: high
Status: filed 2026-09-15
Epic: fixed-lens-light-numba-cpu
Phase: 2
Consequence: judge
Witness: On the numba CPU path at HST Delaunay N=1500, every S3 solver row returns the library's own
`fnnls` log evidence to <= 1e-9 relative (or is RECORDED with its Δ in nats where it is a different
minimiser); the decomposition's exclusive rows plus `unattributed` sum to the clean call within 5 %;
and the note carries one table of whole-call ms for S0 -> S3 (library solver) -> S3 (fastest
equivalent solver) in a single-threaded process (numba 1, BLAS 1), with every thread knob recorded per leg.
Review-minutes: 30
Unattended: never
Filed: 2026-09-15
Issued: 2026-09-15
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/265

## Original request (verbatim)

> We recently did work in autolens_profiling which fixed the lens light such that it wasnt solved
> for in the nnls linear algebra, and on an A100 this produced a significant speed up with a new
> solver. I want you to now do the same work but using the numba CPU sparse likelihood function
> approach, basically with the same assumption of source-only solving making the solver as fast as
> possible on CPU. This could include changing the nnls alogirthm. Perform profiling and give me a
> break down of how successful the speed up is.

## Where the campaign stands

Phase 1 (#263, PR #264 merged 2026-09-14) shipped the harness — `fixed_light_numba.py`,
`call_accounting.py`, `fixed_light_system.py` — but **ran no timing leg**: its JSONs carry
`timing_status: wiring_only_not_measured` and no `results/notes/fixed_lens_light_numba_*.md`
exists. This phase runs those legs first, because the decomposition they produce decides what
the solver work below is worth: on the GPU the certified solve fell to 4-11 ms and stopped
being the call; on numba the balance between mapper, `F` assembly and solve is unmeasured.

## What this phase does

1. **Measure the fixed-light speedup on numba.** Run the phase-1 cell on HST Delaunay N=1500,
   routes a / b / c x {dense, sparse_numba}, single-threaded only
   (`NUMBA_NUM_THREADS`, BLAS, `NPROC` all recorded). Route a -> b is the fixed-lens-light
   speedup on the production CPU path; the access-counted decomposition says where the S3
   call now goes (mapper / `F` build / solve / log-dets / unattributed).
2. **Make the S3 solver as fast as possible.** On the S3 `sparse_numba` system, time the
   solver candidates as harness-injected kernels through the existing
   `reconstruction_positive_only_from` injection seam — no PyAutoArray edits:
   - the library `fnnls_cholesky` cold (dense-sign start, memo off) — the reference **b**;
   - `fnnls_cholesky` warm from the cross-evaluation memo on a random-walk instance stream
     (production's actual path) and on an i.i.d. stream (its worst case);
   - the numpy certified active set (`fixed_light_cpu_kernels.numpy_certified_row`);
   - new candidates chosen from the decomposition and the solver's own iteration counts:
     a numba-jitted Bro & de Jong loop with the in-place Cholesky kernels (removes the
     per-iteration Python overhead and the O(n^2) `ZTZ @ d` gradient rebuild), block pivoting
     for the cold path, and whatever the measured iteration/factorisation counts single out.
   Every row carries ms, outer/inner iterations, factorisation count, the equivalence pin
   against **b** and the thread block.
3. **Score the whole call with the fastest equivalent solver injected**, so the headline is
   a -> b -> best in whole-call milliseconds, not a kernel millisecond.
4. **Write the verdict note** `results/notes/fixed_lens_light_numba_2026_09.md` in the format
   of the six GPU notes: provenance and gate table, decomposition table, solver table, the
   speedup breakdown, a "read this before quoting a number" scope section, and a verdict on
   whether a solver change is worth carrying into PyAutoArray (filed as its own feature prompt
   if so — this phase edits no library).

## Scope and guards

**Single-threaded only (human, 2026-09-15).** Production parallelises the numba likelihood
across cores with Python multiprocessing, one single-threaded evaluation per process, so no
multi-core per-call speedup is a target: every leg runs at `NUMBA_NUM_THREADS=1` and BLAS 1,
and the campaign map's thread-scaling phase is retired.

HST, fp64, Delaunay N=1500 first; rectangular only if the Delaunay legs leave time. Euclid,
the source-pixel sweep and the graded draw set stay in phases 3-5. The thread guard from the
campaign map holds: no comparison crosses a thread setting silently. Positivity is never
dropped in a quoted headline; route c stays a scored diagnostic. Phase 1's leftover worktree
`~/Code/PyAutoLabs-wt/fixed-light-numba-phase1` and its `active.md` row are closed out as
part of this phase's setup.

## Execution

Planned and judged by a Fable session; all execution delegated to Opus subagents with a
progress heartbeat. Legs run one at a time on a quiet laptop.
