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

Status: approved by live human on 2026-11-11 ("Approve cache amendment"). No scientific RAL job has been submitted; the existing single-job authorization is unused. This amendment changes runtime/source placement and the job startup procedure, while retaining the approved measurement and resource limits. Outside Pulse; human merge.

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

## Runtime cache amendment approved

Live human selected "Approve cache amendment". Resume the existing workspace task and PR17; implement/validate the saved amendment and use the original single submission only after all gates. No new scientific attempt or relaxed limit is authorized. Outside Pulse; merge human.

## Local runtime and cache implementation

Producer c243ef676ffa15fc9e4808abc104a93c70bc8145 implements the approved local artifact/restore/validation/cleanup amendment.229 tests, Ruff/format, shell syntax and unchanged catalogue pass; author review. Login-host local runtime validation08 passed full provenance in7.35s with all90 third-party pins/native digest, zero sampling/training. Artifact build/fresh restore09 are active before the one authorized submission. No job submitted. Latest Heart receipt2026-11-11T10:45:45.346227+00:00 RED: "release validation FAILED (stage integrate)"; existing experiment development override applies.

Fresh artifact09 restore passed:49.95s bootstrap,53.29s including cleanup, sampling_started=false, ext4 runtime/NFS scientific output verified. Exact-head CI43015855847 passes every step. Retained NFS checkout final staging remains before the single submission.

## Final staging blocked by NFS — 2026-11-11

Final staging exited124 at600s while `git status --porcelain` waited in an NFS RPC reading hpc/batch_cpu. It had not reached the checkout update or writing the six submission exports. No sbatch/scientific child ran; no pilot output/submission environment/index lock remained in the follow-up check. Existing one-job authorization remains unused. Resume .session/ral-cache-final-stage.sh only after inspecting current remote state and reliable NFS access; retain all runtime/setup evidence, and never relax source/runtime/allocation gates. No cache rebuild or new compute approval is needed merely to resume the same approved staging/submission. Producer c243ef6 and CI43015855847 remain valid; no speedup claim, outside Pulse, human merge.

## RAL setup completed and first job submitted — 2026-11-12

Recovered the new user-owned SSH agent automatically by matching previously supplied public-key fingerprints; no keys/configuration changed. NFS checks and the retained clean checkout update passed today. Exact c243ef6 producer, artifact and six frozen submission inputs are staged; CI43015855847 remains green. The task-internal staging guard now captures Git status before testing its output, so a failed Git command cannot be mistaken for a clean tree; bounded read-only status avoids optional index refresh writes.

Submitted once through hpc/sync: job415132. Original single-job approval is now USED. Watch/collect this job only; no second submission, replacement or relaxed limits. Outside Pulse; human merge.

# RAL setup repair plan — 2026-11-12

Status: approved by live human2026-11-12 ("Approve diagnostic and corrected pilot"). Outside Pulse; human merge.

## Established facts

The chat did not inherit SSH_AUTH_SOCK and the saved socket expired. We recovered the live user-owned agent by matching the public-key fingerprints the human previously supplied; authenticated access through the existing route works. No private keys or user SSH configuration were changed. Future resumes should discover a matching live socket before asking the user for one.

NFS checks and final staging now pass. The retained producer is clean at c243ef676ffa15fc9e4808abc104a93c70bc8145, matching the already-validated artifact;229 tests and exact-head CI43015855847 pass. The task-local staging script was hardened to capture Git status with an explicit failure exit and a30s timeout, rather than treating failed command output as a clean tree.

The original approved job415132 ran on euclid-ral-compute-1 and failed after2s at the storage guard. No sampling/training started. Bootstrap elapsed0.82s, cleanup complete. The guard rejects scientific-output mount types other than nfs/nfs4, inferred from the login host. The same scripts and failure receipts are accessible from login and compute, but the actual compute mount type was not retained: the guard raises before returning its filesystem snapshot. Root cause beyond this unjustified type assumption remains unverified.

Read-only compute SSH was attempted using the scheduler-reported hostname and existing local agent through the existing jump route; it rejected public-key authentication. First-use public host identity was retained only in task-owned known-hosts files; no global SSH config or key was changed. Do not bypass the denial or submit another job under the consumed original approval.

## Proposed bounded work

