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

## Corrected attempt approval

Live human selected "Run corrected pilot once" at83530ce. Run training-pool-02 once after unchanged quiet-host admission, with18children/120s/4096MiB/1800s limits; retain both attempts, stop on first failure, outside Pulse, human merge.

The corrected pre-launch watch quiet-host-02 ended without three consecutive load readings below1.0. No pilot output directory or scientific child was launched; the single approved corrected attempt remains unused. Keep the same source/limits and collect fresh quiet-host readings on continuation; no renewed approval is needed merely to resume admission. No watcher survives the turn.

## RAL timing amendment — proposed 2026-11-10

User request (verbatim): "yeah we should be doing the real timing on RAL".
This supersedes the laptop timing destination. Do not restart laptop admission. The previous corrected local attempt was never launched. This amendment changes the previously explicit "No HPC" scope and admission policy; its concrete allocation/implementation is presented for approval before source edits or submission. Existing experiment-specific Heart RED development authorization, outside-Pulse scope and human merge remain in force.

### High-level plan

1. Run the entire correctness-gated comparison in one RAL CPU allocation, not separate nodes or an array. Both variants share the same host, CPU affinity, environment, filesystem and AB/BA/AB ordering. Do not combine laptop and RAL timings or claim speedup from different machines.
2. Request one exclusive CPU node on partition ral, bind one task to four physical cores, request8GiB memory and a35minute scheduler limit. Exclusivity reserves all node CPUs even though the task uses four. No GPU allocation or fallback partition. Confirm live partition/node policy before submission; unavailable policy/resources stop, not silently broaden scope.
3. Preserve18children,120s/4096MiB per child and1800s scientific budget, including runtime preflight and between-case checks. The extra five scheduler minutes allow allocation verification and cleanup, not additional scientific cases. Failures/caps/parity mismatches/leaks stop once; no retry, requeue or replacement job.
4. Replace laptop load-based admission with verified exclusive SLURM allocation, physical-core binding and available job memory. Record host load as evidence; it is not a substitute for allocation isolation. Preserve the local admission mode for historical reproducibility but do not run it for this task.
5. Repeat the six correctness children on RAL before all twelve timing children. Keep the four native networks, serial likelihood/adaptation, two spawned training workers, one numerical thread each, source pins, stopping settings, final-checkpoint retention and full-workflow timing unchanged.
6. Retain raw output, receipts, SLURM accounting and failed/unrun coverage. Report total-workflow and sampling/training timing separately in PR17. No production API/default changes, no Pulse catalogue/registry additions.

Tier: judge — merge mode: human /prm.

### Implementation and evidence

Continue issue16 / draft PR17, branch feature/nautilus-spawn-training-pool, current source83530ceaee7d62297a0139f7a14c2043090ba6b0. No new competing repository claim. This is a workspace-only extension; no installed library or shared cluster environment changes.

