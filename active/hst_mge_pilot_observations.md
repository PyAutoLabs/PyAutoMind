# HST/MGE pilot observations: bounded project-owned producer

Filed: 2026-10-13
Type: feature
Consequence: judge
Target: @autolens_profiling
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/415
Status: approved implementation

## Original request

> ok go

Context: prepare the HST/MGE fp64 CPU pilot and identify bounded instrumentation
work. This prompt records the implementation follow-up, not compute permission.
Canonical intent: [Pulse pilot](https://github.com/PyAutoLabs/PyAutoPulse/blob/71c93fc285a081ffb1f0f506694c043a15ad4e22/tasks/hst_mge_cpu_pilot.md).
Preparation issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/53.

## Scope to plan through start-dev

Add an opt-in project-owned runner for the existing imaging-mge-runtime-v1 HST
fp64 jit workload. Use fresh processes for each cold/seed/warm leg; record seed
cost, trace+lower, compile, first execution and individual unrounded synchronized
steady samples separately. Retain actual resolved configuration, input hashes,
software/environment, CPU affinity, threads, load and resource/timeout outcomes.
Require positive, workload-associated cache-hit evidence; unknown stays unknown.
Expose explicit cold/seed/warm identities and retain failures. No hidden retries.

Produce an honest observation/receipt path: identify whether a pilot-specific
specification and report can reuse baseline-readiness without changing its full
1044-slot scope or claiming an unfrozen baseline. Do not blindly copy planned
context or declare scientific qualification from schema validity. This design
choice needs review before implementation. A raw pilot envelope is acceptable
only if explicitly distinct from accepted baseline evidence.

Consume an independent correctness reference and user-reviewed tolerances; never
invent either. Capture likelihood and reconstruction parity, normalization,
reference provenance, and both absolute/relative error. Same-code eager/JIT
consistency alone is insufficient for the scientific witness. If the witness
adapter requires broader science work, keep that decision in Pulse rather than
silently extending this task.

## Non-goals

No broader builder coverage, gradient/mixed/GPU path, catalogue-route migration,
old output conversion, default/pin changes, production dataset creation or compute
submission. Do not freeze the main campaign or alter the existing probe's legacy
contract. Existing project sources/results own execution and measurements.

## Validation required by the future implementation plan

Use unit/contract fixtures for process boundaries, raw sample counts, isolated
caches, unknown/missing hit evidence, actual-context mismatch, timeouts and output
non-overwrite. Tiny synthetic CPU fixture may validate implementation, but never
qualifies the production dataset. Run applicable project lint/tests/generated
checks and review source hashes. Production collection is a later authorization.

## Open decisions

Exact producer/spec/report design; reference node and memory; immutable stack and
lock; input/configuration hashes; independent witness/tolerances; load method;
collection window and resource approval. Proposed budget is in Pulse, not an
execution grant. Return to Pulse after shipping; do not close the scientific task.

## Detailed implementation proposal — 2026-10-13

Raw-pilot scope approved by the human on 2026-10-13 ("ok continue"). No production compute authorized.

Brain feature decision recommends phasing (large, scientific ambiguity). First
ship the raw observation runner below. Keep scientific witness generation,
full-campaign baseline integration and production collection as explicit later
work in Pulse. This is fixed-parameter likelihood profiling, never inference.

### Phase 1: raw observation runner

1. Add `scripts/misc/jax_compile/pilot.py` as the opt-in CLI/orchestrator and
   `pilot_worker.py` as the child-process implementation. Reuse `current.py`'s
   HST/fp64 workload builder without changing the existing probe's output format.
   Validate all inputs before process creation: exact supported objective, dataset
   files, CPU affinity, x64, process/repetition caps and a new isolated output
   directory. No shell command interpolation, automatic simulation or submission.
2. A new run directory owns raw records, stdout/stderr, isolated caches and a
   manifest. Refuse overwrite and path/symlink escape. Default command is a
   read-only plan; execution requires an explicit run option. Expose the complete
   process count and upper time budget in the plan. Enforce per-process timeout,
   total process budget, sequential execution and fail-stop behavior; retain
   partial receipts after worker failure. Kill/reap the child process group on
   timeout or cancellation. No retries and no silent backend fallback.
3. Cold, seed and warm workers start fresh interpreters with explicit effective
   CPU/x64/thread/cache settings and fixed affinity before scientific imports.
   Cold caches must be empty. A seed and its warm worker share a dedicated cache;
   unrelated pairs do not. Record a seed-to-warm link and compare actual workload,
   source, software, flags and input hashes; mismatch blocks warm interpretation.
4. Worker records separate setup, trace-plus-lower, AOT compile, first synchronized
   execution and process wall time. A separate runtime worker performs three
   untimed warmups then ten individually synchronized calls. Preserve full raw
   floating seconds, all output synchronization and actual counts. Do not retain
   just a rounded mean. Fixed parameters only: no sampler, search or optimization.
5. Capture JAX persistent-cache diagnostic events during the target executable's
   compile interval, including the module/key and original diagnostic text. Scope
   positive hits to that executable and the matching seed. Unknown diagnostics,
   helper-compilation hits, file counts or faster timing never imply a warm hit.
   An unsupported installed-JAX evidence format stays unknown with a reason.
6. Extend run-level provenance in the new envelope: actual host/CPU/OS, RAM,
   affinity, threads, JAX devices, package versions, clean/dirty Git identities,
   input/config/source hashes and effective cache settings. Report sampled load
   averages honestly as raw host observations, never as background load excluding
   this campaign. Missing independent correctness or validated background-load
   methodology must be explicit blockers, not inferred from clean CI.
7. Raw record schema: `profiling-pilot-observation`, version 1, objective identity,
   observed-at UTC, run/worker/seed IDs, outcome, raw metrics, provenance, cache
   evidence and qualification blockers. Always `accepted: false`; no
   `baseline-observation` or `origin: fresh-campaign` claims. A stdlib summary
   reports median/range/IQR for each like-for-like series, failures and incomplete
   legs. Refuse incompatible grouping. It neither imports historical rows nor
   emits baseline qualification, significance or performance-drift verdicts.
8. Add `scripts/misc/jax_compile/PILOT.md` documenting methods, CLI, failure
   semantics, incompatibility with legacy posterior pins and all outstanding
   collection decisions. Link from the compile README. Do not edit catalogue
   routes, main baseline manifest/readiness, existing measurements or pins.

### Validation and ship

Add `scripts/misc/test/test_jax_compile_pilot.py` with fake workers for orchestration
and real short subprocess fixtures for process isolation, timeout/reaping, stopped
partial runs, caps, non-overwrite and mismatch detection. Test cache-event
qualification against hit/miss/helper/ambiguous fixtures and raw sample collection
against a deterministic clock/synchronization spy. One tiny synthetic HST-style
CPU fixture may exercise builder/AOT/provenance within an explicit development
cap; it is not a production run or independent scientific witness. Use existing
project lint, focused tests, full applicable suite and generated-artifact checks.

Affected source repo: autolens_profiling only. Survey: main with pre-existing
untracked dataset/abell_1201/ (preserve); no active claim for this repo. Proposed
branch: feature/hst-mge-pilot-observations, isolated task worktree under .worktrees.
Pulse preparation #54 merged and closed 2026-10-13; this task now owns the
companion Pulse handoff claim.

Tier: judge — merge mode: human /prm. Stop at reviewed implementation PR; no
production compute, freeze, scientific acceptance or inference is authorized.


## Implementation validation — 2026-10-13

Project PR: https://github.com/PyAutoLabs/autolens_profiling/pull/416
Producer code reviewed CLEAN at b5b8160; generated-only follow-up 7571123.
Full suite on initial implementation: 1452 passed / 6 skipped; final provenance
fix: 32 focused tests passed. Small local CPU synthetic 11x11 image / 3x3 PSF,
fp64, one repetition, 60-second per-worker cap completed four distinct processes
(cold, seed, matching warm hit, runtime) on b5b8160. Ten raw runtime samples;
accepted false. No scientific correctness witness or performance claim.
Ruff, generated checks, browser and smoke passed. Heart STALE only for absent
release rehearsal, permitting development publication. Pulse: 206 tests and
offline board check passed. CI/merge remain pending.

Known qualification gaps remain with Pulse: independent witness/tolerances,
resolved solver-default audit, production host/environment lock/data identity,
background-load method and explicit collection authorization. No inference,
production profile, baseline freeze or default/pin change occurred.

Pulse companion: https://github.com/PyAutoLabs/PyAutoPulse/pull/55.
Final independent review CLEAN: project 7571123 and Pulse 80dca4b; Pulse 3078a2d only adds the project PR link. Both PRs open; lint in progress at handoff.
