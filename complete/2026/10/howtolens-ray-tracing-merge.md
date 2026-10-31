# HowToLens ray-tracing consolidation

Merged https://github.com/PyAutoLabs/HowToLens/pull/106 on 2026-10-31 as e807cf9000b38814b94ab70bd799dbc5128436eb. Issue #105 closed.

Tutorial 2 now includes units and multiple galaxies; Tutorial 3 combines intuitive ray tracing with optional mathematics. Retired the separate formalism tutorial and renumbered Data, Fitting and Summary to 5–7. Updated notebooks, rendered pages, figures and navigation.

Human approved prose in five-block batches and explicitly authorized merge via prm. All eight CI jobs passed, including both Python 3.12 and 3.13 smoke legs. Local full smoke: 49 passed, zero failed. Generated notebook parity and actual rendered lessons validated.

Heart RED development override remains development-only; no release performed. Human approved deleting the worktree and generated data. Removed the task worktree (including datasets/output) and the proven-merged local feature branch on 2026-10-31. Human review copies in Science/scratch remain available.

## Original prompt

# Rebalance HowToLens ray tracing

## Completed review and implementation — 2026-10-31
- All prose/code reviewed and approved in five-block batches.
- Tutorial 2 includes units, shear, satellite and multiple galaxies; Tutorial 3 combines intuitive ray tracing with optional mathematics using one tracer.
- Includes the approved 2D deflection-difference plot plus median, shallow-profile experiment and fixed-source Fermat surface.
- Separate Tutorial 5 retired; human approved shifting old Tutorials 6–8 to 5–7. All navigation, dataset references, notebooks, rendered Markdown and catalogue updated.
- PR: https://github.com/PyAutoLabs/HowToLens/pull/106
- Commit: 3cf2463df13c66ddae33ab5d647db76d9f58a0a4
- Official Heart smoke: 49 passed, 0 failed (Python 3.12, profile_smoke.yaml). Six notebook format/source parity checks and 38 tutorial completion checks pass; all five changed rendered lessons executed successfully.
- Numerical and visual checks pass for the difference map, SIS/power-law critical curves, Einstein mass and fixed-source Fermat surface.
- Final smoke log: scratch/heart_smoke.log; result: task worktree test-results/howtolens__scripts__script.json.
- Review copies: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_ray_tracing_merge_2026-10-31/.
- Next: human reviews PR and invokes /prm after required checks pass. No merge/release authorized.

Type: docs
Target: @HowToLens
Issue: https://github.com/PyAutoLabs/HowToLens/issues/105
Issued: 2026-10-31

## Overview
Rebalance HowToLens Chapter 1: Tutorial 2 teaches practical ray tracing, units and multiple galaxies; Tutorial 3 merges the former Tutorials 3 and 5 into an optional mathematical explanation using one tracer.

## Plan
- Apply human-approved Units and five multi-galaxy blocks to Tutorial 2.
- Review Tutorial 3 in batches of five prose/code blocks before applying them.
- Retain intuitive critical-curve/caustic explanations alongside their mathematics; assume the lens equation from Tutorial 2.
- Retire the separate Tutorial 5 and update navigation/references after review.
- Regenerate notebooks/catalogue and validate the resulting scripts.

Tier: judge — merge mode: human /prm.

## Implementation
Repository: HowToLens; clean main at e986a4a before work.
Branch: feature/howtolens-ray-tracing-merge
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ray-tracing-merge/HowToLens
Canonical files: scripts/chapter_1_introduction/tutorial_2_ray_tracing.py, tutorial_3_more_ray_tracing.py, tutorial_5_lensing_formalism.py.
Tutorial 2: preserve existing lesson, append Units, More Complexity and Multi Galaxy Ray Tracing, replace Wrap Up and correct opening signposts/contents.
Tutorial 3: initial setup, illustrative code, distances (including reduced deflections), convergence, deflections, potential, shear/magnification, critical curves/caustics, Einstein radius, time delays.
Use one tracer throughout formalism; no formalism_tracer alias. Do not apply unapproved prose.
Validate syntax, execute the affected lesson with actual plotting, then regenerate through PyAutoHands and perform required ship checks when review is complete.

## Approval and current phase
Human approved all five-block reviews, moving Units and multi-galaxy ray tracing to Tutorial 2, and closing the numbering gap. This task does not carry merge authority.
Human said: "I approve development on heart red".
RED reasons reported: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; Release readiness: release validation FAILED (stage integrate); autogalaxy: red; Release validation: NOT release_ready — v2026.10.31.1.dev85201 profile=release (2026-10-31T08:04:07+00:00); validation_report/stages/integrate: fail; autolens_profiling: red; Worktree drift: 0 orphan / 0 missing / 1 dirty.

Current Heart RED reason at PR-open: `release validation FAILED (stage integrate)`. Development-only override recorded on issue #105, PR #106, active.md and autonomy_log.md. No release or failed-check bypass.
