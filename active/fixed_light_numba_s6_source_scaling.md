# Phase 6: source-pixel scaling of the numba CPU likelihood

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: fixed-lens-light-numba-cpu
Phase: 6
Difficulty: large
Autonomy: human-required
Consequence: judge
Priority: high
Review-minutes: 25
Status: workspace-dev
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/282

## Original user request

> yep do it

Approves the preceding proposal: measure full likelihood runtime and memory versus source-pixel count, decompose costs, compare production memo on/off for nearby and broad sequences, preserve single-thread numerical checks. This follows merged #279 and #281; the phase-5b residual policy is not promoted.

## High-level plan

1. Profile HST Delaunay fp64 numba CPU with the current `_sparse` assembly API and production positive-only solve, using fixed lens-light subtraction as in phase 5.
2. Sweep requested source pixels 500, 1000, 1500, 2500, 4000. Record actual mapper and solve dimensions separately.
3. At every N compare production memo off/on on the same eight nearby and eight broad draws. Freeze seed 601 and the draw manifest before timings; use phase-5b 0.05/5 prior-sigma stepping conventions, no policy tuning.
4. Run six fresh-cache traversals per lane/sequence, alternating lane order, with compilation and setup outside clean whole-Analysis timings. Keep identical model sequence across N; do not compare numerical solutions across different discretizations.
5. Diagnose curvature, regularization, NNLS and determinants separately; explain residual overhead and avoid double-counting nested timers. Record peak process RSS in an isolated process per N, and distinguish it from matrix memory.
6. Publish JSON/PNG and a qualified note: runtime/memory scaling, bottleneck fractions, memo sensitivity and measured crossover intervals. No extrapolated performance claims or production changes.

## Detailed implementation and validation

All additions live in autolens_profiling, based on merged origin/main:
- scripts/imaging/likelihood_breakdown/fixed_light_numba_scaling.py: prepare/evaluate size cells, clean timing lanes, manifest and diagnostic passes. Reuse phase5.prepare(rows, source_pixels), memo_scope and compare_solutions read-only.
- scripts/misc/likelihood_breakdown/fixed_light_numba_scaling_steps.py: exclusive timing collection, aggregation, dimensions/memory metadata, slope calculation with raw points and fit quality.
- scripts/misc/test/test_fixed_light_numba_scaling.py: meaningful tests for lane/cache isolation, timer nesting, missing/failed cells and paired numerical gates.
- hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_scaling_delaunay_ral_hst_fp64: single CPU, pinned BLAS/Numba thread environments, separate process/job per N, finite walltime and memory bounds. Full sweep on private source snapshot; never refresh shared libraries during another run.
- results/breakdown/imaging/: per-N evidence, raw repeated timings and plots; results/notes/fixed_lens_light_numba_scaling_2026_09.md plus source/job manifest.

Numerical gates: reuse phase-5 comparator unchanged (including exact active-set equality and 1e-9 relative evidence gate) for memo on/off at each same N/model. Carry reconstruction checks and clean/diagnostic likelihood agreement. Report evidence absolute errors too. Any failure blocks interpretation as equivalent likelihood performance. Timers must reconcile with separately observed whole-call timing to 5%; otherwise label breakdown inconclusive, retain clean whole-call results, fix instrumentation before claims. No sum of overlapping timer categories.

Report per-traversal totals, distributions and raw repeats; empirical log-log exponents are descriptive, not asymptotic complexity proofs. No crossover interpolation outside measured brackets. Cache hit/fallback/iteration metadata is diagnostic only. Per-N memory reports include preparation/compilation explicitly; no claim that process RSS equals solver memory. A timed-out/OOM leg stays a failed/censored observation and is not silently omitted. First run small-N smoke and N1500 parity sanity check before the full sweep. Capture library revisions, source hashes, hardware/load, environment thread pins and runtime thread evidence (unavailable when not observable). Ruff/format/import/API/shell/README gates and independent review before shipping.

## Branch survey and coordination

Canonical autolens_profiling: main, clean. PyAutoMind: main, clean before this prompt.
Recent profiling branches: phase5b, phase5, phase4b, main, GPU phase2.
Proposed branch: feature/fixed-light-numba-s6.
Proposed task root: ~/Code/PyAutoLabs-wt/fixed-light-numba-s6/.
Conflict guard finds hst-gpu-residue-p2 and fixed-light-numba-s4b still claiming autolens_profiling. Request explicit approval for this separate worktree, with new phase-6 files only and existing source files unchanged. Prior phase-5/5b waivers were task-specific. Old phase-5 worktrees remain preserved with local outputs pending cleanup permission; they are not reused.

