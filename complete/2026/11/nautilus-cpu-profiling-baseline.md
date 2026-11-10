## nautilus-cpu-profiling-baseline
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/8
- completed: 2026-11-10
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/9
- merge: 6ab7358a9e9ddcbaf14dd31068d1cfb64caf5f89
- summary: Phase 0a controlled CPU harness and exploratory local pilot merged unchanged. Phase 0b canonical representative-target/dimension campaign remains pending; phase 0 is not complete.

### What shipped

Matched direct Nautilus and PyAutoFit settings, analytic target with value-preserving variable CPU cost, bounded parent/worker timing and reconciled batch identities, independent timing controls, source/configuration manifests, subprocess deadlines, checkpoint/failure witnesses, portable report and catalogue integration. Historical catalogue cells are unchanged. No library defaults, sampler algorithm or optimization changed.

52 selected runs use identical dependency revisions/content; 26 trace/control pairs preserve likelihood counts and posterior hashes. Recovery retains one interrupted attempt and ten successful runs excluded after dependency drift. Pinned detached dependencies: PyAutoFit bdb7af0e9c339ad07850679fd6ac168aacc7d18c; PyAutoNerves 9b204c90c2ce05c5bb0cf3e9800ed13f005c6c56. Measurement source 7110619; final head f602ba42b297ba20677b7128187c1d27c089781a.

### Validation and merge authority

40 tooling tests, Ruff lint/format, four checkpoint/resume witnesses, traced/control worker-death probes, timeout receipt, 26 trace reconciliations, catalogue contract/history and links passed. Author review only; no independent review claimed. Exact-head GitHub run 42815939078: one configured pull_request run, one successful lint job, every step successful. Feature pushes do not trigger another workflow. GitHub reported CLEAN/MERGEABLE; all task commits are ancestors of origin/main after merge.

Live human merge command: "Merge and close phase 0a; retain data". Existing task-specific Heart RED development override remains recorded on issue #8, PR #9 and autonomy_log.md. Readiness was RED at 2026-11-10T12:13:48.638875+00:00: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". No release or CI bypass occurred.

### Findings and next scope

Neural-network training and geometry dominate this small Gaussian target. Shared-host variability prevents a precise tracing-overhead or multicore-speedup claim. Checkpoint batching is proposed as the next bounded experiment with interruption/resume witnesses; the measured share implies an ideal upper bound about 1.13x direct / 1.10x wrapped. It is not implemented. Phase 0b needs its separately scoped canonical profiling campaign, including dimensions and representative targets.

### Retained workspace and evidence

At the human's explicit request, retain /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-cpu-profiling-baseline, including 206 MB raw output and the isolated environment. No worktree or local branch removal was performed. Source activate.sh before runtime to select the detached dependency pins. The development claim is released; the retained checkout is an evidence archive, not active work.

Human viewing copy: /mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_plan_review_2026-11-10/phase0a_results/report.html. Repository findings: wiki/campaigns/nautilus_cpu_baseline.md; results: results/analytic_gaussian/nautilus/.

### Backlog reconciliation

Folder-scoped intake reconciliation found no additional prompt proved complete by this merge. Unrelated suspects remain: model_figures_epic.md, results_library_epic.md and ep_analytic_updates.md. A shared-file candidate pairs the Nautilus epic with skip_the_likelihood_for_assertion_violating_samp.md; shared library paths alone do not prove equivalent scope, and phase 0a edits no library source. No sibling was retired. Review separately via `pyauto-brain intake reconcile draft/feature/autofit`.

## Original prompt

# Nautilus CPU profiling baseline

Type: feature
Target: autofit_profiling
Repos:
- PyAutoFit
- autofit_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: awaiting-merge
Epic: nautilus-fast-likelihoods
Phase: 0a
Issued: 2026-11-10
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/8
Filed: 2026-11-09
Consequence: glance
Witness: A documented local command emits a pinned JSON manifest and CPU timeline for direct Nautilus and the equivalent PyAutoFit target, with serial and multiprocess cases, reconciled submitted/completed proposal IDs and an uninstrumented timing control; a variable-cost fixture exposes the batch-tail wait without changing likelihood values or samples admitted to the batch.
Review-minutes: 10
Unattended: ready
Lane: any

## Objective

Implement the first bounded phase of `draft/feature/autofit/nautilus_fast_likelihood_development_epic.md`. Build a reproducible profiling harness in @autofit_profiling using the current Nautilus/PyAutoFit integration. Do not issue the umbrella or start later optimisation phases as part of this task.

## Scope: one profiling-harness PR

