# HST/MGE pilot observations: bounded project-owned producer

Filed: 2026-10-13
Type: feature
Consequence: judge
Target: @autolens_profiling
Status: draft; detailed implementation plan and review still required

## Original request

> ok go

Context: prepare the HST/MGE fp64 CPU pilot and identify bounded instrumentation
work. This prompt records the implementation follow-up, not compute permission.
Canonical intent: [Pulse pilot](https://github.com/PyAutoLabs/PyAutoPulse/blob/feature/hst-mge-cpu-pilot-plan/tasks/hst_mge_cpu_pilot.md).
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
