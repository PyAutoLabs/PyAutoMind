# Nautilus experimental dimension pilot — phase 0b.1

Type: feature
Target: autofit_profiling
Repos:
- autofit_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: workspace-dev
Issued: 2026-11-10
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/10
Epic: nautilus-fast-likelihoods
Phase: 0b.1
Filed: 2026-11-10
Consequence: judge
Witness: A standalone experimental protocol links an immutable run manifest to portable profiling results; dimensions and targets cannot collide or pool silently; a bounded paired direct/wrapped pilot records every attempt and analytic diagnostics without changing historical phase-0a evidence or claiming phase 0b complete.
Review-minutes: 10
Unattended: never
Lane: local-dev

## Request and authorization

User request verbatim: "continue" (after phase 0a merged and closed).
Clarified live authorization verbatim: "Authorize phase 0b planning despite RED".
Implementation approval received 2026-11-10: "Approved. Proceed with phase 0b implementation, the bounded local pilot and development PRs despite Heart RED. Leave merge for human". Scope correction in the same message: "is this a pulse campaign? Feels like for now it can be off to one side its more experimental". This supersedes the original Pulse-registration proposal: keep this experimental in autofit_profiling, with no Pulse registration or automatic catalogue publication. No remote compute, merge or release is authorized. The phase-0a worktree and raw data remain retained by the human's instruction.

## Ownership and current evidence

Phase 0a: autofit_profiling#9 merged at 6ab7358a9e9ddcbaf14dd31068d1cfb64caf5f89; Mind record complete/2026/11/nautilus-cpu-profiling-baseline.md. Its 52 selected runs / 26 trace-control pairs establish an exploratory five-dimensional baseline, not a dimension campaign. Training and geometry dominate; laptop scatter prevents a precise overhead or speedup claim.

This is an off-board experiment at the human's direction. No Pulse campaign/task/registry/board change. Keep evidence under experiments/nautilus_cpu_dimensions/ outside build_catalogue discovery. Mind owns the bounded development issue and claim. Promotion into Pulse is a later explicit decision; historical Pulse/Insight links are context only.

Insight owns existing full-search validation protocols. Read-only reuse/context: PyAutoInsight/tasks/correlated_nd_pilot.md and autofit_inference/wiki/project/protocol_correlated_nd.md. The historical condition-number-1000 Gaussian family at dimensions 20/50/100 and Rosenbrock d20 is DIFFERENT from phase 0a's AR(0.6) Gaussian with normal priors. Its old-pin d100 Nautilus failures, d50 OOMs and four-hour caps are hazard evidence, not measurements of the proposed new family or proof the current stack fails. Do not revive the separate 12,450-run scored wave or paused HST waves.

## High-level plan

1. Record a standalone experimental protocol and immutable local run plan, linking phase 0a and the relevant historical protocols; leave Pulse untouched.
2. Extend the existing profiling harness with a versioned campaign manifest, complete case identity and safe attempt/resume accounting. Preserve all phase-0a commands and results.
3. Make report grouping and output names dimension/target/settings aware; reject duplicate identities, mixed source pins and incomplete pairs instead of overwriting or pooling them.
4. Run a bounded local dimension pilot only after implementation approval: dimensions 5/10/30, three seeds, direct and wrapped, traced and control, fixed settings and one worker. Publish failures, missing diagnostics and variability alongside successes.
5. Prepare the resource-gated next stages for 60/100/200 dimensions, representative targets and worker comparisons; do not execute them or optimize the sampler in this task.
6. Validate and open one reviewable autofit_profiling development PR; keep experiment evidence outside the published catalogue. Phase 0b stays active/pending after this member; no complete-phase claim until its required dimension and representative-target evidence is reviewed.

Tier: judge — merge mode: human /prm. The live RED override authorizes implementation, the bounded local pilot and a development PR. Merge remains separately human-authorized. No release, GPU or HPC submission.

## Detailed implementation

### A. Standalone experimental protocol

Write experiments/nautilus_cpu_dimensions/README.md and protocol.json before measurement. The nautilus-cpu-experiment@1 protocol distinguishes exploration, execution outcome and scientific acceptance. Store its plan/results/report here outside results/ and dashboard discovery. Link it from the producer README as experimental evidence. Do not touch Pulse source, registry, tasks or snapshots, and do not regenerate or publish the production catalogue from these experimental rows.

### B. Manifest and runner

For the first pilot retain phase-0a PyAutoFit bdb7af0e9c339ad07850679fd6ac168aacc7d18c, PyAutoNerves 9b204c90c2ce05c5bb0cf3e9800ed13f005c6c56 and Nautilus 1.0.5 with the same installed-source digest. Copy the environment specification into a new isolated environment and make separate detached dependency worktrees; do not alter the retained phase-0a evidence environment. Record the new harness commit before measurements. Any dependency upgrade is a separately named experiment.

