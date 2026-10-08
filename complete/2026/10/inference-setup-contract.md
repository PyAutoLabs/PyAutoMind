# Inference setup contract — phase 1 complete

- issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/13
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/14
- merged: 2026-10-08; 2d6ea0e4e45f6cc43df0133b38f50a8d4fcf0fe8
- authorization: human `prm, and continue through all phases autonomously to the end`

Version 2 reader, baseline/prepared problem identities, cold/warm/resume and
compilation/cache distinctions, work units and strict comparisons delivered.
157 tests, Ruff, offline validation passed. Both exact-head hosted runs and
all their jobs passed; only PR-disabled publication step skipped.
Parent draft/feature/pyautoinsight/inference_setup_redesign.md remains active
for producer, UI, assistant/wiki and literature candidates. No compute performed.

## Original prompt

# Inference setup and baseline-to-experiment contract

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight
Difficulty: medium
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/13
Epic: inference-setup-redesign (phase 1)

## Scope and approval

Implement the first phase of the approved design in @PyAutoInsight. Parent:
draft/feature/pyautoinsight/inference_setup_redesign.md (original request verbatim).
Human approved the design, baseline contract and start-mode distinctions, then
said "ok begin". No compute, acceptance or merge is authorized.

## High-level plan

1. Accept version 2 setup-oriented inference evidence while retaining v1 feeds.
2. Validate stable setup identities, baseline references and prepared problems.
3. Record cold/warm/resume initialization separately from compilation/cache state.
4. Refuse invalid or incompatible comparisons; preserve unknowns and archives.
5. Document the producer interface and prove reader compatibility with tests.

Tier: judge — merge mode: human /prm.

## Detailed plan

- insight/summary.py: retain existing envelope/record validation, add explicit v2
  routing and comparison controls for prepared problem, protocol and start mode.
- insight/catalogue.py (new): validate setup registry, baseline-stage references,
  experiment bindings, initialization sources and preparation timing semantics.
  Stable IDs are separate from paths; all record references resolve; duplicate,
  mismatched, nonfinite and unsafe data fail closed. Missing historical metadata
  is explicit, never inferred as an accepted or cold baseline.
- insight/registry.py and ingest/cache callers: inspect exact supported-version
  handling and allow v2 without changing the live v1 registry pin.
- REFERENCE.md: document v2 fields, lifecycle/migration, baseline acceptance and
  prepared artifact provenance, sampler cold/warm/resume vs JIT/cache state,
  initialization/preparation vs sampling clocks, typed diagnostics, and strict
  comparison behavior. No renderer or execution changes in this phase.
- tests: representative v2 SLaM baseline and cold/warm/resume experiments;
  dangling references, setup/stage mismatch, missing provenance, duplicate IDs,
  archived/unassessed baselines, invalid metrics/paths, mixed comparison controls,
  supported-version registry behavior and full v1 regression suite.
- Run required Ruff, full pytest, offline check; ship one reviewable PR.

## Survey

PyAutoInsight canonical main is clean, unclaimed; branch:
feature/inference-setup-contract. Later project/assistant canonical checkouts
contain unrelated untracked results/datasets and will use isolated worktrees.
PyAutoBrain is claimed by search-ext-a0c-fit-repair; this phase reads it only.

## Original phase authorization (verbatim)

ok begin

Full original request and intervening approvals are preserved in the parent.
