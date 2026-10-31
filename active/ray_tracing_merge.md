# Rebalance HowToLens ray tracing

## Review checkpoint 2026-10-31
- Tutorial 2 approved Units / More Complexity / Multi Galaxy Ray Tracing / Wrap Up applied in task worktree, plus contents/opening signposts.
- Actual complete Tutorial 2 execution passed on existing workspace Python 3.12 smoke environment. Singular-centre Hessian warning reported (1/10201 points); no exception.
- Log: .worktrees/howtolens-ray-tracing-merge/scratch/tutorial_2_runtime.log (workspace-relative).
- Tutorial 2 notebook regenerated and validated with PyAutoHands; catalogue rebuilt.
- Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_ray_tracing_merge_2026-10-31/tutorial_2_four_galaxies.png
- Tutorial 3 and 5 sources remain unchanged pending remaining block review. Do not remove Tutorial 5 yet.
- Next review: deflection integral, potential, numerical derivative comparison, Hessian/Jacobian and shear. Preserve single tracer and reviewed distances/convergence framing.

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

Tier: undeclared — merge mode: human /prm.

## Implementation
Repository: HowToLens; clean main at e986a4a before work.
Branch: feature/howtolens-ray-tracing-merge
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ray-tracing-merge/HowToLens
Canonical files: scripts/chapter_1_introduction/tutorial_2_ray_tracing.py, tutorial_3_more_ray_tracing.py, tutorial_5_lensing_formalism.py.
Tutorial 2: preserve existing lesson, append Units, More Complexity and Multi Galaxy Ray Tracing, replace Wrap Up and correct opening signposts/contents.
Tutorial 3: initial setup, concise code, distances (including reduced deflections), convergence, deflections, potential, shear/magnification, critical curves/caustics, Einstein radius, time delays.
Use one tracer throughout formalism; no formalism_tracer alias. Do not apply unapproved prose.
Validate syntax, execute the affected lesson with actual plotting, then regenerate through PyAutoHands and perform required ship checks when review is complete.

## Approval and current phase
Human approved the five Tutorial 2 multi-galaxy blocks, and moving Units to Tutorial 2. This task does not carry merge authority.
Human said: "I approve development on heart red".
RED reasons reported: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; Release readiness: release validation FAILED (stage integrate); autogalaxy: red; Release validation: NOT release_ready — v2026.10.31.1.dev85201 profile=release (2026-10-31T08:04:07+00:00); validation_report/stages/integrate: fail; autolens_profiling: red; Worktree drift: 0 orphan / 0 missing / 1 dirty.
