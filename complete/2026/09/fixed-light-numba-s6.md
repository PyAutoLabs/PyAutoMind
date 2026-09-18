## fixed-light-numba-s6
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/282
- completed: 2026-09-18
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/283
- merge: e2ce1798bbb190ea49fa571bcd6a7cbfbec34291 (head705129d proven ancestor of origin/main)
- summary: Measured single-thread numba CPU likelihood at N500/1000/1500/2500/4000 with frozen nearby/broad sequences and production cold/memo lanes. All five cells PASS. NNLS dominates larger systems; N4000 nearby cold/memo2.138/1.289s, broad4.312/10.783s. Memo remains proposal-dependent; no production changes.

## Validation

15 focused tests, lint/format/import/shell/submit/README checks PASS; independent implementation, empirical, note, figure and provenance review CLEAN. All80 paired comparisons pass exact active sets and unchanged1e-9 relative evidence gate.960clean+960instrumented evaluations agree with diagnostics; worst reconciliation0.265%. GitHub lint workflow35357940517 and every job completed SUCCESS before the human-commanded merge.

## Evidence and interpretation

Five completed RAL jobs343430_0,343445_1..4; source48hashes and library revisions verified before/after. Results note and source/job sidecar are committed in results/notes/. Six repeats per lane, eight frozen draws per sequence. NNLS contributes68–95% atN4000. HarnessRSS9.085GiB includes eight prepared Analyses, not a production-worker memory recommendation; one4000x4000matrix128MB. Phase7 remains a separate HST+Euclid representative-proposal verdict, not a global memo default inferred here.

## Authorization and cleanup

Live user "yes I authorize that" permitted task-specific HeartRED development shipping. RED: `release validation FAILED (stage integrate)`; YELLOW: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`. Recorded in issue, PR,active.md and autonomy log. Current user `prm` authorized merge and close-out after all CI green; no release authorization.

Task worktree retained pending the skill-required decision on deleting ignored outputs: output/2.0MiB (local smoke results, logs, source snapshot and verification scratch), dataset/imaging/hst/lensed_source.fits164KiB, plus disposable caches. Published five-cell evidence is committed. No subscriptions/auto-merge/timers armed.

## Original prompt

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
Status: awaiting-merge
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

## Completed evidence — 2026-09-18

All five RAL cells PASS. Jobs343430_0 and343445_1..4 completed0:0 in
3:22,4:19,6:53,17:00,42:21 respectively. Source snapshot basefb303cf,
archive SHA2560f2bdad3f8d03e202e0ca6b67e9a7e526ad7792f77d63ce96a5c2383c8f72c80.
All48source inputs verified before/after; all RAL library revisions unchanged
and tracked-clean. Final source/job/artifact sidecar is
results/notes/fixed_light_numba_s6_source_jobs.json. Raw JSONs were compacted
losslessly; raw/formattedSHA and equality assertions retained in sidecar.

80paired comparisons PASS exact active sets and1e-9relative evidence gate.
960clean+960instrumented evaluations agree with diagnostic evidence. Maximum
evidence error5.23869e-10nats absolute/2.43191e-13relative; worst reconciliation
0.265% against5%gate.15focused tests, Ruff/format/import/shell/README checksPASS.
Independent implementation and full empirical/note/figure/provenance reviewCLEAN.

AtN4000 nearbycold/memo2137.865/1288.876ms; broad4312.031/10782.596ms.
NNLS accounts for68–95% of whole-call time atN4000. Memo saves39.7% nearby,
but broad costs2.50times cold. No production change/default recommendation.
HarnessRSS9.085GiB includes8preparedAnalyses; matrix alone128MB. Suggested
separate phase7: HST+Euclid with representative proposal histories.

24newfiles staged in worktree fixed-light-numba-s6/autolens_profiling,
branch feature/fixed-light-numba-s6; no source commit/push/PR yet.
Final note: results/notes/fixed_lens_light_numba_scaling_2026_09.md.
PR draft: PyAutoMind/tmp/s6-pr-body.md (scratch). All oldtaskfiles unchanged.

Remaining gate: live task-specific HeartRED shipping override for issue282.
Current RED reason: "release validation FAILED (stage integrate)".
YELLOW: "manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml".
No phase6 override requested/granted before this checkpoint. Final provenance review is CLEAN. Ask once with results and exact reasons. On grant,
record four sinks per PyAutoBrain/AUTONOMY.md, commit/push/open pending-release
PR via ship-workspace. Merge requires separate current human command and CI.
No run/CI subscription or scheduled wakeup exists. All cluster work complete.

## Shipping authorization — 2026-09-18

User: "yes I authorize that", responding directly to the issue282 request for
commit/push/PR despite the stated Heart RED/YELLOW reasons. Development-only
scope; no merge or release. Override recorded on the issue, PR body draft,
active.md and autonomy_log.md. Prior awaiting-input checkpoint is superseded.
Commit705129d contains all24 reviewed new files. Shipping smoke and submit
checks pass. PR creation follows successful push.

PR opened: https://github.com/PyAutoLabs/autolens_profiling/pull/283
Commit705129d pushed successfully; pending-release requested. Awaiting CI and
separate human merge command. No polling subscription or auto-merge armed.
