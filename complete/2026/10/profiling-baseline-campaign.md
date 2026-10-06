# Shipped — profiling-baseline-campaign

Completed: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/17 (closed)
PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/18 (merged)
Head: b4e4c80a9d22643db9156b956db4635523078ad4
Merge: 60119db3d0e6d0412b55a4b41ac1ee514936608b

Registers the setup-baseline campaign and pending scientific collection/acceptance task as needs-decision. Project specification links pin reviewed project commit62a6ad1. Existing campaign/task rows, last_checkin, snapshots and receipts are preserved. Future collection is unissued and requires explicit compute authorization; acceptance/promotion requires a later human decision.

Validation:189 tests, Ruff/format, offline rendering/check passed. Independent review CLEAN, final immutable-link substitutions checked. Exact-head CI37470550205/job112292591895 (refresh) and37470549831/job112292592828 (lint) all successful; every test leg green. Full clone ancestry to fetched main verified with zero unmerged commits. Project PR385 merged first.

Current human /prm authorized merge. Current ship Heart YELLOW reasons acknowledged: autogalaxy_workspace, autolens_workspace and euclid_strong_lens_modeling_pipeline open PR7d old; release validation stale after PyAutoNerves moved. No RED override. No jobs, archive acceptance, baseline pin changes or temporal charts.

Evidence archived under .worktree-archives/profiling-phase6-20261006/profiling-baseline-campaign/. Synthetic fixtures preserved; remaining ignored files are disposable Python/pytest/Ruff caches.

## Original prompt

# Profiling baseline campaign

Type: feature
Target: pyautopulse
Repos: PyAutoPulse
Difficulty: medium
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-06

## Original request

ok do phase 6

Parent: draft/feature/pyautopulse/profiling_setup_browser.md (approved Phase 6).

## Scope

@PyAutoPulse: Record the dedicated setup baseline campaign and pending collection/acceptance task in Pulse. Link the project specification and its qualification limits. Render the board offline without restamping check-in, ingesting measurements, changing pins or authorizing jobs.

## Plan

1. Add a needs-decision baseline campaign in campaigns.yaml and a pending task under tasks/ describing missing revision/hardware/setup choices, compile capability, separate compute authorization and later scientific acceptance.
2. Link the project specification and Phase 6 implementation issue/PR; state archived rows are context only and CPU arrays use ral.
3. Regenerate board offline with current Brain renderer and check the committed snapshots without fetching. Preserve last_checkin, unrelated campaign rows and coordinated heading edits.
4. Run Ruff, full Pulse tests, offline check and independent review.

Tier: judge — merge mode: human /prm.

No profiling jobs, baseline pin changes, archive promotion or temporal charts. No Heart RED override or merge permission inherited from previous sessions.

Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/17