1. Submit exactly one setup-only diagnostic on partition ral: one node/task/CPU,256MiB,60s, no exclusivity, GPU, array, requeue, sampling, likelihood evaluation or neural training. Execute system utilities/system Python only. Retain exact commands, job ID, stdout/stderr and final accounting in a new diagnostic directory.
2. Record the compute node's findmnt JSON and mountinfo for /tmp and the existing retained task/output path, hostname, task marker/content identity, and scheduler/cgroup context. Write only diagnostic receipts to the original retained task directory and confirm they are visible from login. Do not read another campaign's data or change its jobs.
3. Correct the existing bootstrap to validate the observed shared retained-storage identity rather than assuming the login-host protocol label describes compute-node mounts. Keep the exact retained output location and both arms on the same filesystem. Capture observed storage details before any rejection. Do not broadly accept arbitrary local disks or silently move scientific outputs. If the diagnostic cannot establish that the output is the same retained shared storage, stop and report.
4. Keep the correction in the existing branch/PR17 and issue16. Add regression tests using the actual mount records for accepted shared storage and rejected wrong/ephemeral storage, plus failure-receipt coverage. Preserve source/runtime/build pins, full inventory checks and allocation gates. Use a fresh explicit attempt02 claim/output directory so job415132 and every earlier artifact remain intact; duplicate execution of an attempt must still fail.
5. Complete tests/Ruff/format/catalogue/shell checks, author review, exact-head CI and Heart under the existing scoped development override. Rebuild and retain the artifact at the corrected exact producer, validate a fresh restore without sampling, then stage frozen inputs. Preserve every prior environment, artifact and log. Routine implementation fixes and setup-only validation within this plan need no further approval.
6. Once all gates pass, submit exactly one corrected scientific pilot: exclusive ral node, one task/four bound physical cores,8GiB,35min; bootstrap180s, cleanup reserve120s;18children maximum,120s/4096MiB each,1800s science total, six correctness children before twelve timings. Same four native networks, source/package pins, scientific configuration, retained output filesystem and serial/pool comparison. Stop on first failure; no further scientific job, retry/requeue or replacement. Retain raw data and final accounting. Merge stays human; no Pulse ingestion or release.

## Approval boundary

The previous approved plan says: "No extra job, retry/requeue, GPU or alternate partition." Its one job was415132. The workspace AGENTS.md also says: "Plan before editing. Present a plan and wait for explicit user approval before editing any source, workspace script, notebook, test, or release file." This amendment authorizes the specific diagnostic, informed guard correction and one corrected pilot together. It does not authorize open-ended jobs or changing scientific limits.

## Storage diagnostic and correction

Diagnostic415135 completed0:0 in1s using1CPU/256MiB. The compute mount is Ceph; login sees NFS4. Two existing file hashes matched between both hosts and compute-written receipts were visible from login. Runtime caches use local ext4. No science ran.

Correction47857ec3995d6c924d2c8acb529d06585bd069c8 freezes both observed mount identities, the retained root and immutable witness hashes in a separate checksummed storage contract embedded in runtime artifact schema2. It rejects wrong/local/ephemeral volumes and path/witness changes; failure receipts now preserve mount observations before rejection. Wrapper explicitly claims fresh attempt02; original job415132 remains intact.240 tests, Ruff/format, shell and unchanged catalogue pass, author review. Artifact10/fresh restore active; corrected pilot approval unused. Outside Pulse/human merge.


## Corrected RAL pilot submitted — 2026-11-12

Fresh artifact10 restore passed in34.6s (35.9s including cleanup), no science, cache removed. Exact producer47857ec and eight frozen inputs staged; old environment retained as ral-environment-attempt01.sh.240 tests and exact-head CI43202895306 green. Submitted exactly once through hpc/sync: job415136. Corrected authorization now USED; no replacement/retry/requeue. Initial live compute bootstrap passed23.92s, runtime validation and preflight passed, scientific experiment started. Original job415132 and diagnostic415135 retained. Outside Pulse; merge human.

Fresh authoritative Heart 2026-11-12T10:38:39.599379+00:00 RED: "PyAutoNerves: 2 commit(s) behind origin"; "PyAutoFit: 2 commit(s) behind origin"; "PyAutoLens: on branch feature/mge-feature-review (not main)"; "PyAutoLens: 2 uncommitted source change(s)". Existing experiment-specific development override applies; source/runtime/CI gates passed, no release or merge authority. Full receipt retained in .session/readiness-corrected-presubmit.json.


## Corrected RAL outcome — job415136

Job415136 FAILED1:0 after167s; compute bootstrap23.92s passed, cleanup complete. Pilot140.74s, six correctness children passed (exact four-network parity and both crash/resume checks), first serial timing child failed post-fit checkpoint verification, eleven cases unrun, zero valid timing pairs. Both recovery results exactly match control:16,300 likelihood evaluations/ESS10020.771588733165. All child descendants reaped; peak sampled group RSS557.80MiB; max child25.71s. All raw evidence20,933,974bytes retained locally and remotely, plus original415132 and diagnostic415135. RAL setup/storage/runtime/allocation are now witnessed working; no speedup claim.

Failure is in harness performance() line374: reopened Sampler uses identity prior lambda x:x, whereas the live fit uses Gaussian priors. Native posterior() transforms unit coordinates with its current prior, so the exact hash compares different coordinates. Read-only checkpoint/samples.csv inspection: transformed coordinates match within1.3322676295501878e-15, likelihoods exactly equal, checkpoint hash65eaf581048807ea20bc198e1888b518f6b12a09aeb0cde429474fd5229508df unchanged. No sampling/training/likelihood calls. This supports the prior mismatch diagnosis, not retroactive exact live-state parity. No source correction or new job after failure.