The issue body is this two-level plan. Do not create issue, worktree or source edits until the coordination guard is approved. Phase 7 (HST + Euclid verdict) remains separate.

## Live authorization

2026-09-18: user replied **yes go** to the phase-6 plan and separate-worktree coordination request. Both existing claims were rechecked; new phase-6 files only. Base fb303cf.

## Run checkpoint — 2026-09-18 14:53 BST

Implementation complete, 15 focused tests + Ruff/format/import/shell/README checks PASS.
Independent implementation review CLEAN. Independent empirical review CLEAN for
N500/1000/1500; root artifact verification also passes N2500. No old task source
files changed. Worktree branch feature/fixed-light-numba-s6; source + four cells
and explicitly interim note/aggregate are staged, no source commit or PR.

RAL first job343430_0 N500 completed0:0 in3:22. Array343445_1 N1000 completed4:19,
_2 N1500 completed6:53, _3 N2500 completed17:00, all0:0 and every gatePASS.
Final343445_4 N4000 started14:52BST, still running at checkpoint. The run limit
is4hours/64GiB/oneCPU, noGPU. Do not resubmit completed sizes. No monitoring
subscription or agent wake-up is armed.

Private remote snapshot: /mnt/ral/jnightin/autolens_profiling_wt/fixed-light-numba-s6-run
(local output/s6/source.tar.gz and source_manifest.json). Archive SHA256
0f2bdad3f8d03e202e0ca6b67e9a7e526ad7792f77d63ce96a5c2383c8f72c80;48inputs
verified before execution and unchanged locally. Basefb303cf. RAL stackclean:
Array192d4b7,Fit7c0e79a,Galaxy90e757d,Lens478213e,Nerves8eca4b3. Exactfull
revisions in artifacts and output/s6/ral-provenance.txt. Compute lscpu captured
separately in ral-compute-lscpu.txt (AMD EPYC7702,124onlineCPUs); lscpu inside
ral-provenance.txt is the login node and MUST NOT be described as compute hardware.

Next steps:
1. Read sacct343445 and tail output/output.343445_4.out under remote hpc/batch_cpu.
2. Pull *s6_n4000* from remote results/breakdown/imaging into the worktree same
   folder only after final file written. Preserve any failure/censored cell;
   do not silently drop it or rerun to obtain a desired result.
3. Run output/s6/verify_results.py (current cells allPASS,64pairs); final allfive
   should give80pairs,960clean+960instrumented evaluations.
4. Source ../activate.sh; run driver --aggregate --output-dir results/breakdown/imaging.
   output/s6/finish_note.py drafts tables only IF all gates pass; inspect and
   write real final interpretation, not just its generated tables. Remove interim
   status/table. If final cell fails, adapt note to report failure honestly.
5. Add source/job sidecar with source_manifest, alljobstates/elapsed/MaxRSS,
   remote post-run48hashes and library cleanliness; dataset/source/library
   identity across sizes already checked through2500. Runtime BLAS count is
   unavailable; only envpins1 and Numba runtime1 are observed. RSS is harness
   high-water with8prepared Analyses, not a single production likelihood.
6. Ask existing independent s6_review worker for complete empirical/note review;
   code review alreadyCLEAN. N2500/N4000 not yet independently reviewed.
7. Final validation and draft PR against main via ship-workspace. Heart remains
   RED release validation FAILED (stage integrate), YELLOW manifest drift:
   remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml.
   No phase6 shipping override has been requested/granted; do allreviewable work
   first, then obtain live task-specific grant if these reasons persist.

Local N100/N1500 smoke numerical results passed, but concurrent smoke timings
were discarded; final RAL code additionally counterbalances clean/observed order.
The failed first timer wiring (interferometer curvature target) and accidental
oldtest edits were fixed before the source snapshot; currentproduction target
is imaging_numba.sparse.InversionImagingSparseNumba and actual NNLS callable.
Do not quote earlier55tests: that was a worker path mistake; finalnew7 plus
parent8 =15focused tests. Existing source files are unchanged.
