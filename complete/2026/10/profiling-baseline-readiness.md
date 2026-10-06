# Shipped — profiling-baseline-readiness

Completed: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/384 (closed)
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/385 (merged)
Head: 62a6ad1e82735e360c7cf25be62253a286493b17
Merge: b8b2f1a149812ab4043cf9e2261464c44d9e2b81

Phase 6 defines the proposed fresh baseline contract and standard-library validate/enumerate/report tooling. The matrix has 1,044 slots:620 unverified,366 unsupported,58 CPU device-memory slots not applicable.177 unresolved scientific choices remain blockers. Reports screen hashes, matching context, freshness declarations, load/repetition/correctness observations and CPU timeout exclusions but always retain accepted:false. Physical execution and scientific suitability require human verification.

Validation:1,126 full tests passed,6 skipped; final46 focused passed; Ruff, browser interactions, catalogue/Pulse contract, wiki, dashboard, artifact-layout and HPC submit contracts passed. Independent review CLEAN at exact tree a4df8471e2e910ce16f1dc188b771a23353c086a. Exact-head CI37470508592/job112292448183 completed successfully, every test leg green. Full clone ancestry to fetched main verified with zero unmerged commits.

Current human /prm authorized merge. Ship Heart YELLOW acknowledged for autogalaxy_workspace, autolens_workspace and euclid_strong_lens_modeling_pipeline open PR7d old; release validation stale because PyAutoNerves moved. No RED override or release authorization. No jobs, archive promotion, pin changes or temporal charts. Pulse retains the pending separate collection/acceptance campaign; compile builder and other capability gaps remain explicit.

Evidence archived under .worktree-archives/profiling-phase6-20261006/profiling-baseline-readiness/. Synthetic fixtures preserved. Worktree held only reproducible test/browser caches in addition to source and archived evidence, no irreplaceable scientific products.

## Original prompt

# Profiling baseline readiness

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: medium
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-06

## Original request

ok do phase 6

Parent: draft/feature/pyautopulse/profiling_setup_browser.md (approved Phase 6).

## Scope

@autolens_profiling: Define a draft, versioned baseline campaign specification and a pure stdlib dry-run/report CLI. Enumerate the declared dataset/model/instrument matrix across device, precision and measurement slots. Preserve explicit missing capability and setup/hardware/revision unknowns. Validate evidence against a frozen specification without promoting results or updating pins.

## Plan

1. Add baseline/campaign.json with exact configuration requirements, frozen-revision fields, host/thread/load bounds, timing synchronization/warmup/repetitions, compile cache states, distinct memory methods and correctness witnesses. Unknown choices block readiness.
2. Add scripts/misc/tooling/baseline_readiness.py with validate, enumerate and report read-only commands, deterministic JSON output, source/campaign identity checks, CPU usability exclusions and rejection of archived/mismatched evidence. Never execute profiling or accept results.
3. Add tests for matrix completeness, absent capabilities, unknown settings, frozen spec identity, unsafe/archived evidence, units/method mismatch, CPU exclusions and valid synthetic review candidates.
4. Document the campaign and the later separate compute/acceptance authorization in baseline/README.md and wiki/campaigns/setup_baseline.md; run unit, lint, wiki and appropriate no-job checks plus independent review.

Tier: judge — merge mode: human /prm.

No profiling jobs, baseline pin changes, archive promotion or temporal charts. No Heart RED override or merge permission inherited from previous sessions.

Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/384