Corrected pilot authorization is consumed. Task waits for human decision on the bounded plan below. Outside Pulse; PR17 remains draft/open and merge human.

# Checkpoint prior verification correction — proposed

Status: awaiting explicit approval for the source correction and one fresh pilot. Outside Pulse; merge human. RAL job415136 consumed the corrected-pilot allowance; no extra job is authorized.

RAL setup is now validated. Job415136 passed actual storage/runtime/allocation checks and six correctness children, then stopped at the first serial timing case because the verification harness reopened its Gaussian-prior checkpoint with an identity prior. It therefore hashed unit-cube points against physical points. Offline inspection of retained checkpoint/samples.csv found matching shapes, identical likelihoods, and Gaussian-transformed coordinates matching within1.33e-15; no sampling/training/likelihood calls, checkpoint bytes unchanged. This diagnoses the coordinate mismatch, not an exact live-state parity pass.

## Concrete correction and validation

1. In training_pool_benchmark.py performance(), construct the read-only reopened Sampler using the captured original sampler.prior instead of lambda x: x. Preserve the original constructor flags/configuration. Keep the likelihood callback forbidden and never call run(). Do not change native Nautilus, installed libraries, random seeds, sampling, checkpoint writes or tolerances.
2. Add a non-identity-prior regression that fails under the old reopen behavior and verifies all posterior arrays and state, zero likelihood/run calls and unchanged checkpoint bytes. The existing exact byte-hash gate stays strict; the offline1.33e-15 observation is not permission to weaken it.
3. Before compute submission, validate against the retained failed-case checkpoint without sampling/training. Check prior/coordinate semantics and compare raw stored posterior arrays/weights/likelihoods. The original live object was not retained, so no offline check may claim retroactive live-object exact parity. If another difference emerges, diagnose it before requesting/using scientific compute.
4. Keep source/evidence in existing issue16/PR17, retain all previous attempts. Use an explicit fresh attempt03 output claim with duplicate refusal; rebuild frozen artifact at the new clean producer. Require tests, lint, shell checks, exact-head CI, Heart under existing scoped override, frozen runtime/storage checks and a fresh restore before submission.
5. Submit exactly one new exclusive ral job: four bound physical cores,8GiB,35min;180s bootstrap,120s cleanup margin;18children maximum,120s/4096MiB each,1800s scientific total. Six correctness cases precede twelve timings. Same D5/D10 seeds, four native networks, two spawn workers versus serial, same retained output filesystem. Stop on first failure; no retry/requeue/replacement. Retain raw data/accounting, outside Pulse, merge human.

## Why approval is needed

The approved RAL setup repair plan authorizes “exactly one corrected scientific pilot” and says “Stop on first failure; no further scientific job, retry/requeue or replacement.” Job415136 used that allowance. This new prior-verification correction and fresh job extend that plan.


## Prior correction approved — 2026-11-12

Human selected "Approve correction and one fresh pilot". This authorizes the saved prior-preservation correction and ONE new same-limit RAL pilot after all gates. Outside Pulse; merge remains human. New attempt03 allowance UNUSED until sbatch; earlier415132/415136 retained.

Implemented prior-preserving verify_checkpoint at eb88e0c; non-identity-prior regression fails under old code and passes corrected;244 tests pass. Offline pinned-runtime checkpoint reconstruction validates all raw posterior arrays exactly, prior negative control differs, checkpoint unchanged, zero sampling/training/likelihood calls; does not claim retrospective original-live-object parity. CI43206309695 caught an unrelated procfs ESRCH race in existing cleanup test; fixing that test before new exact-head CI/artifact. Artifact11 at eb88e0c is setup-only and will be retained; final producer artifact/restore required before submission.


## Prior-corrected pilot submitted

Job415139 submitted ONCE via hpc/sync at db516b50cd8d6ea1301704bc39e8d14819024968.244 tests and CI43206509078 pass, author review; offline posterior reconstruction exact with zero sampling/training/likelihood, old identity prior rejected. Artifact12 runtime2.90s, fresh restore51.32s/52.71s including cleanup, zero science. Final staging preserved attempt02 environment; new attempt03 output claim. New single-job approval is now USED; no resubmit/requeue/replacement. Same18children/120s/4GiB/1800s, exclusive ral4boundcores/8GiB/35min. Outside Pulse; human merge. Heart2026-11-12T11:09:22.974524+00:00 RED under existing scoped override: "PyAutoFit: 2 commit(s) behind origin"; "PyAutoArray: 2 commit(s) behind origin"; "PyAutoGalaxy: 2 commit(s) behind origin"; "PyAutoLens: 2 commit(s) behind origin".


## Approved pilot complete — human review

