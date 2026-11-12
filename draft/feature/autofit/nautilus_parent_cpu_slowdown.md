# Diagnose parent CPU slowdown after native training-pool use

Status: approved 2026-11-12 by live human; one gated 12-fit RAL job authorized, not yet submitted.
Target: @autofit_profiling
Consequence: judge
Continuation: issue16 / draft PR17, nautilus-spawn-training-pool.
Existing worktree: .worktrees/nautilus-spawn-training-pool/autofit_profiling
Existing branch: feature/nautilus-spawn-training-pool (clean fc508ae)
Outside Pulse. Merge stays human. No release or default change.

## User request (verbatim)

> Can we investigate why the other CPU work slows down when the training pool is enabled? Keep it outside Pulse and leave merge for me.

## Existing evidence and new read-only finding

Job415180 completed17/17 cases with exact parity on euclid-ral-compute-1. Mean traced10Dseed2: training saved2.24s, other fit work added8.11s (parent CPU added7.78s), lifecycle added1.62s. Full workflow31.12→38.61s. Equal phase call counts, likelihood count, posterior/model/target digests, native one-thread metadata; hardware/runtime cause unresolved.

Chronology analysis of the retained receipts requires no new sampling/training/evaluation. With the pool already initialized, the eight likelihood batches before the first training call take mean0.08627s serial versus0.08738s pooled parent CPU (~1.3% difference). After the last of11 training calls,168 remaining batches take1.81169s serial versus3.39046s pooled (~87% more). Several early training intervals in the first pooled fit alternate between fast/slow; the second pooled fit stays near serial until the last training call. Mere pool creation is therefore not a sufficient explanation in these observations. Worker activity after training, transferred-model/GC effects, parent thread/runtime state and CPU placement remain hypotheses. Coarse native thread-count snapshots alone cannot resolve them.

## High-level plan

1. Preserve the retained-data onset analysis and use it to target the long post-training interval rather than repeat the previous broad benchmark.
2. Add a controlled full-fit comparison: original serial and pooled modes, pooled workers closed after the final training call, serial models passed through a pickle roundtrip, and matched parent-pinned serial/disjoint-worker modes.
3. Observe main-thread versus process CPU, worker CPU during non-training intervals, parent placement, garbage collection and native runtime state without changing library code or numerical settings.
4. Require exact historical science/model parity and consistent phase counts before interpreting any timing. Compare within this new instrumented study; do not equate timings with uninstrumented speedups.
5. Run one fixed bounded RAL job only after tests, green CI, current readiness and a fresh zero-science runtime restore. Stop at first failure and retain everything.
6. Publish the evidence and unresolved alternatives in the existing PR. Do not change defaults, ingest Pulse, merge or release.

Tier: judge — merge mode: human /prm.

## Frozen proposed matrix: twelve full fits

Two reverse-order rounds over six arms: A,B,C,D,E,F then F,E,D,C,B,A. Two observations per arm; positional balancing is not statistical significance. Every case is a fresh10D/seed2 wrapped fit under the same original native configuration. No extra capture fit, synthetic likelihood work, training replay, warmup fit or probe likelihood call.

- A: original serial training, parent may use all four allocated CPUs; no training workers.
- B: original persistent two-worker training, parent/workers share the same four-CPU mask.
- C: identical to B through the final (11th) native training call, then close and reap the owned training workers before subsequent parent work. Do this after the trained result is collected and its native training timer has ended. Record shutdown in its own phase. An unexpected12th training call is a hard failure, never a pool restart or serial fallback. This tests worker lifetime during the long post-training tail while retaining the same transferred models.
- D: serial training as A, but roundtrip each returned native network through the same effective multiprocessing pickle protocol before use; no workers. Record serialization separately and require exact model parity. This tests transfer-related object/layout effects without a live pool. It is an intervention control, not a proposed optimization.
- E: serial training with the parent pinned to the lowest of the four validated allocated physical CPUs for the fit.
- F: same parent CPU as E; two training workers each pinned to the next two distinct allocated CPUs. Create workers while the parent still has the original four-CPU allocation, then narrow its mask for the fit. Restore parent affinity in finally before allocation revalidation. E controls the parent pinning change; F tests a disjoint placement policy. Comparing B and F alone does not separate parent pinning from worker placement.

