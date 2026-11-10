# Nautilus opt-in CPU checkpoint batching

Issued: 2026-11-10
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1763
Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_profiling
Classification: Both (library plus experimental benchmark workspace)
Consequence: judge
Autonomy: supervised
Epic: nautilus-fast-likelihoods
Phase: experimental phase1 sampler overhead optimization

## Scope and authority

Original request (verbatim): "ok this sounds like a worth while thing to do, can we do this and also start some of the other CPU sampler speed up work?"

Experimental continuation of nautilus-fast-likelihoods. Outside Pulse; no campaign registration, HPC submission or release. Full phase0b remains incomplete. Tier: judge — merge mode: human /prm. Status: approved for implementation, validation, bounded pilot and development PRs; live Heart RED override granted for both plans. Current authoritative RED reasons: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure" (2026-11-10T15:48:37.310808+00:00).

The existing diagnostic PR autofit_profiling#13 is open and green at2c3c0aa. Keep it unmerged and retain every old worktree/raw archive. These are new bounded implementation members, not additional changes slipped into that diagnostic PR. Register one issue/implementation PR per member after approval. Use isolated feature branches and serialize coding claims for PyAutoFit/autofit_profiling under the same session; explicitly transfer only this session's profiling claim, recording the pending diagnostic PR/retained worktree. Use a profiling branch based on the diagnostic head where its helpers are needed, label that dependency, and never merge its base automatically. No source edits in canonical main or pinned dependency archives. Library-first merge gates remain human.

Library survey: canonical PyAutoFit main clean atbdb7af0e9, no other active PyAutoFit coding claim in Mind. Existing plotting fixes already defer shared-axis handling and avoid duplicate pyplot draw. Profiling claim belongs to nautilus-30d-diagnostics; resolve its same-session handoff explicitly during setup. Recheck refs/claims before creating worktrees. Pin the baseline and candidate dependencies; never update the retained environment in place.

## Evidence and expected benefit

The phase0a traced one-worker fixed-cost medians attributed checkpoint I/O11.6% direct/8.7% wrapped; neural training51.9%/37.4%, geometry32.4%/24.2%, likelihood dispatch0.5%/1.1%. These are noisy fixture-specific measurements, not all-workload guarantees. Even eliminating checkpoint cost gives only about1.13x/1.10x ideal speedup. Full snapshots may offset batching gains; measure rather than promise.

Implementation owner: @PyAutoFit. Experimental benchmark owner: @autofit_profiling.

## High-level plan

1. Prototype opt-in batching of native checkpoint persistence in the PyAutoFit Nautilus adapter, preserving sampling and neural-bound settings.
2. Keep each committed disk snapshot internally consistent and bound the work lost on interruption.
3. Validate clean finish, interruptions and resume before a small matched CPU sampling pilot.
4. Publish separate runtime/durability results; keep default behavior unchanged.

## Detailed implementation

- Proposed branch feature/nautilus-checkpoint-batching from clean library baseline, independent of the plotting change. Add a focused helper/subclass in autofit/non_linear/search/nest/nautilus/checkpoint_policy.py; integrate via search.py sampler construction/sampler_cls seam. Add checkpoint_interval_batches default1 with validation/documentation and corresponding packaged config only where the constructor currently obtains such defaults.
- Interval1 preserves the current native path; checkpoint=False retains no-checkpoint behavior, and incompatible explicit interval combinations are rejected clearly. Candidate interval5 is experimental opt-in. Guard supported native schema/version (initially Nautilus1.0.5); do not patch the installed package or globally replace h5py functions. Preserve the current large-attribute HDF5 context, native checkpoint resume and worker initialization/watchdog behavior.
- Do not defer one shell while writing global metadata from a newer state. For interval>1, accumulate completed batch updates in memory; at the interval, write a complete native snapshot to a same-directory temporary .hdf5, close/flush it, then atomically replace the published checkpoint. Publish no partially updated mixture of shells, caches, bounds, exploration flags, counters or RNG state. Retain the previous good snapshot if writing fails; propagate the error. Clean owned temporary files without touching prior archives.
- Honor native full-write points immediately (initial snapshot, bound transitions, exploration-mode transition). Flush pending state on normal sampler.run return, including normal budget/timeout return, and before wrapper full-output boundaries. Do not serialize a potentially inconsistent half-mutated state after arbitrary exceptions. On abrupt termination resume the last complete snapshot; report lost completed batches/evaluations and any in-flight work.
- No acceptance/adaptation change, point dropping, altered random draws, lower ESS target, neural-network removal, training parallelism, new process pool or JAX port. This reduces disk overhead during sampling; it does not increase statistical efficiency.