Job415139 COMPLETED0:0 in591s at measured producerdb516b5.18/18 cases passed; six exact posterior/state/model/target timing pairs, both recovery controls and all checkpoint reopens passed. Bootstrap23.56s, pilot565.95s, max child47.92s/594.50MiB; cleanup complete and all descendants reaped.153,104,897bytes raw retained remotely/task-locally/human archive. Median paired workflow:5D17.9% faster(1.217x),10D2.4% slower(0.976x); median sampler speedups1.393x/1.038x. Mixed three-seed pilot, no production default change or30D claim. Report-only producer commit798d743 in PR17; measured producer CI43206509078/244tests green. Outside Pulse; human merge; no more compute.

All approved implementation and compute finished. PR17 and issue16 remain open pending human review/merge; unmerged basePR13 remains unchanged. Fresh-run allowance consumed, no retry/requeue/replacement. Human report: Science/scratch/nautilus_optimizations_2026-11-10/training/RAL_RESULT.md; raw archive/checksums under ral_setup_diagnostics/job415139/.


# 10D training-cost diagnosis — proposed implementation and RAL plan

Status: approved by the live human on 2026-11-12: “Approve bounded diagnostic study”. Implementation and one gated RAL job authorized despite Heart RED; allowance consumed by job415179; see terminal result below. This is a continuation of nautilus-spawn-training-pool, issue autofit_profiling#16 / PR#17. Outside Pulse. Tier: judge — merge mode: human /prm.

## User request

> Can we investigate why faster training isn’t translating into faster 10D fits? Keep it outside Pulse and leave merge for me.
>
> continue

## Evidence and questions

The completed job415139 at measured producerdb516b5 passed18/18 cases and all six exact timing pairs. In10D, training saved1.73/2.22/2.39s by seed; pool lifecycle added1.69/1.59/1.54s. Other sampler time added0.82/0.34/4.67s and other fit time changed−0.06/−0.01/+2.45s. Pooled networks consumed39–48% more aggregate CPU time despite identical trained-model/iteration digests. Unequal worker workloads add0.79–1.02s beyond an even-work lower bound; only0.050–0.053s of parent training lies beyond the busiest-worker bound. That is not a direct IPC measurement and cannot exclude overlapping contention. The read-only report is retained in Science scratch training/10d_training_diagnosis_2026-11-12/.

Questions: (1) does a single spawned worker show the same CPU cost increase, or does it emerge with simultaneous workers? (2) does distinct-core placement help? (3) which exclusive phases explain seed2’s extra non-training time? Frequency/cache/BLAS differences are hypotheses, not established causes.

## High-level plan

1. Capture the actual training inputs from one serial10D/seed2 fit, checking its posterior/state/model digests against the retained serial reference. Treat this capture as correctness/data collection, not a performance baseline.
2. Replay that identical corpus in four contexts: parent process, one spawned worker, two spawned workers with shared affinity, and two spawned workers assigned distinct cores. Three interleaved repetitions per context; exact model checks precede interpretation.
3. Run two serial/pool pairs for the full10D/seed2 fit with the same lightweight exclusive wall/CPU phase timers on both arms. Separate geometry, prediction, native checkpoint writes and final output costs, with an explicit residual.
4. Retain task timing, worker CPU time, placement and native-library metadata; preserve all scientific settings and installed libraries. Report uncertainty rather than assigning hardware causes without evidence.
5. Publish a diagnostic report in the existing development PR. Keep raw data and every previous attempt, stay outside Pulse and leave merge to the human.

Tier: judge — merge mode: human /prm.

## Frozen proposed compute matrix

Exactly one exclusive partition=ral node job: one task, four bound physical cores,8GiB,35-minute scheduler cap;180s bootstrap from wrapper entry and120s cleanup reserve. At most17 child processes,120s and4096MiB per child process group,1800s aggregate scientific budget including admissions/verification. The same guards and stop-on-first-failure rule apply. No replacement, retry, requeue, GPU or alternate partition. Failure of a resource/source/parity invariant ends the job and marks remaining cases unrun.

The17 children are:

- C: one serial10D/seed2 wrapped fit capturing all actual native neural-training inputs and reference outputs.
- Twelve replay children: three rounds of four arms. P=parent, S=one spawned worker, U=two spawned workers with the inherited four-core mask, B=two spawned workers each pinned to a different core within that mask. Frozen order: round0 P,S,U,B; round1 B,U,S,P; round2 U,P,B,S. Each child replays the entire captured sequence once with fresh pool lifetime. This balances positions partially; three rounds are not a fully balanced design and do not establish statistical significance.
- Four instrumented full-fit children in ABBA order: serial, two-worker shared-affinity, two-worker shared-affinity, serial. They form two matched pairs with reversed order. Each starts fresh; native seeds/settings match the retained10D/seed2 case. The bound-worker arm is a replay diagnostic only, not a changed production default.

