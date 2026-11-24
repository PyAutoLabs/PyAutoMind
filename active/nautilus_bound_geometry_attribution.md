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
Status: draft producer PR #19 open for human review

## User request (verbatim)

> ok continue to next task

## Scope

The [epic ledger](../draft/feature/autofit/nautilus_fast_likelihood_development_epic.md) identifies bound construction as the next CPU profiling target. The [preceding member](../draft/feature/autofit/nautilus_parent_cpu_slowdown.md) recovered the twelve 10D, seed-2 fits in RAL job 415196. Start with the two ordinary serial controls and their frozen reference. @autofit_profiling owns the experimental producer.

1. Validate the input receipts. Compare corresponding build ordinals, calls and scientific outputs. Separate enclosing time, nested neural work and the remaining geometry time.
2. Inspect the pinned implementation and retained checkpoint structure. Use only operation names and timings the evidence supports. Identify a bounded, representative build or set of builds for finer attribution and explain the selection.
3. If the traces omit inner timings, design the smallest matched instrumented comparison that can identify the costly operations. Use a local engineering pilot with explicit resource bounds and an uninstrumented control. A campaign requires the canonical domain task first.

The scope preserves the four native neural networks, serial training and existing pool safety. The wider 30D evidence check, sampler optimization, JAX acceleration and Pulse promotion remain separate decisions. Merge stays human.

## Result — 2026-11-24

[Draft PR #19](https://github.com/PyAutoLabs/autofit_profiling/pull/19) contains the verified replay, exact input fingerprints and matched timings. All eleven checkpoint geometries passed. The minimum-volume enclosing ellipsoid routine accounted for 97.3% and 97.4% of the local outer mixture constructor. These fractions do not establish its share of whole-bound or fit time on RAL. Producer head `8f1572f6bd6d5bfb2a7ded3078b4662519360557`. The packaged replay, input rejection checks, 111 Python 3.12 tooling tests, Ruff and catalogue validation passed. The scoped Heart gate was green and deferred the producer to PR checks. Merge stays human.
