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
equivalent solver) at one and eight threads, with every thread knob recorded per leg.
Review-minutes: 30
Unattended: never
Filed: 2026-09-15

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
   routes a / b / c x {dense, sparse_numba}, at one and eight threads
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

HST, fp64, Delaunay N=1500 first; rectangular only if the Delaunay legs leave time. Euclid,
the source-pixel sweep and the graded draw set stay in phases 3-5. The thread guard from the
campaign map holds: no comparison crosses a thread setting silently. Positivity is never
dropped in a quoted headline; route c stays a scored diagnostic. Phase 1's leftover worktree
`~/Code/PyAutoLabs-wt/fixed-light-numba-phase1` and its `active.md` row are closed out as
part of this phase's setup.

## Execution

Planned and judged by a Fable session; all execution delegated to Opus subagents with a
progress heartbeat. Legs run one at a time on a quiet laptop.