Thus at most five new sampler fits (one capture plus four traced fits). The12 replay children perform training only: no likelihood evaluations, adaptation or Sampler.run. The capture is a full ordinary fit under the same120s limit; its additional corpus logging makes its timing ineligible for a performance comparison.

## Scientific invariants and provenance

Retain Fitbdb7af0e9c339ad07850679fd6ac168aacc7d18c, Nerves9b204c90c2ce05c5bb0cf3e9800ed13f005c6c56, native Nautilus1.0.5 and the existing full pinned runtime inventory. Producer is a new exact clean commit. Four native networks, original architecture/stopping, ordered per-network seeds0..3, one native numerical thread, serial likelihood and sampler adaptation.10D,seed2,400live points,batch100,ESS10000,n_shell1,discard_exploration=True, no synthetic work, native checkpointing. Search corner plots disabled equally; other fit output unchanged.

Capture raw inputs at the NeuralNetworkEmulator.train boundary, along with array dtype/shape/order and immutable call order/settings, corpus checksums and exact output model digests. Use non-object NumPy arrays and JSON metadata (allow_pickle=False); cap retained corpus at64MiB. Refuse empty/truncated/oversize/inconsistent corpora. Compare final capture posterior/state, likelihood count, target and ordered model digests with job415139’s retained10D/seed2 serial receipt before replaying.

Every replay executes the unchanged native training method on the same inputs and settings. Exact normalization/weights/biases/iteration digests must match each captured model; inputs remain unchanged. Prevent sampling/likelihood entrypoints. Record zero forbidden calls. Load and verify corpus outside the training timer; use equal loading/copy policy across arms. Parent and shared-affinity workers inherit the same four-core allocation; bound workers get two distinct allowed cores. Record actual placement and affinity, do not infer physical exclusivity beyond verified scheduler/kernel evidence.

For full fits, verify exact posterior/state, likelihood counts, model digests, target and read-only checkpoint reopening against the retained reference and paired arm. The existing prior-preserving reopen and forbidden-likelihood check remain strict. No relaxed float/hash tolerance, altered samples or extra timing likelihood calls.

## Implementation files and behavior

Existing producer: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-spawn-training-pool/autofit_profiling; branch feature/nautilus-spawn-training-pool; current head798d743375579b623f1f463a02fc48f8afa79c06. Clean. Existing Mind sync branch sync/nautilus-training-pilot-record. Conflict guard found no competing claim (only old unregistered evidence-worktree warnings). PR17 remains based on unmerged PR13; do not retarget or merge.

- New scripts/analytic_gaussian/nautilus/training_diagnostics.py: immutable versioned17-child protocol, corpus capture/validation, replay matrix and traced fit driver, source/allocation/budget admission, durable terminal receipts and report export. Reuse the existing target/configuration/retained-checkpoint helpers while preserving the original18-case benchmark protocol unchanged.
- New scripts/misc/profiling/nautilus_training_diagnostics.py: diagnostic-only ordered transport for0/1/2workers, optional fixed distinct-core assignment, corpus observation and scoped phase wrappers. Reuse native train_network/model_digest and existing resource helpers. Do not broaden the old TrainingTransport's approved0/2-worker contract or alter installed libraries.
- Replay metrics: per-network monotonic start/finish, process CPU time, PID and observed CPU, input/result size estimates, dispatch/collection boundaries, pool startup/teardown, aggregate CPU and overlap-aware worker occupancy. Record full threadpoolctl library/version/path/thread data and relevant thread environment in parent and workers; validate one native thread. CPU frequency/cache/steal counters are optional observational metadata where readable, explicitly unavailable otherwise; no privileged profiling or system configuration changes. Only fixed in-allocation CPU affinity differs in armB.
- Full-fit metrics: lightweight nested exclusive wall and parent-process CPU timers around Sampler.run, evaluate_likelihood (batch-level, including prior/dispatch), sample_shell, write/write_shell_update, NautilusBound.compute, neural train/predict, and existing PyAutoFit pre/post-fit and SearchUpdater output methods. Separate samples output, latent samples, summary/profiling and visualization. Avoid per-likelihood event traces. Worker CPU is a separate channel; never sum overlapping worker wall time into parent elapsed time. Retain inclusive timestamps and residuals, validate accounting instead of silently clamping negative totals. Restore every patched descriptor in finally. These traced fits diagnose phases; instrumentation overhead is included and no uninstrumented-speedup claim is permitted from them.
- hpc/tools/build_nautilus_runtime.py and nautilus_runtime_cache.py: add an explicit allowlisted diagnostic experiment identity tied to its entrypoint/wrapper and manifest, checked during build/restore before execution. Preserve the original training-pool default and exact runtime/storage checks. No arbitrary command or user-supplied executable argument. New diagnostic job uses a fresh dedicated output claim, not a reset of attempt01/02/03.
- New hpc/batch_cpu/submit_nautilus_training_diagnostics: same exclusive ral allocation and limits, new frozen experiment identity and unique output/training-diagnostics-ral-01 claim, separate staging environment, duplicate refusal and cleanup. Do not overwrite original submission environments or claims.
- scripts/misc/test/test_nautilus_training_diagnostics.py plus focused runtime/allocation tests: matrix immutability; wrong/tampered/mutated corpus; wrong model/order; forbidden sampling; one-worker and core-assignment contracts; missing worker/library metadata; descriptor restoration after failure; nested wall/CPU accounting; aggregate budget/timeout/group cleanup; experiment manifest mismatch; duplicate submission-claim refusal; original benchmark/runtime default regression.
- experiments/nautilus_spawn_training_pool/diagnostics_10d/: versioned protocol, compact evidence and report. No catalogue, Pulse registry, publication board, production default or library changes.

