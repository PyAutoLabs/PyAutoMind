# Attribute CPU time inside Nautilus bound construction

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Phase: experimental 0b CPU geometry attribution
Difficulty: medium
Autonomy: supervised
Consequence: judge
Witness: Reconcile geometry wall and parent CPU across the same eleven bound builds in both exact-parity 10D serial controls. Identify the resolution of the existing timers and checkpoint data. Any ranking of inner operations requires a direct measurement on matched inputs with native neural bounds and sampler parity.
Lane: local-dev
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/18
Status: approved for a draft PR on 2026-11-24

## User request (verbatim)

> ok continue to next task

## Scope

The [epic ledger](../draft/feature/autofit/nautilus_fast_likelihood_development_epic.md) identifies bound construction as the next CPU profiling target. The [preceding member](../draft/feature/autofit/nautilus_parent_cpu_slowdown.md) recovered the twelve 10D, seed-2 fits in RAL job 415196. Start with the two ordinary serial controls and their frozen reference. @autofit_profiling owns the experimental producer.

1. Validate the input receipts. Compare corresponding build ordinals, calls and scientific outputs. Separate enclosing time, nested neural work and the remaining geometry time.
2. Inspect the pinned implementation and retained checkpoint structure. Use only operation names and timings the evidence supports. Identify a bounded, representative build or set of builds for finer attribution and explain the selection.
3. If the traces omit inner timings, design the smallest matched instrumented comparison that can identify the costly operations. Use a local engineering pilot with explicit resource bounds and an uninstrumented control. A campaign requires the canonical domain task first.

The scope preserves the four native neural networks, serial training and existing pool safety. The wider 30D evidence check, sampler optimization, JAX acceleration and Pulse promotion remain separate decisions. Merge stays human.