All cases require the exact historical reference node euclid-ral-compute-1. No fallback node/partition, no other campaigns' scheduling changes. Affinity is only narrowed within the validated allocation; all workers/threads remain in it. The original protocols/matrices remain unchanged and retained.

## Science and resource invariants

Fitbdb7af0e9c339ad07850679fd6ac168aacc7d18c, Nerves9b204c90c2ce05c5bb0cf3e9800ed13f005c6c56, native Nautilus1.0.5 and the full frozen runtime inventory remain unchanged. Four native networks/seeds0..3; live400,batch100,ESS10000,n_shell1,discard_exploration=True; serial likelihood/adaptation; one native numerical thread; native checkpointing; no synthetic likelihood work. Search corner disabled equally; all other output retained. Fixed reference job415139/10Dseed2 and retained exact corpus/model/checkpoint records remain authoritative; no tolerance or replacement reference.

At most12 supervised scientific case processes (with their owned worker subprocesses inside each group),120s/4096MiB per group and1800s aggregate including admission/verification. One exclusive partition=ral job on euclid-ral-compute-1, one task/four bound physical cores,8GiB,35min;180s bootstrap and120s cleanup reserve. The reservation includes the whole252-CPU scheduler node; only four CPUs are used by the scientific step. No retry/requeue/replacement or additional scientific job. First resource/source/accounting/parity failure halts later cases and records them unrun.

## Detailed implementation

Continue the existing task/worktree/issue16/PR17; do not change installed dependencies or production libraries.

- New scripts/analytic_gaussian/nautilus/parent_cpu_diagnostics.py: versioned immutable12-case plan, original-node and environment admission, fixed arms, durable pre-fit runtime/candidate/success/error receipts, reference/checkpoint/phase checks and terminal state. Reuse validated source/runtime/configuration/checkpoint/supervision helpers without broadening earlier protocols. Use a fresh output/parent-cpu-diagnostics-ral-01 claim.
- New scripts/misc/profiling/nautilus_parent_cpu.py: diagnostic-only transport/lifecycle controls for arms A–F. Reuse ordered native training seam; verify seeds/function and actual worker affinity. Explicit one-time early shutdown after training call11 for C with idempotent final cleanup. D uses the actual multiprocessing effective serialization protocol and records array shape/dtype/strides/C-F layout/alignment modulo64 before/after transfer; do not mutate numerical values. All results still pass exact model and end-to-end parity.
- Optional observer seam in existing diagnostic PhaseTrace, with original default behavior unchanged, or a dedicated subclass: add nested main-thread CPU accounting alongside process CPU/wall; require exact reconciliation of each channel. Observe parent CPU endpoints/context switches/fault counters only at coarse boundaries (likelihood batches, training, geometry and final output), not per likelihood or per prediction. Record observation overhead separately; restore patched descriptors, affinity and callbacks on every exit.
- Track parent GC start/stop/generation/collected counts passively; never disable GC, force a collection, change thresholds or use GC as an optimization in this study. Snapshot GC state and full native-library thread/runtime metadata before the fit, around each training call and after fit. Read available cgroup CPU quota/throttling counters and parent scheduling/affinity state; no configuration changes, privileged profiling or new installed tools. Explicitly label unavailable observations and global counters.
- Read owned worker/process-thread CPU counters after results are collected and before the next training call, plus at final output. Distinguish active training intervals from supposed-idle intervals. Observe main-thread/process CPU differences to test parent executor-management overhead. Worker CPU remains separate; never sum overlapping worker wall durations into parent elapsed time. Boundary snapshots are observational and do not imply continuous placement or isolated hardware causation.
- hpc/tools runtime builder/cache: add the explicit allowlisted parent-cpu diagnostic identity bound to its wrapper/entrypoint/manifest hashes; preserve old defaults/experiments and storage/runtime gates. New hpc/batch_cpu/submit_nautilus_parent_cpu_diagnostics with fixed original node, separate environment and atomic new claim.
- Focused tests: immutable arms/order/limits; wrong-node/mask rejection; affinity restoration; serialization parity and protocol selection; early shutdown exactly once/no later dispatch/no live workers; missing/invalid CPU counters; nested thread/process/wall accounting; passive GC callback restoration; candidate preservation and unverified rejection; fail-stop/resource/deadline/duplicate-claim gates; allowlist mismatches; regression coverage for original training/diagnostic contracts.

## Decision logic and interpretation