Add scripts/analytic_gaussian/nautilus/campaign.py and scripts/misc/profiling/nautilus_campaign.py. Reuse cpu_baseline.py/RunConfig, source_pins and the existing supervisor. Campaign plan mode emits all expected cases and resource limits without importing scientific packages or launching work. Run mode consumes that immutable plan; it cannot regenerate a different matrix on resume.

Identity includes campaign/protocol, target family and truth digest, dimension, settings digest (seed excluded from grouping but retained per run), adapter, workers, cost policy/work, seed, trace, source/content pins and host identity. Attempt IDs are separate from logical case IDs. Write status atomically before launch and after exit. Restart reconciles an interrupted/running attempt as incomplete and creates a new attempt directory; never reuse a checkpoint silently, erase a failed attempt or count a retry twice. Source changes halt the campaign; equivalent detached paths are allowed only when revision/content identities agree.

Preserve success/error/timeout, add explicit interrupted/missing/deferred/unrun/trace-incomplete accounting. Keep existing phase-0a pilot behavior compatible. A hard wall cap must kill the process group using the existing supervisor and write its receipt. Add a configurable Linux process-tree RSS guard for this pilot; sample parent plus descendants and record cap-triggered termination separately from a measured OS OOM. Choose 4 GiB or a smaller explicit host-safe cap after available-memory preflight; refuse to start if that allocation is not safe. No machine paths in exported evidence.

### C. Reporting and diagnostics

scripts/analytic_gaussian/nautilus/report.py currently keys groups by adapter/workers/cost/trace and pairs by those fields plus seed. That is insufficient for a multi-dimensional campaign and can overwrite duplicate pair entries before matching. Add full target/dimension/settings identities and explicit duplicate/pair completeness checks. A new campaign report/export namespace keeps old phase-0a IDs and outputs stable. Do not label an unmatched traced run as measured tracing overhead.

Reuse analytic logZ and posterior truth. Report raw and standardized posterior-mean error, covariance error, logZ error, n_like, achieved ESS, calls per ESS, wall, component shares, tail metrics where applicable, peak memory, coverage and paired trace/control wall ratios. Distinguish unavailable native uncertainty/proposal rejection diagnostics from zero. Add diagnostics only from inspected runtime APIs; if they require invasive Nautilus changes, report unavailable and leave that as a separate task. No classic nested-sampling sqrt(H/n_live) accuracy assumption for Nautilus.

Trace/control numerical gate: same target/settings/pins, identical native likelihood count and posterior hash at the deterministic NumPy pin. Cross-adapter comparisons also assert the effective prior transform, resolved options and native run-call schedule. Fail closed on a mismatch. Analytic errors are descriptive at three seeds, with no invented scientific acceptance tolerance or speedup threshold. Scientific scoring must reuse an applicable Insight protocol unchanged, or pre-register a separate calibrated protocol before independent scored seeds.

### D. First pilot: explicit proposed budget

| Item | Proposed value |
|---|---|
| Target | Existing CorrelatedGaussianTarget; AR(0.6), independent N(0,1) priors, float64 |
| Dimensions | 5, 10, 30, in ascending order |
| Seeds | 0, 1, 2; engineering calibration only |
| Adapters | direct, pyautofit |
| Tracing | off/on paired; alternate order by seed |
| Workers | 1; native BLAS/OpenMP threads 1 |
| Sampling | n_live=400, n_networks=4, n_batch=100, n_eff=500, f_live=0.01; checkpoints on; update_interval=1000000 |
| CPU cost | fixed, work=100; same numerical target and work across each matched pair |
| Cases | 3 dimensions × 3 seeds × 2 adapters × 2 trace modes = 36 |
| Per-case cap | 120 s, including subprocess execution |
| Whole execution cap | 90 minutes including runtime preflight; stop admission when remaining budget cannot fit a case |
| Memory | Explicit process-tree cap at most 4 GiB after safe-host preflight; native threads capped before imports |

The 400-live setting is fixed across this pilot and can support a later d200 geometry probe; it is not a statistical adequacy guarantee. d5/400 is a new bridge cell, not a replacement or an apples-to-apples speed comparison with phase 0a's d5/200. Later setting changes create a new experiment identity.

Run only on a quiet reserved CPU allocation. Record CPU model, physical/logical cores, affinity, thread-pool configuration and host load. If the local machine cannot provide a quiet window, defer execution with a clear missing-host witness; do not cancel unrelated work. Observe but do not subtract timing variability. No RAL SSH or submission is part of this member.

