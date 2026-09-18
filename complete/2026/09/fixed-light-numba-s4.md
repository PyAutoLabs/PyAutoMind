# fixed-light-numba-s4 — phase 4 wave A: lever 4a, the curvature-kernel A/B on Delaunay (no lever)

- Repo: autolens_profiling
- Repo: PyAutoArray
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/274 (closed 2026-09-17)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/275 — MERGED, merge commit `92f1fadd`
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/557 — MERGED, merge commit `192d4b70` (docstring-only)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/557
- Epic: `fixed-lens-light-numba-cpu`, phase 4 — **wave A only**; wave B (lever 4b, A′) re-filed as `draft/research/autolens_profiling/fixed_light_numba_s4b_permute_active_last.md`
- Note: `results/notes/fixed_lens_light_s4_2026_09.md` (autolens_profiling)
- RAL: job 343394 (`fl_numba_s4`, `gpu` CPUs-only, euclid-ral-gpu-1, COMPLETED 0:0, 00:02:42)
- completed: 2026-09-17

## What shipped

Lever 4a was a measurement, not a rewrite: the two curvature-matrix kernels that already exist behind
`curvature_matrix_via_sparse_operator_from` (two-stage, the production branch at N ≤ 4096; the direct
quadruple loop) plus a prototyped touched-index two-stage variant, A/B'd **in one process against one
installed library** on the HST Delaunay N=1500 fixed-light cell (route b, memo ON, one thread, `--n-repeats 64`,
ABBA harness). Before the measurement the cell's instrumentation-overhead gate was restated from a ratio
(`1.03`, which killed job 343355 at 224 ms) to a millisecond budget (`MAX_INSTRUMENTATION_OVERHEAD_MS = 12.0`,
ratio still recorded).

**Verdict under the rule written before the run (lever iff ≥ 5 % faster on the whole call with ABBA PASS):
no lever — both candidates are slower.**

| row | whole call (ms) | vs `b` | ABBA overhead | site `sparse_numba.curvature_matrix` (ms) |
|---|---:|---:|---|---:|
| `b` two-stage (production) | 230.149 | — | −1.13 ms ×0.9951 PASS | 87.740 |
| `b_direct` | 244.924 | +14.775, +6.42 % | −1.62 ms ×0.9934 PASS | 105.690 |
| `b_touched` | 236.913 | +6.765, +2.94 % | +0.02 ms ×1.0001 PASS | 100.547 |

Witness PASS in the same job: W1 one kernel call per `figure_of_merit`; W2 direct vs two-stage max rel
4.100e-13, touched **bit-identical**, control == un-injected dispatcher; W3 log evidence rel 7.385e-16 (direct),
0.0 (touched); W4 site medians of 20: two_stage 85.043 ms, direct 102.052 (0.83×), touched 97.019 (0.88×).
So **two-stage is right on Delaunay too** (u0 = 1.604), and the two-stage docstring's own prediction that it loses
for narrow barycentric mappings is refuted at this cell. Control `b` reproduces lever 3's 230.031 ms at +0.05 %
across jobs and days on the same node; the campaign chain **413.301 → 230.031 ms** is unchanged (wave A adds 0).