- `scripts/analytic_gaussian/nautilus/training_pool_benchmark.py`: versioned explicit execution/admission mode; bind allocation receipt into the frozen plan; verify before each child; retain existing per-process-group timeout/RSS/cleanup and1800s budget. A SLURM environment variable alone is not proof of allocation. Parent/worker affinity must remain inside the four physical cores, with no unintended math threads. Record actual cpuset, topology, node, job/step IDs, allocation/TRES and effective memory allowance. Reject missing/unverifiable evidence, GPU resources, non-exclusive allocation, changed affinity or insufficient remaining job memory.
- `scripts/misc/profiling/nautilus_allocation.py` (new): read-only SLURM/cgroup/CPU-topology inspection with bounded command timeouts and strict receipt validation. Use the cluster's supported SLURM output schema after read-only discovery; do not fabricate sample IDs or accept stale receipts. Allocation-level memory and affinity checks must not rely only on host-wide `/proc/meminfo` or advertised CPU count.
- `hpc/batch_cpu/submit_nautilus_training_pool` (new): single-job wrapper, ral-only, no array/GRES/mail/requeue. Fail-fast shell, explicit core binding, fixed thread environment, unique output directory, traps and exit status preserving failures. The35minute scheduler request is a hard budget cap with cleanup margin, not a runtime forecast. Run measurement only on a compute node. Capture scheduler accounting and verify all task processes finish. Use the existing hpc/sync submission interface after configuring its isolated task root; never rsync over the canonical RAL git checkout or change another campaign.
- `scripts/misc/test/test_nautilus_training_pool.py` and a focused allocation test module: wrong partition/job/node, shared allocation, missing cgroup evidence, topology/affinity mismatch, GPU TRES, exhausted budget/memory, no valid admission, child cleanup and post-fit retained-checkpoint cases. Shell syntax and all tooling tests/Ruff/catalogue/link checks. No science timings on the laptop.
- `experiments/nautilus_spawn_training_pool/protocol.json` and `README.md`: separate versioned RAL protocol, exact hardware/software/storage provenance, explicit host admission change, old receipts retained. Export a distinct RAL receipt; no fabricated reuse of the laptop quiet-host log.

### Remote staging and reproducibility

Read-only discovery first: verify SSH, partition/node topology and exclusivity policy, cgroup accounting, job bindings, scratch/storage capacity and installed runtime. Then use a unique task directory under the RAL profiling area, with clean git worktrees pinned to the approved producer and read-only PyAutoFit bdb7af0e9c339ad07850679fd6ac168aacc7d18c / PyAutoNerves9b204c90c2ce05c5bb0cf3e9800ed13f005c6c56. Do not switch or reset shared source trees or run HPCPullPyAuto against another experiment's pins.

Use the shared runtime read-only only if its scientific dependency inventory matches the approved local inventory. Otherwise prepare a separate task environment with matching Python/scientific package versions and record the full resolved inventory; never upgrade the shared venv. If the pinned packages/native1.0.5 source digest cannot be reproduced, stop and propose the exact discrepancy before compute. OS/CPU/platform identity will intentionally differ; freeze the actual RAL identity for both arms and require exact parity within RAL, not bitwise agreement across CPU architectures.

Choose the same retained task filesystem for both arms and record its type/mount; full-fit timings include its checkpoint/output cost. No claim that node exclusivity isolates shared filesystem or OS noise. Keep both original laptop artifacts and all new RAL raw data. Generic hpc/sync excludes search_internal, so recovery checkpoint transfer needs an explicit scoped read-only pull in addition to the normal output pull; verify hashes. Nothing is removed from RAL during this task.

Before submission: new source committed/clean, exact-head CI green, environment and live scheduler checks complete, record fresh Heart readiness under the existing override, and bind the job script to the approved experiment limits. Submit at most one job after this amendment is approved and SSH access is restored. No background polling subscription; inspect job state in the active chat and leave a concrete job/receipt handoff if pending.

### Current blocker and authorization boundary

Read-only SSH through the configured aliases failed on2026-11-10 before reaching RAL. Explicit BatchMode on both hops returned `njn86@finan.ncl.ac.uk: Permission denied (publickey,password,keyboard-interactive).` No remote inventory was obtained, no remote files changed and no job submitted. Do not edit SSH configuration/keys or request passwords in chat; the user needs to restore the existing jump-host authentication.

The existing pilot code and145tests/CI remain valid at83530ce; the RAL adapter above is not implemented or validated yet. Proposed resource allocation is not a discovered available node. Approval is requested for this amendment, not a repeat of the already-granted direction to move timing to RAL. User workspace AGENTS.md: "Plan before editing. Present a plan and wait for explicit user approval before editing any source, workspace script, notebook, test, or release file." The original plan also explicitly excluded HPC. Source/submit edits wait for amendment approval; remote execution additionally waits for working SSH.