## Runtime gates and retention

Before the one submission: source committed/clean, appropriate tooling suite and lint/format/shell/catalogue checks pass, author review recorded honestly, exact-head CI green, fresh authoritative Heart receipt under the task-scoped development override, full pinned runtime validation, new checksummed artifact and a fresh zero-sampling restore pass. Use hpc/sync for one submission and record its job ID immediately; ambiguous submission outcome must be resolved by accounting, never blind retry.

Keep runtime/source copies node-local and scientific outputs/corpus on the same witnessed shared storage (NFS view on login, Ceph on compute). A verified read-only corpus copy may reside in the guarded task cache during replays, equally for every arm; retain the authoritative shared copy and hashes. Cleanup only the newly created per-job cache. Preserve job415139 and every earlier job, artifact, source checkout, checkpoint and raw-data bundle. No edits to shared installed environments or unrelated jobs.

Stop after completion/report or first failure. Judge evidence once; do not add a persistent watcher or expand repetitions. A further job or scientifically changed protocol needs a new human decision. Merge/close-out remains human and no release is authorized.

## Readiness and approval boundary

Published entry feed: Heart YELLOW, updated23h ago. Authoritative recorded receipt2026-11-12T11:24:54.298644+00:00 is RED: "PyAutoLens: on branch feature/pixelization-feature-review (not main)"; "PyAutoLens: 2 uncommitted source change(s)". Existing task-scoped override permits this planning continuation; request explicit approval for this new implementation and17-child compute extension despite RED. Source/runtime/CI gates remain mandatory and the unrelated canonical checkout is not a measured dependency.

The workspace AGENTS.md requires: "Plan before editing. Present a plan and wait for explicit user approval before editing any source, workspace script, notebook, test, or release file." The preceding single fresh-pilot allowance was consumed by415139. This proposal is the concrete new scope to approve; no implementation or scientific compute has begun.


### Planning classification and phase boundaries

Brain's automated feature decision scanned the accumulated historical task and returned generic too-large/public-API warnings. Scoped judgment for this extension: workspace-only experimental measurement; no public library API changes. Implement in separately reviewed commits: (A) immutable capture/replay protocol and corpus/transport tests; (B) exclusive phase instrumentation and parity/accounting tests; (C) allowlisted runtime/job integration and admission tests; (D) gated run and evidence report. The single job itself gates capture, then every replay, then full fits; failure stops later phases. The larger historical task is not reopened for unrelated changes.

Memory consulted for benchmark hygiene: maintain identical science/settings and keep exploratory timing distinct from inference accuracy or a general speed ranking. Current retained receipts, not historical host timings, drive this design. No additional source/compute scope is implied.


### 10D diagnostic implementation approved and validated — 2026-11-12

Live human approval: “Approve bounded diagnostic study”. Scope is the saved17-child diagnostic and one gated RAL job, despite Heart RED; outside Pulse, stop on first failure, retain data, human merge. New job allowance remains UNUSED. Implemented capture/replay, exclusive wall/CPU phases, strict retained-reference parity, allowlisted runtime identity and separate submission claim. Original18-child benchmark and0/2 transport are unchanged.292 tests pass; lint/format/shell/catalogue pass; zero-science structural smoke verifies descriptors plus0/1/2/shared/bound worker startup and cleanup. Author review only; CI/fresh runtime restore are pending gates.

Planning Heart RED reasons were “PyAutoLens: on branch feature/pixelization-feature-review (not main)” and “PyAutoLens: 2 uncommitted source change(s)”. Fresh authoritative readiness2026-11-12T12:40:44.942978+00:00 is YELLOW with no RED reasons: “PyAutoArray: open PR 9d old”; “test run status unknown”; “release validation stale: source moved since rehearsal (PyAutoLens)”. Existing approval covers development; no release, merge or failed-check bypass. RAL authentication and private staging cache are available.


### Diagnostic submission415179

