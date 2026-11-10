# Nautilus experimental spawn-based training pool

Work type: feature
Primary: @autofit_profiling
Read-only dependency: PyAutoFit (not an affected source repository)
Epic: nautilus-fast-likelihoods
Status: approved — workspace implementation
Issued: 2026-11-10
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/16
Consequence: judge
Witness: Four unchanged native neural networks trained through two spawned workers preserve coefficients/predictions and complete sampler trajectories; interrupted processes clean up and resume exactly; matched full-run timings include pool lifecycle and demonstrate whether any gain survives startup, serialization and teardown.
Review-minutes: 15
Unattended: never
Lane: local-dev

## User request (verbatim)

"ok good keep going"

Persistent constraints: "Keep it outside Pulse and leave merge for me."
Existing authorization: "Approved, proceed with both plans despite Heart RED. Keep them outside Pulse and leave merge for me."

This request continues experimental CPU work. The completed checkpoint experiment does not authorize a new sampling matrix automatically. This draft scopes the next decision; it does not authorize edits to library/harness source, new compute, issue creation, merge or release.

## Evidence and choice

The retained dimension pilot (producer544bc89; experiments/nautilus_cpu_dimensions/evidence/summary.json) reports median exclusive component shares for three traced seeds per dimension:

| Dimension | Adapter | Neural training | Bound geometry | Prediction |
|---:|---|---:|---:|---:|
| 5 | direct | 59.75% | 26.05% | 1.36% |
| 10 | direct | 60.60% | 27.02% | 1.60% |
| 5 | PyAutoFit | 41.72% | 18.21% | 0.97% |
| 10 | PyAutoFit | 37.79% | 16.90% | 0.99% |

These observations use live400 / ESS500 / fixed synthetic cost100. They rank targets, not predict a gain under the new live400 / ESS10000 / no-synthetic-work comparison. The 30D direct cell has only one complete seed and unresolved evidence error; exclude it from this optimization pilot.

The completed checkpoint experiment (PR15, measured5206f0b/librarye16fba3ee) is a negative result: interval5 full snapshots increased sampler time21.2–48.8% across all six pairs. Retain native interval1. The plotting candidate is separately in PR1764/PR14; do not mix it into this comparison.

Installed Nautilus1.0.5 neural.py exposes NeuralNetworkEmulator.train(..., pool=None). It already constructs four MLPs with ordered seeds0..3 via map or pool.map. Each train_network call limits native math threads to one. This is a narrow existing seam for measuring fork-free training concurrency. The July investigation rejected removing neural bounds and found a CPU JAX rewrite slower; it also cautioned against forking after JAX initialization. Neither workaround is proposed here.

If training really accounts for60% of runtime, perfect two-way acceleration alone has an optimistic whole-run ceiling near1.43x, before startup/IPC/imbalance. This is an upper-bound illustration, not a forecast or measured speedup.

## High-level plan

1. Add a standalone experimental harness that compares unchanged serial training with two persistent spawn-based training workers; no installed-package edits or production API change.
2. Preserve four networks, default architecture/stopping, per-network seeds, output order, and one native math thread per process. Keep likelihood evaluation and all sampler adaptation serial.
3. Require exact trained-model/prediction parity and controlled crash/resume recovery before admitting timing cases.
4. Run six interleaved D5/D10 seed pairs, with identical native checkpointing and output policy. Include startup, IPC and teardown in the full-workflow metric.
5. Retain positive or negative results, all failed/unrun cases and raw data; publish a development PR outside Pulse. Do not promote defaults from this experiment.

Tier: judge — merge mode: human /prm.

## Scope and proposed files

Workspace-only implementation in @autofit_profiling. Proposed branch feature/nautilus-spawn-training-pool; task worktree .worktrees/nautilus-spawn-training-pool. Run the formal branch/claim survey after approval. Do not edit canonical main, pinned dependencies, prior worktrees or archives.

Start the profiling branch from the retained diagnostic PR13 head2c3c0aa. Reuse its analytic target, resource supervision, source identity and reporting contracts. Carry the small test-only process-reaping fix c06cae0 if the source still needs it. Record the dependency on unmerged PR13; do not merge a base automatically. The experiment must run against pinned native PyAutoFit baseline bdb7af0, not require the checkpoint or plot candidate library PRs merely to reuse measurement helpers.