Planning route: continuation of issue16, workspace-only transport/admission change; no new library claim or scientific model change. Phases are adapter/tooling validation, remote staging/discovery, then one correctness-gated RAL pilot. Brain classification is performed in-session against the existing active plan. Memory nested-sampling context supplied no cluster-specific procedure; the workspace RAL policy and project hpc docs govern deployment. Slurm references: https://slurm.schedmd.com/sbatch.html#OPT_exclusive and https://slurm.schedmd.com/srun.html#OPT_cpu-bind (live site configuration still requires verification).

## RAL amendment approval

Live human selected "Approve the RAL amendment". Implementation and one submission after access/validation gates are authorized with the stated exclusive ral/four cores/8GiB/35min scheduler allocation and18children/120s/4GiB/1800s scientific caps. User then confirmed the existing SSH route and will restore authentication. No new permission is required merely to resume those authorized steps. Outside Pulse and human merge remain binding.

## RAL implementation handoff

Implemented352eafb in existing draft PR17, basePR13: allocation/cgroup/core-binding admission, explicit RAL protocol/runtime reference, one-job wrapper and supervised affinity/budget cleanup.190tooling tests, Ruff/format, shell syntax and unchanged catalogue validation pass; author review only. Logs under task .session/ral-tests-final.log and readiness-ral.json. RAL metadata tests are synthetic; live version/schema/runtime validation remains mandatory. Existing source pins and scientific settings unchanged.

The configured SSH route still fails at jump_finan before RAL. User confirms using the same route and will restore authentication. No remote writes, probe jobs or scientific children launched. The single approved submission is unused. Next: read-only discovery, reconcile runtime reference, isolated remote source worktrees and output/ral-environment.sh staging, verify exact-head CI, then hpc/sync submit --cpu submit_nautilus_training_pool once. Record job ID before any polling. Do not resume laptop quiet admission or request repeated authorization for these approved steps.

Fresh Heart2026-11-10T19:52:15.059564+00:00 RED: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "autocti_workspace: Smoke Tests failure on main". Existing experiment-specific development override retained, outside Pulse and human merge.

Exact-head Actions42890122136 passed all tooling, Ruff, catalogue and link steps for352eafb1ed77813afec36a16d4dfc065f4d65757. No remote run has been attempted.

## RAL access and staging update

The human supplied the working WSL agent socket; per-command SSH_AUTH_SOCK restored access through the existing euclid_jump/jump_finan route without changing keys or configuration. Read-only discovery: Slurm22.05.11, ral OverSubscribe=NO, CR_CORE_MEMORY, task/affinity+task/cgroup, ConstrainCores/ConstrainRAMSpace enabled. Live legacy TRES resource field is now supported at107ec1c7809cd7f4741e3ab48e62e096d3434320 with strict CPU/memory/GPU checks intact;194tests, Ruff/format and exact-head Actions42898804169 all pass. Actual allocation affinity and cgroup enforcement remain to be witnessed.

An isolated task directory under /mnt/ral/jnightin/profiling/autofit_profiling_wt/nautilus-spawn-training-pool holds producer and pinned Fit/Nerves checkouts. Initial local Nerves clone lacked the old tree; fetching its exact revision into the isolated clone resolved that staging error. Shared sources/runtime were not modified. Shared Python3.12.4 and packages differ, so a separate Python3.12.10/pinned runtime is being staged. No job or scientific child submitted; one-job authorization remains unused. Preserve staging logs01/02.

Fresh Heart2026-11-10T20:50:57.253679+00:00 RED: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure"; "autocti_workspace: Smoke Tests failure on main". Existing task-wide development override and explicit RAL amendment remain applicable; no release/merge/CI bypass.

## Human bedtime pause

