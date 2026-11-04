# Bring HowToGalaxy Chapter 3 up to the approved HowToLens teaching standard

Type: docs
Difficulty: large
Autonomy: supervised
Consequence: judge
Target: @HowToGalaxy
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/101

## Original request
can we apply the changes to HowToGalaxy if we did not already happy for you to do this autonomously without me

## Scope
Audit current Chapter 3 against HowToLens PR #126. Transfer applicable evidence/Goldilocks explanations, early-content restoration, fit-problem motivation, adaptive reconstruction and bounded-memory experiments. Adapt all science to directly observed galaxies; do not import lens mass degeneracies, borders/ray tracing, Maresca figures or positions penalties. Preserve existing MGE-plus-pixelization model-fit teaching. Regenerate notebooks/catalogues and validate strict profiles, full-size numerical examples, smoke and independent review. Autonomous implementation/shipping authorized; no automatic merge requested.

## Plan
1. Preserve and improve Tutorials 1/2, including complete contents and the explicit log-evidence coefficient-selection rule.
2. Add Fit Problems followed by Adaptive Reconstruction, and retain the existing combined-model fit as the final lesson with repaired numbering/navigation.
3. Explain brightness-guided resolution and adaptive smoothing using unlensed galaxy images; keep reconstruction and decomposition caveats explicit.
4. Validate live API calls, science/numerical examples, generated notebook parity and canonical smoke; run strict environment-profile validation before shipping.
5. Prepare an open PR after the autonomous shipping gates pass. Tier: judge — merge mode: human /prm.

## Worktree
/home/jammy/Code/PyAutoLabs/.worktrees/howtogalaxy-ch3-parity/HowToGalaxy
Branch: feature/howtogalaxy-ch3-parity (base b6e4d2a).