**autolens_profiling (#275, 8 commits):** overhead gate as an ms budget + its tests; `fixed_light_numpy_kernels.py`
(`curvature_kernel_injected` seam, three kernels); routes `b_direct` / `b_touched`; `fixed_light_numba_s4_witness.py`
(W1–W4); `hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_s4_delaunay_ral_hst_fp64` with a WALL-BASIS
block; `test_fixed_light_s4.py`; the job 343394 artefacts; the note.
**PyAutoArray (#557):** the two-stage kernel's docstring corrected — dispatch is on `pix_pixels` against
`CURVATURE_TWO_STAGE_MAX_PIX_PIXELS` (the named `CURVATURE_TWO_STAGE_COST_RATIO_THRESHOLD` never existed), and
the refuted Delaunay sentence replaced by the measurement. No kernel or dispatch change: nothing in the
measurement supports moving the cap.

## Traps and notes

- **WALL-BASIS overestimate.** The submit's block estimated 7200 s from job 343356's two-arm shape; the
  one-arm job took 162 s. Re-pin (`wall: 250 ref: RAL-job-343394`) is a follow-up — the submit text was not
  edited because the recorded run depends on it.
- **Laptop vs RAL W4** agree on the winner only; the ranking of the two losers is host-dependent (laptop:
  touched worst; RAL: direct worst). Only "two-stage fastest, both candidates lose on both hosts" is portable.
- **Why touched loses although it does strictly less arithmetic:** a 1500-long fp64 AXPY is 12 KB and
  L1-resident; maintaining the touched-index list is itself a data-dependent scatter and the gather it enables
  replaces a contiguous vectorised AXPY with an indexed one.
- **Heart gate at ship:** RED with exactly `install verification FAILED (testpypi; checks F)` and
  `release validation FAILED (stage integrate)` (released Colab bootstrap, unrelated); shipped to PR-open on the
  human's instruction naming those two; two transient `N commit(s) behind origin` reasons were local staleness
  (ff-pull of canonical PyAutoFit/PyAutoArray + vitals tick). Merged via `/prm` with "i authorize anything
  required"; every leg was green (autolens_profiling lint; PyAutoArray unittest 3.12 / 3.13 / nojax).
- **RAL worktree cannot push** (no GitHub credential on the cluster): the harvest commit was fetched over
  ssh (`git fetch euclid_jump:<wt> <branch>`) and fast-forwarded locally. `git worktree add` over the slow
  `/mnt/ral` mount outlives an ssh call — run it under `nohup` and poll the artefact, and never check its
  liveness with `pgrep -f` (it matches the ssh wrapper).
- **`pkill -f`/`pgrep -f` on a command-line substring** matched the caller's own shell twice this session.
- **The dashboard scanner** only versions `_v<version>` artefacts: no lever-family artefact (levers 1–4a) has a
  README row, so `build_readme.py` producing no diff is expected, not a miss.
- Local `black` 25.1.0 disagrees with the version that formatted PyAutoArray `main` on an unrelated line of
  `inversion_imaging_numba_util.py`; #557 left it alone.
- `test_fixed_light_numba.py`'s `injected_kernel.n_calls` differs between injected rows by the host-dependent
  steady-state warm-up (6–12 discarded calls); the timed counts are identical.

## Next

Wave B — lever 4b (A′: permute the active columns last, one `potrf`) — was never started: witness definition
first (active-set Jaccard on the seeded draw set, Δ evidence in nats, PDIP fallback count unchanged), then
`fnnls_cholesky_permuted` behind lever 3's solver seam as route `d_perm`, then its own RAL A/B with control =
this merged state. Re-filed as `draft/research/autolens_profiling/fixed_light_numba_s4b_permute_active_last.md`.

## Original prompt

# Fixed-light numba CPU round 4 — the curvature-matrix kernel A/B on Delaunay, then permute-active-last

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- profiling
- pixelization
- cpu
- numba
- inversion
Difficulty: large
Sizing-note: the intake sizing faculty derived too-large (score 12); large is kept — the two levers are
ordered and 4a is a measurement of two kernels that already exist; if it must be split, split between
lever 4a and lever 4b, never between a lever and its witness.
Autonomy: human-required
Priority: high
Status: formalised
Epic: fixed-lens-light-numba-cpu
Phase: 4
Consequence: judge
Witness: On HST Delaunay N=1500 numba CPU (RAL gpu partition CPUs-only, 1 thread), each lever carries a
before/after whole-call table with thread and backend recorded per leg; lever 4a returns the library's log
evidence to <= 1e-9 relative; lever 4b keeps the active set on every seeded draw within the witness's declared
tolerance with the PDIP fallback count unchanged; the note chains the cumulative from 413.3 ms.
Review-minutes: 30
Unattended: never
Filed: 2026-09-16
Issued: 2026-09-17
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/274

## Original request (verbatim)

> and you think theres nowhere else tp gp wotj numba? without digging through deeper stuff is level 4 not low hanging
> [...] i think 1 and 2 are worth doing

## Context

Phase 3 (#267, `complete/2026/09/fixed-light-numba-levers.md`) took the production numba CPU
fixed-light call from 413.3 to 230.0 ms. Its residue, from the lever-3 decomposition
(`results/notes/fixed_lens_light_levers_2026_09.md`, "Next"): `sparse_numba.curvature_matrix`
87.8 ms (38 %), `solver.fnnls_cholesky` 61.1 ms (27 %), `delaunay.triangulation` 18.9 ms (8 %),
everything else under 9 ms a site. This phase inserts ahead of the renumbered memo / scaling /
verdict phases of `fixed-lens-light-numba-cpu`, which become 5, 6 and 7. Two levers, measurement
first, in order.

## Lever 4a — A/B the two existing curvature kernels on Delaunay (low-hanging)

`curvature_matrix_via_sparse_operator_from` (PyAutoArray
`inversion/inversion/imaging_numba/inversion_imaging_numba_util.py`) dispatches on a pixel-count cap
(`two_stage_max_pix_pixels` = `CURVATURE_TWO_STAGE_MAX_PIX_PIXELS`) between the two-stage kernel and
the direct quadruple loop. The two-stage docstring itself says it wins for bilinear rectangular
(u0 = 4, 2.9x at the HST rectangular fiducial) and can lose for barycentric Delaunay (u0 ~ 1.55),
because stage 2 does a dense `pix_pixels`-long AXPY per mapping of every data pixel and then
re-zeroes the full accumulator, regardless of how few indices stage 1 touched. The choice was
never measured on the Delaunay fixed-light cell.

1. A/B the two existing kernels on the HST Delaunay N=1500 fixed-light cell (route b, memo ON):
   RAL `gpu` partition CPUs-only, 1 thread across numba and BLAS, the #267 two-arm harness with a
   private merge-base PyAutoArray on PYTHONPATH as control, `--n-repeats 64`. The direct kernel is
   already reachable by passing `two_stage_max_pix_pixels=0`; no library change is needed for the
   measurement.
2. If neither pure form wins, a touched-index variant of stage 2: record the indices stage 1
   touched, scatter only over them, zero only them. Same inputs, same outputs, same
   halved-diagonal / `A + A.T` contract.
3. Fix the stale dispatcher docstring regardless: it names
   `CURVATURE_TWO_STAGE_COST_RATIO_THRESHOLD`, the code branches on `pix_pixels`.

Pins: the kernels agree to floating-point reassociation (~4e-13 measured), log evidence <= 1e-9
relative, `log_likelihood` not comparable across arms.

## Lever 4b — A-prime: permute the active columns last, one potrf

Lever 3's design measured the permuted factorisation at 41 ms against `fnnls_cholesky`'s 61.1 ms,
reading ~15-20 ms more by folding both fancy-index copies and the second pass away. The cost: the
passive factor is perturbed at 5e-13, which reaches the active set's knife-edge inclusion
decisions, so the solve is no longer byte-identical and lever 3's cleanest property is given up.

1. Witness design FIRST: what "the same active set" means at 5e-13 — active-set Jaccard across the
   seeded graded draw set, evidence delta in nats, PDIP fallback count unchanged. Written down and
   agreed before a kernel exists.
2. The kernel, on the numpy/numba path only (`fnnls_cholesky`), behind the same seam lever 3 used.
3. The A/B on the same cell and host, control = lever 4a's merged state.

## Cell prerequisite (before either lever)

The harness's `max_instrumentation_overhead_ratio = 1.03` was calibrated on a ~400 ms call; its
fixed cost does not shrink with the call (1.0147 at 413 ms, 1.0366 at 224 ms) and it killed RAL
job 343355. Fix it in the cell before measuring: scale the cap with call length, or require a
minimum block count, or state it as a per-call millisecond budget (note "Next" item 6).

## Out of scope

`fnnls` algorithm changes beyond A-prime (phase 2 closed the solver round); the edge-zeroed
generalisation and the covariance third factorisation (zero gain on the production cell); the
`delaunay.triangulation` / `find_simplex` site (a separate candidate); the JAX path (both log-det
levers proven CPU-only, the A100 has no fnnls factor to read); route a, Euclid, rectangular meshes,
the source-pixel sweep, the sparse-operator/profile-subtracted-image bug.

## Witness

On HST Delaunay N=1500 numba CPU, each lever carries a before/after whole-call table with thread
and backend settings recorded per leg; 4a returns the library's log evidence to <= 1e-9 relative;
4b keeps the active set on every seeded draw within the witness's declared tolerance and the PDIP
fallback count unchanged; the note carries both tables and the cumulative chain from 413.3 ms.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3f1053cc-606f-4477-bef4-abe3a68cd02b/scratchpad/intake_raw.md -->