- scripts/analytic_gaussian/nautilus/training_pool_benchmark.py: immutable protocol, ordered matrix, dedicated spawn pool, native-training adapter, metrics, parity/recovery and bounded child supervisor.
- scripts/misc/profiling/nautilus_training_worker.py: importable, lightweight worker/initializer functions with no PyAutoFit/JAX import or global pool creation. Import native Nautilus/sklearn only where needed; cap native threads before imports. Confirm actual multiprocessing start method is spawn.
- scripts/misc/test/test_nautilus_training_pool.py: protocol/ordering, scoped restoration, cap/worker-failure behavior and stdlib-only supervision contracts; real runtime parity checks are included in the compute matrix below.
- experiments/nautilus_spawn_training_pool/: frozen protocol, exported results, failures/coverage, local review report. No catalogue, Pulse campaign/registry, release or production-library change.

Use a scoped replacement of NeuralNetworkEmulator.train only inside each disposable experimental child. Delegate to the original native method with the dedicated ordered pool argument; restore the original descriptor in finally. Do not change network settings, random draws, training data, native train_network implementation or sample weights. No patched source files in Nautilus/sklearn/anesthetic, vendoring, fork context, general sampler/likelihood pool, asynchronous adaptation or JAX rewrite.

The parent remains responsible for adaptation and result ordering. Two training workers persist for the entire fit; no pool per bound. Ensure native pool wrappers cannot accidentally dispatch geometry or likelihood work to this training-only pool. Stop rather than broaden the design if the seam cannot meet that constraint.

## Correctness and metrics

Preflight checks fixed corpus inputs, all four native MLP coefficients/intercepts and predictions, network seed/order, child process/thread settings, source/package hashes, readiness/teardown and absence of orphan workers. Compare exactly, not with an enlarged tolerance. A numerical mismatch stops this experiment; a statistical-equivalence design would require a separate decision.

Measure total workflow wall from before pool construction through worker teardown, native sampler.run, PyAutoFit fit/output, training wall, per-network duration and serialized payload bytes. Distinguish overlapping worker time from parent critical-path wall. Keep worker startup/readiness and teardown explicit; never claim a gain using only warm training. Report per-process/group RSS and actual workers/threads. Instrumentation is the same where applicable in both arms, and its overhead is not silently subtracted.

Every timing pair must match posterior array hash/order, likelihood count, ESS, shell count and stopping state. Preserve target truth/configuration hash. Native checkpoint files must remain valid and reopenable. Candidate full-run results also match the serial control in the recovery checks.

Controlled interruptions: (a) while neural training workers are active, after a valid native checkpoint exists; (b) immediately after a complete native checkpoint publication. Parent supervisor kills the entire process group, verifies no active descendants remain, retains the previous checkpoint and partial artifacts, and resumes a copy in a fresh process/pool. Record completed/in-flight likelihood and training work separately. Check checkpoint hash before/after the interruption and verify restored count before sampling. A successful resume must exactly match the shared uninterrupted serial D5/seed0 control. No power-loss or network-filesystem durability claim.

## Fixed proposed compute matrix and limits

Maximum18 children, each120s /4096MiB sampled process-group RSS;1800s total including runtime preflight and all between-case waits. Numerical threads1; training worker count2 only; one serial likelihood worker. No HPC/GPU/30D expansion.

1. One bounded runtime preflight child: frozen synthetic training corpus, serial-versus-two-spawn training equality, process lifecycle and configuration/source checks. No nested sampling in this child.
2. One uninterrupted serial D5/seed0 native control, retained for both recovery comparisons.
3. Four recovery children: training-active interruption + resume, then post-checkpoint interruption + resume, using the two-spawn candidate. All must pass before timing cases.
4. Twelve timing children: D5/D10 × seeds0/1/2 × serial/two-spawn training, interleaved AB/BA/AB per dimension.

Frozen sampling settings for control/recovery/timing: n_live400, n_batch100, n_eff10000, n_networks4 with unchanged default neural-network kwargs, n_shell1, discard_exploration=True, no synthetic likelihood work, native interval1 checkpoints, iterations_per_full_update1000000. Same analytic Gaussian prior/target as the completed checkpoint experiment. Disable only search corner plotting equally in both arms; retain other fit output.