1. Read current instructions, existing generic search.fit breakdown and accepted fixtures. Pin Python, Nautilus release/source, PyAutoFit revision, backend, platform, CPU/core allocation, process start method, thread limits, seeds and sampler settings in each run manifest. Reconcile the July NN-overhead study and August pool repairs linked by the epic; treat historical measurements as context, not a current baseline.
2. Start with one analytic correlated Gaussian target whose evidence/posterior are known. Run direct Nautilus and the equivalent @PyAutoFit wrapper with identical priors/settings. Cover serial and a small available multicore setting with real CPU work; add fixed, random and parameter-correlated latency variants that leave numerical likelihood values unchanged. Use the existing data/result conventions.
3. Instrument useful non-overlapping timing boundaries and event IDs: worker startup, prior conversion, likelihood compute, dispatch/serialization where observable, result collection, neural training/prediction, geometry/proposal sampling and checkpoint/output. If an upstream boundary cannot be observed safely, explicitly mark it unavailable and use a profiler; do not patch production Nautilus internals just to manufacture precision.
4. Measure instrumentation overhead against uninstrumented runs. Report parent wall time separately from aggregate worker CPU/service times, worker idle gaps, batch duration and tail wait. Include likelihood-count and sample/ESS/evidence diagnostics so a throughput win cannot conceal extra work or altered results.
5. Add focused harness checks: accounting with reordered completions, identical numerical targets under latency injection, timing units and manifest completeness. Run a local smoke/pilot small enough for this environment. Add commands for the subsequent real-lens and dimension-sweep campaign; do not submit large HPC/GPU jobs in this implementation task.
6. Publish the local pilot as exploratory evidence and rank the measured costs; if this environment cannot reproduce a real production condition, name the missing witness. Recommend the next single CPU optimisation and its expected maximum end-to-end payoff from the measured cost share.

## Ownership handoff

The epic's Pulse/Insight links are the domain entry points. Before real benchmark campaign execution, resolve/create the scoped canonical domain task through its owner and link it back; do not duplicate or resume paused campaigns in this Mind task. Existing accepted lens fixtures and parity requirements are authoritative. If substantial reusable PyAutoFit instrumentation is required, split that into its own dependency PR rather than expanding this harness task silently.

## Acceptance and non-goals

- One reproducible command per baseline case; manifest plus readable bottleneck/timeline report; uninstrumented control; no fabricated speedup.
- Exercise parameter-correlated runtime to distinguish scheduler effects from target changes. All generated points in each logical batch remain accounted for; do not use a first-finished subset.
- No default changes, neural-network removal, new sampler, fork publication, asynchronous adaptation or JAX port. Preserve the worker-initializer and serial-sampler-pool safety fixes.
- CPU-first initial development is ready. Hardware-dependent scored validation remains a separate campaign step; this phase is complete when the harness, tests and honest local pilot are reviewable, not when every CPU/GPU matrix row has run.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:nautilus_baseline_input.md -->

## Approved implementation clarification (2026-11-10)

Phase 0a delivers the controlled harness and local pilot in autofit_profiling#8. Match resolved stopping criteria, n_batch, checkpoint/run-call cadence and likelihood-only pool topology explicitly; PyAutoFit is a pinned measured dependency, not a source-edit target. The implementation plan is on the issue.

Phase 0b is the separate, pending canonical profiling campaign including the dimension sweep and representative targets. Phase 0 is complete only after both outputs exist; finishing this member does not establish the dimension baseline. No phase-0b campaign is issued or executed here.

The human approved the plan and feature/nautilus-cpu-profiling-baseline branch and authorized implementation after the task-specific Heart RED override. Merge remains human /prm.

## Phase 0a review handoff — 2026-11-10

PR: https://github.com/PyAutoLabs/autofit_profiling/pull/9

Implementation and local pilot are reviewable at f602ba4. All 52 selected runs use the same dependency revisions/content; 26 trace/control pairs preserve posterior hashes and likelihood counts. The recovery record retains one interrupted attempt and ten superseded successful attempts excluded after shared dependency drift. Detached dependency worktrees and source-drift checks now guard the run.

Validation: 40 tooling tests, Ruff lint/format, four direct/wrapped × one/two-worker resume checks, watchdog probes with tracing off/on, timeout receipt, trace accounting, catalogue/history validation and links passed. GitHub lint was pending at PR-open. Author review only; no independent review claimed.

Neural-network training and bound geometry dominate this small Gaussian target. Shared-host variability prevents a precise overhead or speedup claim. The report proposes checkpoint batching as the next bounded experiment (ideal share-based upper bound about 1.13x direct / 1.10x wrapped), with interruption/resume requirements. No optimization or phase-0b campaign was implemented.

Heart remains RED: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure" (2026-11-10T12:13:48.638875+00:00). Existing task-specific human override covers this development PR; merge remains human /prm with green required checks.
