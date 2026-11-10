# Nautilus fast likelihood development epic

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_inference
- autofit_profiling
- PyAutoLens
- autolens_inference
- autolens_profiling
- PyAutoCortex
- PyAutoInsight
- PyAutoMind
- PyAutoPulse
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: phase 0a merged 2026-11-10 (autofit_profiling#9, issue #8 closed); experimental phase 0b.1 merged (autofit_profiling#11, issue #10 closed), experimental phase 0b.2 diagnostics awaiting human merge (autofit_profiling#13, issue #12); wider phase 0b incomplete; no Pulse campaign
Epic: nautilus-fast-likelihoods
Filed: 2026-11-09
Consequence: judge
Witness: Pinned CPU and GPU end-to-end comparisons show reduced wall time at matched posterior/evidence accuracy across repeated seeds, with overhead, likelihood work, memory, failure rates and checkpoint/resume behaviour reported separately; each shipped optimisation has its own bounded PR and fallback.
Review-minutes: 20
Unattended: never
Lane: any

## Intent and current state

James chose Nautilus development on 2026-11-09: profile and extend Nautilus for fast likelihoods on both CPU and GPU, CPU first. This is an implementation epic, not a replacement-sampler survey. It is FILED, not running. No performance result or implementation decision below is claimed as measured in this intake.

Preserve Nautilus's demonstrated usefulness for lens modelling while reducing the time spent outside useful likelihood work. Investigate the hypothesis that CPU batches wait on the slowest evaluation; measure both within-chunk imbalance and the final batch barrier. Also measure serial neural training, geometric bounds, serialization, wrapper overhead and checkpointing. Characterise degradation with increasing nonlinear dimension from the start; solving execution overhead does not by itself solve sample efficiency.

This umbrella is never issued wholesale. The phase-0a member is complete in `complete/2026/11/nautilus-cpu-profiling-baseline.md` (autofit_profiling#9 merged); create later small implementation prompts from measured findings, one task/PR at a time. The phase order below is the plan, not approval to start development tonight or a scheduled job tomorrow.

## Ownership and repository boundaries

- @PyAutoFit owns its Nautilus adapter, likelihood dispatch, configuration, samples and checkpoint integration. Re-read current `autofit/non_linear/search/nest/nautilus/search.py`, `autofit/non_linear/fitness.py` and prior-vectorisation code before editing; the search-extensibility refactor may have changed earlier call sites.
- @autofit_profiling owns generic sampler/wrapper instrumentation and reproducible cheap-likelihood fixtures. @autolens_profiling supplies representative likelihood costs and component breakdowns.
- @autofit_inference and @autolens_inference own full-search benchmark producers and results. Use current accepted fixtures, never restore the retired inference_programme or treat its archived measurements as baselines.
- @PyAutoPulse owns profiling campaign intent and pending profiling tasks; @PyAutoInsight owns inference campaign intent and pending validation runs. @PyAutoCortex retains scientific run records and human conclusions. This Mind ledger owns bounded development phases and their issue/PR lifecycle, not a competing run queue.
- Phase 0 must resolve/link canonical campaign tasks before campaign execution. Existing anchors: [Pulse autofit profiling](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md), [Insight HST sampler wave](https://github.com/PyAutoLabs/PyAutoInsight/blob/main/tasks/hst_mass_samplers_wave1.md) and the `gaussian-x3-search-benchmark` campaign in Insight. Preserve their existing blockers; a new epic does not restart paused waves or change accepted targets.
- Upstream implementation is [johannesulf/nautilus](https://github.com/johannesulf/nautilus). Record the installed release and exact source SHA. Prefer small upstream-compatible changes; use an isolated pinned experimental checkout for upstream prototypes. Decide any maintained fork/package/repository arrangement only when a measured change requires it; do not silently vendor Nautilus or replace the production dependency.

## Existing evidence and constraints to carry forward

1. [July overhead investigation](https://github.com/PyAutoLabs/PyAutoMind/blob/main/complete/2026/07/nautilus-nn-bottleneck.md): historical fast-likelihood experiments found neural training and geometry dominant. The maintainer rejected disabling neural networks despite toy speedups because peak-finding degraded. A JAX MLP prototype was slower on CPU. Reproduce relevant facts on current pins; neither repeat the failed port blindly nor treat a historical feasibility verdict as a permanent prohibition on new work. Keep neural bounds enabled in the production comparison.
2. [August pool repair](https://github.com/PyAutoLabs/PyAutoMind/blob/main/complete/2026/08/nautilus-serial-bound-training.md): worker initialisation fixed repeated serialization of a large Fitness/dataset; serial bound training avoided dead-worker hangs. Preserve those fixes. A second sampler pool requires an independent safety/memory witness, not removal of the existing protection. Avoid forking a process after JAX runtime/thread initialisation; evaluate spawn/forkserver only where supported, with realistic initialization cost.
3. [Existing variable-batch compilation task](https://github.com/PyAutoLabs/PyAutoMind/blob/main/draft/bug/autofit/vmap_jit_recompiles_per_nautilus_batch_length.md): link and reuse this task after checking whether it has since shipped. Do not file a duplicate or assume the historical implementation still exists.
4. [Search extensibility epic](https://github.com/PyAutoLabs/PyAutoMind/blob/main/draft/research/autofit/search_extensibility_epic.md) and [likelihood lifecycle epic](https://github.com/PyAutoLabs/PyAutoMind/blob/main/draft/research/autolens_profiling/likelihood_lifecycle_epic.md) already own shared contracts, profiling/inference producers and backend parity. Consume them; avoid another framework rewrite.

## Phases and decision gates

| Phase | Bounded objective | Required evidence before proceeding |
|---|---|---|
| 0 — CPU baseline and instrumentation | Build the repeatable profiling harness, reconcile old work, identify the actual CPU floor and straggler cost. | Pinned manifest, event timeline, measured instrumentation overhead, serial/multicore decomposition and ranked bottlenecks; correctness checks on the harness itself. |
| 1 — Reduce CPU overhead | Optimise the largest measured serial/wrapper costs one at a time. Candidates: array allocation/copies, prior transforms, bound geometry, prediction batching, checkpoint frequency and unnecessary result/log work. | Ablation showing end-to-end gain, unchanged target and sampling configuration unless explicitly varied; correct checkpoint/resume and no hidden loss of neural-bound quality. |
| 2 — Improve CPU worker utilisation | Tune persistent-worker task granularity, thread/process budgets and result collection. First keep the same complete logical batch and adaptation boundary, but schedule its chunks dynamically and restore proposal order. Separately test a dedicated safe sampler pool if bound construction warrants it. | Worker occupancy and p50/p95/p99 latency improve on variable-cost fixtures and real targets; all submitted batch members accounted for; no per-task Fitness pickling, unbounded queues, hangs or oversubscription. |
| 3 — Overlap work, then evaluate true asynchronous adaptation | First overlap proposal generation/dispatch with evaluation using frozen proposal epochs and bounded buffers. Only then consider advancing sampler state before all older work returns. | Explicit statistical design for proposal versions, shell membership, sample counts/volumes, adaptation and evidence weights; runtime-bias tests, crash/restart tests and independent review. May conclude that stable batch boundaries are the better design. |
| 4 — Combined CPU/GPU execution | Apply the proven CPU improvements to the host side; explore multiple CPU sampler workers feeding GPU likelihood batches, concurrent CPU and GPU likelihood workers, and multiple GPUs where available. Profile transfers, compile count, device/worker idle gaps and batch-memory tradeoffs. Reuse the existing variable-batch task; follow the mixed-device experiment contract below. | Warm and cold end-to-end timings on actual hardware, bounded compilation/memory, correct padding/masking, backend likelihood parity and full-search accuracy. Quantify whether mixed execution improves on the best CPU-only and GPU-likelihood baselines at stated resource allocations. |
| 5 — Selective JAX acceleration | Port only measured expensive kernels, initially behind optional backends: geometry/membership tests, transforms or ensemble prediction/training where justified. Keep CPU control flow initially; evaluate deeper device residence as a separate design. | Kernel equivalence plus end-to-end wins including compilation and transfers. Reject regressions; a neural rewrite must compare bound/proposal quality and total evaluations, not just training speed. No assumption that a wholesale JIT rewrite is necessary or beneficial. |
| 6 — Improve higher-dimensional efficiency | Using the dimension sweep already established in phase 0, determine whether proposal acceptance, bound volume, NN discrimination, modes or adaptation causes the loss. Test measured remedies separately from scheduling changes. | Better wall time and evaluation efficiency at matched evidence/posterior accuracy and mode recovery across seeds; no silent prior narrowing or dropping hard cases. Algorithmic changes get their own mathematical justification and review. |
| 7 — Integration and release readiness | Consolidate successful options, docs, configuration, dependency pins, diagnostics and fallback; upstream suitable changes. | PyAutoFit conformance/integration and supported-platform checks; resume compatibility policy; reproducible CPU/GPU results published to the owning projects/boards. Production defaults only change through the normal reviewed development flow. |

Dependencies: 0 → 1 → 2. Phase 3 follows the phase-2 evidence and may remain experimental; phase 4 can proceed using phases 1–2 even if true asynchronous adaptation is rejected. Phase 5 follows phase 4. Phase 0a is the harness/local pilot (autofit_profiling#8); phase 0b is the separately scoped canonical baseline campaign, including dimension measurements. Both outputs are required to complete phase 0. Dimension measurement begins in phase 0b, while dimension-changing algorithm work is deferred to phase 6. Phase 7 lands proven increments rather than waiting for every speculative branch to succeed.

## Combined CPU and GPU experiment contract

Explicitly requested by James after reviewing this plan: "also make sure cpu plus gpu multi use is explored". CPU-first remains the order; combined execution is a required investigation in phase 4, not an assumed speedup or a promise to ship every topology.

1. **CPU sampler pool plus GPU likelihood:** compare serial host Nautilus with multiple safe CPU workers for proposal generation, geometric bounds and neural training/prediction where dependencies permit. Feed one persistent GPU-owning process with bounded batches. Measure overlap of independent host/device work, including transfers, rather than presuming it is possible during every adaptive stage. Keep training/proposal state versions explicit and retain the existing pool-safety protections.
2. **CPU and GPU likelihood workers together:** evaluate a heterogeneous worker pool in which both devices compute the same target. Explore cost-aware dispatch and device-specific chunk/batch sizes, initially inside a frozen logical batch with ordered result admission. Account for slow CPU tails that could make the combination worse than GPU alone. Reserve CPU capacity for the controller, GPU dispatch and data handling; CPU likelihood workers must not starve them.
3. **Multiple GPUs where available:** start with independent persistent workers per device and explicit data placement; compare sharding one search's likelihood work with independent searches/seeds on separate GPUs. Distinguish single-fit latency from campaign throughput. Avoid spawning a GPU context in every generic CPU process, and measure replicated model/data memory, JIT warm-up and contention. No multi-GPU hardware means this leg is unmeasured, not passed.
4. **Correctness and accounting:** validate CPU/GPU numerical parity on common points, including near current likelihood boundaries, before mixing results. If backend discrepancies can change admission, define and test a consistent reevaluation policy or keep those backends separate. Record device assignment, proposal version and RNG ownership; apply the asynchronous correctness contract to mixed completion times, retries and checkpoints. Never preferentially retain points because their device finished first.
5. **Comparison and decision:** report CPU-only, one-GPU likelihood with serial host work, one GPU with parallel CPU sampler work, mixed CPU/GPU likelihood work, and multi-GPU results where feasible. Use the same target and accuracy criteria; state CPU allocation, GPU model/count, CPU-hours, GPU-hours, peak memory and full-run wall time. Measure CPU/GPU occupancy and critical-path waits to decide whether spare CPU capacity helps the sampler, helps likelihood evaluation, or should remain unused. A justified negative result satisfies an exploratory leg.

## Benchmark and profiling contract

Start small and expand after a pilot; avoid a huge Cartesian sweep. Propose a seed count and numerical tolerances from baseline variability, freeze them before scored comparisons, and retain every failed, timed-out and missing run. For engineering pilots use at least several independent seeds; decisive correctness claims need the pre-registered, sufficiently powered validation campaign.

- Three layers: direct Nautilus with a trivial analytic likelihood, Nautilus through PyAutoFit with the same target, and validated PyAutoLens fixtures. This isolates sampler cost from wrapper cost and real likelihood behaviour.
- CPU backends: serial, vectorised single-process, and persistent multiprocess; NumPy/Numba and JAX CPU where supported. Compare 1/2/4/8 workers subject to available cores and explicitly cap BLAS/OpenMP/JAX thread counts. Include a slower-likelihood control to expose regressions hidden by the cheap regime.
- Synthetic targets: correlated Gaussian with known evidence, curved degeneracy/funnel, separated mixture and a plateau/bounded target as supported by existing suites. Characterise approximately 10/30/60/100/200 nonlinear dimensions where affordable; record which cases actually ran. Source pixels/linear coefficients solved inside an inversion are not sampler dimensions.
- Stragglers: fixed-cost, random variable-cost and parameter-/mode-correlated runtime profiles with identical numerical likelihood values. Sleep can isolate scheduler mechanics but must be accompanied by real CPU work/representative likelihoods. Inject one slow/failing worker and interrupted runs. Never discard a sample because it is slow or select only the first completed results.
- Lens ladder: begin with an accepted cheap parametric/MGE imaging fixture; then validated Delaunay/inversion and a larger nonlinear model. Keep data, masks, priors, linear treatment, precision and likelihood pins identical across sampler variants. Sparse/dense parity blockers remain blockers, not performance results.
- Record wall time for startup/compilation, warm sampling and complete run; likelihood and prior-transform cost; neural training/prediction; geometry/proposal rejection/overlap; serialization/IPC; queue wait and idle-worker intervals; checkpoint/I/O/results overhead; memory; accepted proposal rate; likelihood calls; effective sample size; logZ and uncertainty; posterior/mode recovery. Separate overlapping work from the critical path instead of summing overlapping stage times.
- GPU timers must wait for the measured device work to finish at measurement boundaries; measure CPU-only host work separately. Report warm versus cold compilation and batch shapes. Padded rows must never enter shell counts, evidence, history or samples, and padded inputs must themselves be valid for the likelihood.
- Primary outcome: time to a statistically valid result, including failure rate and uncertainty across seeds. Also report ESS/second, likelihood calls per useful sample, total CPU-hours/GPU-hours and peak memory. Do not claim success from throughput or speed per likelihood alone.

## Asynchronous correctness contract

Distinguish (a) scheduling chunks within an unchanged batch, (b) prefetching under a frozen proposal, and (c) adapting on partial/out-of-order results. A map_async call followed by a full wait is still a batch barrier. Smaller chunks reduce imbalance but cannot eliminate the final slow evaluation.

Each proposal needs stable identity, proposal/bound version, RNG ownership and evaluation status. The sampler controller is the sole owner of adaptive state. Define when each result is admitted, how outstanding work is drained or retained across updates, and how retries are deduplicated. Correct weights/counts must follow Nautilus's actual importance/shell estimator, not a guessed standard nested-sampling rule. A stale proposal is not made valid merely by checking the latest likelihood threshold. Explain estimator validity before implementing partial-result adaptation.

Persist or safely drain pending work at checkpoint boundaries; test cancellation, worker death and resume with no omitted/duplicated samples. Use reordered execution and runtime correlated with parameter values to expose completion-order bias. Preserve deterministic logical ordering for the first scheduling implementation; promise bitwise equality only where the design and backend permit it.

## Scope limits and research reserve

The user's choice is Nautilus development. Alternative samplers are optional diagnostic controls, not prerequisites or a new broad comparison campaign. Gradients are deferred: they are not a straightforward replacement for Nautilus's rank-trained bound classifier, and discontinuous likelihood components need separate treatment.

Retain links from the preceding research as design references, not validated lensing results: [i-nessai](https://arxiv.org/abs/2302.08526), [JAXNS](https://github.com/Joshuaalbert/jaxns), [NS-SwiG](https://arxiv.org/abs/2602.17414), [SHARPy](https://github.com/gabrieledemasi/sharpy), [PARIS](https://github.com/mx-Liu123/parismc), [ASPIRE](https://github.com/mj-will/aspire), [neural transport NS](https://arxiv.org/abs/2609.29413). Reverify versions, public code and estimator assumptions before importing any idea. ASPIRE-style result reuse and hierarchical factorisation are separate science/workflow opportunities, not direct Nautilus CPU optimisations.

## Tomorrow's starting point

Resume this epic and start phase 0 only. Read current pins and claims, inspect the generic profiling harness, and produce the smallest instrumented CPU benchmark. Deliver a measured bottleneck ranking and the next single optimisation proposal. Aim for one verified CPU improvement in the next development step; do not begin by rewriting the neural network or the entire sampler in JAX.

## Original request (2026-11-09)

"I am going to push forward with nautilus development tomorrow with the goals to be to profile and extend nautilus against fast likelihood evaluations on both CPU and GPU. So based on this chat come up with a plan for how we do this and intake it as an epic in PyAutoMind. Cpu speed up first makes sense i think"

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:nautilus_epic_input.md -->

## Experimental phase 0b.1 — merged 2026-11-10

Completion record: `complete/2026/11/nautilus-cpu-campaign-setup.md`. PR autofit_profiling#11 merged unchanged at 62e67ccf2942778f2493f70a9752e8d884bc3c43 after explicit human merge authorization and every configured CI step passed; issue #10 is closed.

The human approved implementation and the bounded local pilot despite RED, narrowing it to experimental off-board work. That correction supersedes canonical Pulse registration for this member. No Pulse task, campaign, registry or catalogue publication occurred. The worktree and raw data are retained by explicit request.

Pilot: 26 successes, one fixed-cap timeout, nine unrun; 13 matched tracing pairs and 12 cross-adapter matches. Direct 30D seed 0 reported logZ error −0.9081 despite ESS 9740.4; wrapped 30D control timed out at 120 seconds with no complete fit receipt. These are exploratory findings, not accepted accuracy or an optimization speedup. Full phase 0b remains incomplete.

Next: separately scope high-dimensional evidence accuracy and end-of-fit output cost before expanding dimensions/targets or considering Pulse promotion. No new compute, optimization, merge or release is authorized by this completion record. Existing paused campaigns and parity blockers remain intact.


## Proposed first optimization members — 2026-11-10

Human requested implementing the plotting adapter and starting CPU sampler-speed work. Two separate plans are prepared, awaiting approval before library edits/compute:

- [Compact corner array adapter](../../../active/nautilus_compact_plot_adapter.md): PyAutoFit-owned opt-in path, numerical/visual parity and repeated wrapped-output comparisons; no anesthetic source edits.
- [CPU checkpoint batching](../../../active/nautilus_cpu_checkpoint_batching.md): opt-in interval5 versus native interval1, complete atomic snapshots, interruption/resume witnesses and paired5D/10D CPU runs.

Both remain experimental/outside Pulse; fullphase0b is incomplete. The diagnostic PR13 remains unmerged. Default behavior and neural bounds remain; merge stays human. Approval must cover the detailed new resource bounds and extend the development HeartRED override to these phase1library changes; no release/CI bypass.