Before launching the attempt, wait within the invoking chat for three one-minute-load readings below1.0, at least30s apart, and at least8192MiB available. This pre-launch waiting is recorded separately from the timed attempt. Do not launch a competing local benchmark/test during the pilot. No background subscription or task survives the chat turn.

Keep the existing admission threshold load<=max(1, affinity CPUs/4), memory>=twice child cap. Because two legitimate training workers may raise the recent load, allow up to60s of bounded between-case waiting for the unchanged admission threshold, charged to the1800s total; this is waiting before a child, not a retry or a relaxed load threshold. Reserve the full child cap before each launch. If admission still fails, budget is exhausted, any case errors/times out/exceeds memory, source changes, workers leak or any parity check fails: stop, retain the failure and all unrun coverage, no automatic retry.

## Validation and decision

Run tooling tests, Ruff check/format, catalogue unchanged/read-contract validation and applicable link CI. No library API changes; no production-library full-suite rerun is substituted for real runtime witnesses. Do not modify or weaken required checks to obtain a passing result.

Publish exact provenance, per-case/full-pair metrics, correctness witnesses, all resource/coverage states and raw-data locations. A promising warm training result with worse total wall is a negative end-to-end result. A positive result is grounds for a later library-integration plan, not implicit authority to add an API, change defaults or merge. A negative result redirects attention to geometry profiling after a separate scoped decision.

## Authorization boundary

Existing live HeartRED development permission supports continuing this experimental planning, with outside-Pulse/human-merge constraints. The published Heart feed remains RED, with older global CI/workspace alerts; current authoritative readiness and exact reasons must be recorded before issue/implementation under the continuing development override. No release or failed-check bypass.

Approval requested for this new workspace implementation and the specific18-child bounded local experiment. No issue/worktree claim/source edits or new sampling have been performed for this member yet.

## Brain routing and execution phases

The automated FeatureDecision classified the text as large/combined (score15), because it detected the named library and API/architectural terms. The concrete file list contains no library modification or public API. The in-session scope review therefore routes workspace-only, while retaining the requested phasing:

- A: isolated harness/worker implementation, static/tooling tests and immutable protocol; commit clean sources before compute.
- B: the six bounded preflight/control/recovery children above; stop on any failure, no timing admission without complete correctness witnesses.
- C: the twelve timing children, export/author review, CI and development PR. B and C share the same1800s budget; there is no per-phase budget reset.

A future production API/integration remains a separate plan even if this experiment succeeds. The July record and Memory methods index were consulted; no GPU/JAX-port assumption or network-removal proposal is imported from historical work.

Published Heart feed checked during planning: "Heart: RED — Release RED; monitoring RED · 11/100 · 138 unresolved (updated 5h ago)". Authoritative readiness receipt2026-11-10T18:35:43.930077+00:00 reports exact RED reasons: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "PyAutoCTI: 1 uncommitted source change(s)". Existing permission is used for this draft's planning only; implementation approval must explicitly cover this new bounded experiment despite RED. No release or failed-check bypass.

## Live implementation approval

Human selected "Approve this bounded experiment" for the18-child/120s/4GiB/1800s experiment despite HeartRED, outside Pulse and human merge. This supersedes the draft pending-approval statements above. No changes to approved scientific configuration or compute limits.

## Attempt01 and corrective verification

The approved attempt at c9f6d2e passed the fixed-corpus exact training parity and both interrupted/resumed sampling witnesses, then stopped after96.82s at the first timing child: native resume checkpoint pathname absent after successful Fit finalization. Six children passed, one failed, eleven unrun; no complete performance pair. All raw data retained, no retry.

Correction83530ce retains a hard link to the native checkpoint immediately after native.run returns, before normal Fit cleanup. Reopen after workflow timing verifies exact state and unchanged bytes with likelihood calls forbidden. Retention overhead is separately reported and included in full-fit/workflow timings equally; native sampler timing excludes it. Final archive and cleanup behavior, native checkpoint policy, neural networks, sampling settings and compute caps remain unchanged.145tooling tests/Ruff/catalogue pass; runtime correction awaits a fresh human decision under the stop-on-first-failure rule. Proposal: one new quiet-host attempt, same18children/120s/4096MiB/1800s, retain both attempts, outside Pulse, human merge.