Human: "going bed get this into a resumeable state". Stopped the task-owned RAL Python installer and staging shell; both verified absent. No Slurm job or scientific child submitted and no watcher armed. Clean producer107ec1c and pinned dependency checkouts are retained. Isolated Python3.12.10 extraction was still incomplete;88 binary-package pins resolve, while two pure-Python utilities are staged separately. Full executable handoff: task .session/RESUME.md and Science scratch nautilus_optimizations_2026-11-10/training/RESUME.md. The handoff corrects the staging inventory key to reference_distribution_versions. Resume environment setup, import/provenance verification, then the already-authorized single job; do not request duplicate approval. Outside Pulse; human merge.

## Resume check — 2026-11-11

The human resumed work. The saved /tmp/ssh-XXXXXXLVzNFO/agent.518 socket no longer exists and Codex has no inherited SSH_AUTH_SOCK. Existing-route BatchMode SSH failed at jump_finan before RAL. Asked the human for the current socket path from their working WSL terminal; no credentials/configuration changed. No new remote writes or job submission.

Producer107ec1c and its exact-head CI42898804169 remain unchanged/green. Prepared and shell-syntax checked .session/ral-resume-stage-03.sh for the already-approved runtime continuation; it has not run. It installs exact pinned versions and performs import/provenance validation only, with no sampling/submission.

Fresh Heart2026-11-11T08:47:27.525797+00:00 RED: "autocti_workspace: Smoke Tests failure on main". Existing experiment override retained. Next: receive current agent path, verify SSH and remote state, finish runtime staging, then submit the single already-approved job after all gates. Outside Pulse; merge human.

## RAL staging resumed with working agent

2026-11-11: human provided a current WSL SSH agent path. Explicit-proxy and ordinary euclid_jump access work. No previous pilot receipt or queued training job was found. Partition ral is up with5idle nodes and OverSubscribe=NO. Runtime-only staging-03 resumed exact Python3.12.10 installation,90 pinned distributions and then import/provenance checks. No sampling or sbatch in this script. Shared filesystem extraction is slow but advancing. Local ignored hpc/sync.conf points only to the isolated task. Scientific authorization remains unused; retain all limits and stop-on-first-failure rule.

## RAL runtime installed; validation diagnostics

2026-11-11: diagnostic staging04 installed exact Python3.12.10 (10m33s),88 binary packages (14m58s preparation,17m06s installation). An SSH interruption ended that connection during utility setup; reconnected and verified no remaining task-owned installer, then staging05 confirmed the two utility pins using the retained environment. SSH keepalives and remote logs now preserve diagnostics.

The first imports/source/inventory check timed out at600s without a pass receipt. Validation06 adds phase markers and60s Python stack dumps under a1200s setup-only cap. It performs no sampling or neural training. Root cause is not yet established beyond observed NFS waits. Do not submit until this gate passes, and do not relax scientific limits. All setup logs retained. Producer107ec1c/194tests/exact-head CI unchanged. Latest Heart2026-11-11T09:53:07.387383+00:00 YELLOW: "PyAutoArray: open PR 7d old"; existing scoped development authorization remains, outside Pulse and human merge.

## Proposed node-local runtime cache amendment — 2026-11-11

Status: awaiting explicit plan approval. No scientific RAL job has been submitted; the existing single-job authorization is unused. This amendment changes runtime/source placement and the job startup procedure, while retaining the approved measurement and resource limits. Outside Pulse; human merge.

### Evidence

The isolated NFS environment now contains Python3.12.10 and the pinned packages. Python setup took10m33s;88 binary packages took14m58s to prepare and17m06s to install. The two pure-Python utilities subsequently passed the installer check. An SSH interruption is retained separately; keepalives and remote logs were added.

The first import/provenance check timed out600s without a pass receipt. A phase/stack diagnostic then exited139 during an early provenance-module import; the crash cause is unresolved. A separate isolated (-I -S) import probe passed its standard-library portion, then reached180s before completing the baseline-module import. Import timings included json37.325s cumulative, re26.467s cumulative and zipfile37.209s cumulative. Python processes were observed waiting in NFS RPC calls. These are setup observations on the login host, not sampler performance measurements, and do not prove the cause of the diagnostic crash.

