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