## Validation and compute

Unit/native integration tests cover invalid intervals, unchanged default path, all dirty shells, blobs/live caches, RNG and discard-exploration flags, large attributes, bound/mode transitions, failed temp writes, atomic replacement, ordinary return and native reopening. Verify that saving consumes no sampler RNG and uninterrupted interval1/5 runs have identical trajectories/posterior hashes/call counts. Explicitly measure maximum lost work; make no untested power-loss/network-filesystem guarantee.

Before performance timing, four supervised crash/resume witnesses: workers1and2 crossed with kill while updates are deferred and kill during an atomic write. Up to two children per witness (interrupted then resumed), each120s/4096MiB; compare resumed final posterior/count/ordering against matching uninterrupted controls. Prove at least the previous committed file remains usable after interrupted writes. Abort performance pilot on any correctness failure; no automatic retries.

Performance matrix: dimensions5and10, seeds0/1/2, interval1versus5, one worker/native threads1;12children maximum,120s/4096MiB each. Use400live points,batch100,four neural networks,discard exploration enabled,ESS10000 and fixed shell minima identically across each pair. Freeze exact protocol/source/target hashes before launch. Interleave policy order by seed; use identical plot/output policy in both paths and report sampler.run separately from end-to-end output. Do not compare these fresh-sample settings as speedups against the historical phase0a settings.

All correctness witnesses, runtime preflight and performance children share1800s aggregate budget (at most20children for crash/resume+matrix). Existing load/memory guards; stop on cap/failure, retain missing/unrun coverage. No30D/remote scaling in this first optimization pilot. Required library full-suite/CI and applicable smoke are validation gates, not part of this timed-run budget.

Report write counts/bytes/time, native sampling wall, full fit wall, memory, pair ratios, checkpoint integrity and recoverable lost work. Benefit is not assumed: if frequent full snapshots erase savings, retain the negative result and do not promote an inefficient path. Defaults remain interval1. Larger neural/geometry improvements and worker scheduling remain separate later decisions.

## Execution phases within this approval

Brain feature routing classified this as large library work. Keep three sequential gates: (A) compatibility/design and deterministic correctness tests; (B) opt-in implementation plus parity or interruption/resume witnesses; (C) the stated bounded paired pilot and development PR. Do not start C if B fails. Approval covers these stated phases only; changing scientific semantics, defaults, resource caps or external-library source requires a new decision. No independent agent delegation requested; execute sequentially.

## Live approval

"Approved, proceed with both plans despite Heart RED. Keep them outside Pulse and leave merge for me."
Approved for the stated implementation, validation and bounded pilot. No merge/release.

## Fresh corrected pilot approval — 2026-11-10

Live human selected "Run corrected checkpoint pilot once" after attempt01 receipt serialization failure. One fresh run of corrected harness daf0cc6, unchanged20children/120s/4096MiB each/1800s total, stop on first failure. Clean producer15afe55 contains the identical harness plus test portability and attempt01 report only. Preserve both attempts, outside Pulse, no merge.

## Quiet-host fresh pilot approval — 2026-11-10

Live human: "Try the checkpoint pilot again once the host is quiet, with the same limits. Keep it outside Pulse and leave merge for me." One new attempt03 with the unchanged corrected harness and limits; preserve all attempts, stop on first failure/cap. Wait in this turn for three load readings below1.0 spaced30s, with required memory available; this is a stricter launch condition, not a change to the in-run guard or compute budget.