- C versus B on the same last168 likelihood batches tests whether removing the trained workers changes the slowdown. If it helps, inspect idle-worker CPU and parent thread counters; shutdown also changes scheduling/runtime conditions, so it is not by itself proof of busy spinning or cache contention.
- D versus A tests whether serialization alone reproduces the loss; record layout/alignment/GC evidence without treating correlation as causation.
- E versus A tests parent pinning; F versus E tests pooled training with disjoint placement. F versus B assesses the complete placement policy, not either change independently.
- Before the first training call, B/C have created pools but have not trained. Retain this within-fit startup control. Align later observations by training-call count and phase ordinal, with identical phase counts and exact science gates.
- Compare wall, parent process CPU, parent main-thread CPU, worker activity and passive runtime/GC evidence. If inconclusive, report that clearly and propose no default change. Avoid extrapolating from two observations per arm.

## Gates, retention and approval boundary

Before submission: approved plan, clean exact source commit, appropriate tests and zero-science lifecycle/affinity smoke, lint/format/shell/catalogue validation, author review recorded honestly, exact-head CI green, current authoritative Heart readiness, exact pinned-runtime validation and fresh zero-sampling/zero-training artifact restore/cleanup. Scientific outputs remain on the witnessed shared storage; runtime/source node-local. Submit once through hpc/sync, persist job ID/consumed authorization immediately. Resolve an ambiguous submission through accounting; never blindly retry.

Retain all twelve case receipts/raw data, runtime/staging evidence and all previous jobs. Cleanup only the newly owned temporary runtime cache. No persistent watcher, automatic merge, issue close-out or release. No new science has been run for this proposal.

Entry feed: “Heart: YELLOW — Release YELLOW; monitoring RED · 16/100 · 165 unresolved (updated 25m ago)”. Authoritative2026-11-12T13:48:57.456105+00:00 YELLOW/no RED reasons: “PyAutoArray: open PR 9d old”; “release validation stale: source moved since rehearsal (PyAutoFit, PyAutoGalaxy, PyAutoLens)”. Recheck at shipping; no failed branch gate can be overridden.

Workspace AGENTS.md requires an explicit approved plan before source/job-script edits. The prior single-job grants are consumed. Approval requested for this implementation and one12-case RAL job under the stated limits; merge remains human.


## Classification and branch survey

The Feature CLI matched the `autofit` folder as a library target and returned a generic combined/library API plan. Scoped review overrides that routing: all proposed executable changes are in autofit_profiling; Fit, Nerves, Nautilus and other installed libraries are immutable measured dependencies. This is workspace-only experimental diagnostics. Stage implementation as (1) fixed matrix and lifecycle/serialization controls, (2) passive instrumentation and accounting, (3) allowlisted runtime/job integration, (4) the single gated run and report. Review each stage; no additional scientific runs are implied.

Memory was consulted for CPU benchmark hygiene: compare identical science on the same hardware, balance order, and separate diagnostic instrumentation from an uninstrumented performance claim. It supplied no established explanation for the observed slowdown.

Producer worktree is clean at fc508aefcabf58e7c4cb65a12fcf19f2375daa8a on feature/nautilus-spawn-training-pool. Canonical producer main is clean. Conflict guard passes for this existing task; it warns only about the retained phase-0 baseline/setup worktrees from this same experimental history. Those remain untouched. PR17 is draft/open/unmerged, based on feature/nautilus-30d-diagnostics. Continue issue16 and the existing worktree; do not create a duplicate issue or broaden library scope.

## Retained evidence provenance

The onset analysis sums exclusive parent-process CPU from existing Sampler.evaluate_likelihood events. Before training means an event finishes before the first native training event starts; after training means it starts after the final native training event finishes. Every fit has 8 before-training batches, 168 after-training batches and 235 overall. Each mean uses two fits. No native science code was run for this analysis.

| Receipt within retained job415180 pilot | SHA256 |
|---|---|
| fit-0-w0/child.json | 48d211b6fa4e655867240fa0e82e9a8fdd4e7e15ff6889829a972410f3386850 |
| fit-1-w2/child.json | b42754aae7dd6a53e29b89a6de6ddd154c89005181a7430a9317d62c2066c7ab |
| fit-2-w2/child.json | 428be0248fe214cdd99df90f85e306679ea95a30aef09da444e7c1632562b349 |
| fit-3-w0/child.json | 7a1aa42822f75844d247636aac3f8e3157f67d5fa4d809850aca14d55dd057fc |