Read-only discovery shows /mnt/ral is nfs4; /tmp on the login host is local ext4 with about42,509MiB available. Compute-node local storage remains to be checked inside the single approved allocation; no probe job is authorized.

### Concrete implementation

1. Continue issue16 / draft PR17 on feature/nautilus-spawn-training-pool. Preserve current producer107ec1c and every previous setup log/artifact. Make no production library, shared runtime, Pulse, sampling-setting or default change.
2. Prepare a private, uniquely named local staging cache on the RAL login host. Reproduce the same Python3.12.10 build,90 third-party version pins, native Nautilus1.0.5 source digest, and clean pinned Fitbdb7af0 / Nerves9b204c9 source checkouts. The producer checkout must be the new exact validated PR head. No sampling/neural training on the login host. Validate imports, source identities and inventory from local storage before any submission; if imports still fail or crash, stop and report rather than declaring the cache a cure.
3. Produce a retained, checksum-addressed runtime/source artifact and manifest under the existing NFS task directory. Include exact package/native-source inventories, producer/library revisions, artifact checksums, and only the inputs needed to reproduce the local environment. Validate a local restore without scientific evaluation. Keep the existing NFS installation and failed setup evidence. No dependency or Python-version substitution.
4. Extend hpc/batch_cpu/submit_nautilus_training_pool with a bounded local-cache bootstrap helper under hpc/tools/. Submit through the existing hpc/sync interface. Run bootstrap and experiment within the same numbered srun step bound to the four physical cores. Use a fresh task-owned local directory on the allocated node; verify filesystem/capacity, artifact checksum, safe extraction, source revisions/cleanliness, exact versions/native digest and allocation identity. Rebuild only environment path wiring from retained binary/wheel inputs; no internet download, native compilation, library-source patching or sampling during bootstrap.
5. Keep the authoritative receipt directory, checkpoints and every scientific output on the original retained NFS task filesystem. Both serial and pool arms use the same local runtime/source cache and the same NFS output filesystem. Record both filesystem identities. Full-fit/workflow timing continues to include NFS checkpoint/output cost; do not claim it is a purely in-memory CPU benchmark.
6. Preserve one exclusive ral node, one task/four bound physical cores,8GiB and35minutes. Maximum18 scientific children,120s/4096MiB per child,1800s scientific budget, six correctness checks before twelve timing cases, exact parity/recovery and stop-on-first-failure remain unchanged. Bound bootstrap within180s from wrapper entry and reserve120s cleanup margin; bootstrap failure starts no scientific cases. Enforce the original scientific deadline independently. No extra job, retry/requeue, GPU or alternate partition.
7. Retain bootstrap/failure receipts directly on NFS. After all owned experiment processes stop, remove only the newly created node-local cache using ownership/path guards; retain the runtime artifact, original NFS environment, source worktrees and all scientific data. This explicitly narrows the original "Nothing is removed from RAL" rule for disposable local caches only. Any failure to establish identity, binding, memory, time, storage, extraction safety or cleanup is reported; never weaken a gate to make the job run.
8. Add meaningful tooling tests for artifact tampering, unsafe extraction/path ownership, missing local storage, insufficient time/memory, source/package mismatch, bootstrap failure before sampling, exactly one submission/step, unchanged output filesystem and guarded cleanup/exit status. Run required tests/Ruff/catalogue checks, inspect exact-head CI and refresh Heart. Use the already-authorized single submission only after the amended implementation and runtime gates pass. Merge remains human.

### Approval boundary

The workspace AGENTS.md requires: "Plan before editing. Present a plan and wait for explicit user approval before editing any source, workspace script, notebook, test, or release file." The previous approved plan places clean worktrees in the retained profiling task area and does not describe a node-local bootstrap or disposable cache cleanup. This proposal makes that change explicit before editing the job wrapper/helper. Approval is for this runtime-placement amendment, not an additional scientific attempt or relaxed budget.