Submitted exactly once through hpc/sync after CI43220440830 green and fresh artifact13 restore65.78s with zero science and cleanup. Producer0958bc28705541f6ff07fa4ad79bbfaf94ccdaaf; new training-diagnostics-ral-01 claim and separate environment. Approval now CONSUMED; no retry/requeue/replacement. Monitoring job415179 to completion or first failure; retain all evidence; outside Pulse, human merge.


### Diagnostic415179 terminal result — no new compute authorized

FAILED1:0 in70s on euclid-ral-compute-10-2. Bootstrap25.80s and normal capture fit/checkpoint reopen completed; historical posterior hash failed. Scientific supervisor42.645s, child36.976s, group peak241.81MiB, no live descendants and cache cleanup complete. All12 replay/four traced cases unrun. Raw16,627,876bytes retained remotely/locally/human scratch; report and compact inspection committed to diagnostics_10d. No new timing conclusion.

Read-only checkpoint inspection forbade run/train/likelihood (all zero) and preserved bytes. Old reconstructed posterior/models exactly match retainedreference. Both fits23500calls/12shells/all44 network iteration counts identical; initial cube points equal but initial likelihood differences~1e-14, later coordinate max1.56e-13. Different node versus reference euclid-ral-compute-1 makes cross-node numerics the leading hypothesis, not proven causation. Sampling settings, complete inventory and pinned sources match.

Producer0958bc2/CI43220440830 passed. Author review only. Fresh authoritative readiness remains12:40:44Z YELLOW with no RED; current scoped approval recorded. One-job grant CONSUMED; no replacement submitted. Proposed next amendment below requires explicit approval; outside Pulse, human merge.

# Proposed reference-node amendment — awaiting approval

Issue16 / draft PR17, existing feature/nautilus-spawn-training-pool worktree. Continue outside Pulse; merge remains human. The previous single-job allowance was consumed by job415179. This plan is not permission to submit another job.

1. Update only the diagnostic protocol/driver, diagnostic wrapper and focused tests. Request `--nodelist=euclid-ral-compute-1`, the actual reference node, in addition to the existing exclusive ral allocation. Validate that exact hostname before launching any child and on subsequent admissions. No fallback node, alternate partition, extra allocation or scheduler manipulation; if unavailable, the job waits normally.
2. Record candidate result, ordered model digests and completed corpus manifest before historical-reference comparison, explicitly marked unverified. Preserve parent CPU identity and full native-library/thread metadata before the fit starts. The failed capture remains failed; no replay can consume a rejected or incomplete capture. Keep all old raw outputs and reports unchanged.
3. Add negative tests for wrong-node admission, persistence on historical-parity failure and refusal to replay an unverified capture. Re-run existing tests, lint/format/shell/catalogue checks and zero-science structural smoke; commit/push and require exact-head CI green. Refresh authoritative Heart readiness under the scoped development override. Build a fresh checksummed runtime and require a fresh zero-science restore/cleanup pass.
4. Submit exactly one fresh17-child diagnostic, with a new training-diagnostics-ral-02 output claim and separate environment; preserve attempt01. Same one capture,12 replays in PSUB/BUSP/UPBS order, four traced fits in serial/pool/pool/serial order. Same reference, scientific settings and exact hashes; do not replace reference values or introduce tolerances. No reuse of the rejected corpus to bypass capture.
5. Limits remain120s/4096MiB per child group,1800s total, at most17children, one exclusive ral node/four bound physical cores/8GiB/35minutes;180s bootstrap and120s cleanup reserve. Whole-node reservation on the reference node includes252 scheduler CPUs; only four are bound to the scientific step. Stop on first failure; retain everything; no retry/requeue/replacement or release. Cleanup only the newly owned temporary runtime cache.
6. Report replay/phase results if exact gates pass, otherwise retain and report the failure. Node pinning addresses a concrete admission omission but does not prove or guarantee cross-run bitwise reproducibility. No new performance claim until measurements complete.

Approval requested: this narrow diagnostic correction plus one fresh job. Workspace AGENTS.md requires an approved plan before source/job-script edits; the approved diagnostic plan's stop-on-first-failure and one-job limits require a new compute decision. The existing PR remains unmerged.

Final report head e81caa89cafc2b9c81efe99b350ea34f58df3004 and CI43222506205 are green. PR17 remains draft/open/unmerged. Proposed reference-node amendment remains unapproved; no more compute authorized.


### Reference-node amendment approved

Live human: “Approve amendment and one run”. Approved saved NODE_PIN_AMENDMENT.md scope: original node admission, durable pre-validation candidate and metadata receipts, focused tests, one fresh17-child diagnostic after tests/CI/fresh restore. Same120s/4GiB per child,1800s total, exclusive ral4boundcores/8GiB/35min; exact parity unchanged. First failure stops; preserve all data, outside Pulse, human merge. New allowance UNUSED.