A correctness/configuration/source/accounting failure halts immediately. A timeout or memory cap records the attempt and stops escalation to larger dimensions; remaining cases are deferred/unrun with the reason. No automatic resource inflation, selective seed retries or replacement of poor results. This task may ship an honest failure/capped pilot; it cannot claim that the dimension baseline is established from censored runs.

### E. Later phase-0b stages (not authorized by this member)

- Quiet-node scaling: 60/100/200 dimensions, one seed and matched direct/wrapped control first, then three calibration seeds only for resource-admitted cells. Explicit scheduler/memory/time budget needs approval. CPU arrays use RAL partition only. No automatic 200D launch.
- Utilization: one/two/four/eight likelihood workers subject to physical cores, first NumPy without JAX/fork hazards; fixed/random/parameter-correlated CPU work and slower-likelihood control, not a full Cartesian product. Current harness only supports one/two workers; four/eight requires its own safety and accounting checks. Vectorized single-process and JAX CPU routes need separately matched configuration/start-method witnesses.
- Target ladder: keep AR Gaussian separate; reuse pinned correlated_nd Gaussian/banana definitions, priors, realizations and exact references rather than inventing another hard-target benchmark. Mixture/plateau targets require validated existing definitions or a separately reviewed target addition. Preserve old inference protocol identities and historical failures.
- Lens ladder: first candidate is the existing simulated HST imaging/MGE builder and day-zero jax_cpu_dense_fp64 route, then a parity-admitted Delaunay/inversion and larger nonlinear fixture. The accepted day-zero result is likelihood evidence, NOT an accepted full-search posterior. Freeze data/mask/prior/nonlinear-parameter and linear-treatment identities before fitting; count sampled parameters, not linear coefficients. The JAX route must not be put through the current fork pool after JAX initialization. This needs its own autolens_profiling member, API/fixture admission and safe serial/vectorized execution plan. Paused HST sparse fixed-light divergence/other parity blockers stay blocked.
- Full-search correctness/scoring remains coordinated through Insight and scientific run records through Cortex. This task does not write either queue or submit their existing waves.

## Tests and acceptance

- Stdlib tests: manifest determinism, unique IDs across dimensions/settings, immutable resume, every terminal status, multiple attempts and duplicate rejection, budget/memory guards and pair coverage.
- Regression tests: multi-dimension report separation, no silent pair overwrite, mismatched/partial traces rejected for overhead, source pin equality independent of checkout path, historical catalogue byte/semantic preservation.
- Full-stack smoke: existing resume/watchdog probes plus one new campaign case on the fixed pins; process-tree termination and receipt verified in a small subprocess fixture. Never depend on a real OOM for a test.
- Ruff lint/format, focused and full tooling suites, catalogue --check --validate-with the pinned Pulse reader, link checks; verify the production catalogue remains unchanged. Preserve all previously committed measurements.
- Publish protocol, immutable plan, all attempt receipts, selected-case mapping, report and resource summary. Producer records stay unreviewed. No speedup or phase-completion claim inferred from successful exit codes.

## Branch and claim survey — 2026-11-10

Branch: feature/nautilus-cpu-campaign-setup (autofit_profiling only).
Proposed worktree root: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-cpu-campaign-setup.
Primary issue: autofit_profiling, title "feat: add experimental Nautilus dimension pilot"; create through the Mind primitive.

No active Mind claim conflicts for autofit_profiling/PyAutoPulse. Main autofit_profiling is clean and behind the merged phase-0a head; create the new worktree from current origin/main, never reuse the retained phase-0a evidence worktree. Pulse main has untracked tmp/ and is behind generated dashboard commits; preserve it and use an isolated worktree. An older unregistered Pulse check-in worktree also exists; do not remove or alter it. Insight and inference/lens repos are read-only context in this member. Recheck claims/branches at implementation start.

## Planning gate record

Read-only start_dev entry feed: "Heart: RED — Release RED; monitoring RED · 11/100 · 143 unresolved (updated 23h ago)". The full entry output is saved with the human planning bundle; all RED reasons were shown in chat. User subsequently authorized implementation, bounded local pilot and development PRs, with Pulse registration removed. No new implementation tests are claimed yet. Carry the exact task-scoped authorization and current applicable evidence into issue, PR, active.md and the first autonomy-log table under the canonical workflow.

## Feature routing receipt

Brain feature classified this as workspace development affecting autofit_profiling and PyAutoPulse. Its declared medium classification wins over the derived too-large heuristic (the long document includes deferred later campaign scope). The executable member is only campaign registration, manifest/report changes, guards and the 36-case Gaussian pilot; later target/worker/HPC stages are excluded. No public library API change is planned. Memory was consulted; historical sampler notes do not override current protocol/fixture evidence.

The user's experimental-scope correction overrides all earlier canonical-campaign routing requirements for this member. No further permission is required to implement this narrower approved scope.