Reference-node implementationd3a36cf:300tests/lint/format/shell/catalogue/zero-science worker-descriptor smoke pass, author review. CI43227695075 green. Heart12:57:11Z YELLOW: "PyAutoArray: open PR 9d old"; "release validation stale: source moved since rehearsal (PyAutoLens)". Artifact14/fresh restore14 pending, new one-job allowance UNUSED.


### Fresh reference-node job415180 submitted

One submission via hpc/sync at d3a36cf; all gates passed:300tests/zero-science smoke/CI43227695075, runtime4.18s/fresh restore51.19s/cleanup. Exact node euclid-ral-compute-1 requested; output training-diagnostics-ral-02 and separate environment, old claim01 preserved. New allowance CONSUMED; no retry/requeue/replacement. Monitoring owned job; outside Pulse, human merge.


### Reference-node diagnostic complete — awaiting human review/merge

Job415180 COMPLETED0:0/538s,17/17 cases, unrun0, complete cleanup/all descendants reaped. Bootstrap23.92s, scientific510.59s, largest child48.30s/592.86MiB sampled process-group RSS. All fits match reference posterior/state/model/target23500calls/12shells/ESS10038.507608002912; all12replays exact with zero forbidden calls and unchanged inputs. Phase call counts equal and accounting exact.

Mean traced10Dseed2: training10.974→8.734s(−2.240), otherfit20.139→28.253s(+8.114), lifecycle~0→1.619s, workflow31.117→38.610s(+7.493). Extra parent CPU outside training7.78s accompanies extra wall8.11s; likelihood/prediction/output dominate, not extra sampling or storage waiting alone. Replays give no fixed spawn penalty; pinned0/1 slower than shared. Underlying hardware/runtime cause not isolated; no default change or uninstrumented speed claim.

Measured sourced3a36cf79b5c5dfc073ec64b38595430400798ed,300tests/lint/format/shell/catalogue/zero-science smoke pass, source CI43227695075 green. Report-only headfc508aefcabf58e7c4cb65a12fcf19f2375daa8a/final CI43231203005 green. Author review only. Latest readiness receipt12:57:11Z YELLOW: "PyAutoArray: open PR 9d old"; "release validation stale: source moved since rehearsal (PyAutoLens)". No release/merge/failed-check bypass.

Raw110,486,049bytes retained on RAL and locally;57,820,758byte archive plus SHA256SUMS and readable HTML/plots in Science scratch/training/10d_training_diagnosis_2026-11-12/job415180. Attempt01 and all previous jobs unchanged. Both single-job allowances consumed; no extra compute or persistent monitoring. PR17/issue16 remain open, outside Pulse, human merge. Deliverable complete; next investigation requires its own explicit scope/approval.


### Parent CPU slowdown follow-up — proposed, awaiting approval (2026-11-12)

User request: “Can we investigate why the other CPU work slows down when the training pool is enabled? Keep it outside Pulse and leave merge for me.”

Read-only chronology of retained job415180 found that the first 8 likelihood batches, with the pool already initialized but no training yet, use mean 0.08627s serial / 0.08738s pooled parent CPU. The 168 batches after the last training call use 1.81169s / 3.39046s (~87% more). This localizes the loss after actual training but does not establish its cause. No new scientific calls or executable source edits.

Concrete two-level plan: draft/feature/autofit/nautilus_parent_cpu_slowdown.md. Twelve full fits, two reverse-order repetitions of six arms: serial, persistent pool, pool closed after final training, serial model pickle roundtrip, parent-pinned serial, and disjoint parent/worker affinity. Passive main-thread/process/worker CPU, GC and runtime observations. Preserve frozen science and exact historical parity; no installed library changes. Workspace-only continuation of issue16/PR17; phased implementation and existing branch claim checked.

Proposed one exclusive RAL job on euclid-ral-compute-1, four bound physical cores, 8GiB, 35 minutes; 12 case groups, 120s/4096MiB each, 1800s total. Stop on first failure, retain all data, outside Pulse, merge human. This new implementation and compute remain UNAPPROVED; all prior job allowances are consumed. Heart authoritative receipt 2026-11-12T13:48:57.456105+00:00 remains YELLOW, no RED reasons (old Array PR and stale release validation).

Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_optimizations_2026-11-10/training/parent_cpu_followup_2026-11-12/REPORT.html, with chronology plot, evidence JSON, source receipt hashes, proposed plan and resume note. Previous job415180 artifacts remain unchanged. Producer remains clean at fc508ae, draft PR17 open/unmerged.


### Parent CPU investigation approved — 2026-11-12

Live human: “Approved, proceed with the 12-fit investigation and one RAL job under those limits. Keep it outside Pulse and leave merge for me.” The saved six-arm, reverse-order 12-fit plan is approved for implementation and one gated RAL job. Allowance UNUSED. Exact reference node/science, 120s/4096MiB per group, 1800s total, exclusive four-core/8GiB/35-minute job; stop on first failure, retain all data. Resume existing workspace/issue16/PR17, no merge or Pulse.
