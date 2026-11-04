## howtogalaxy-ch3-parity
- issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/101
- completed: 2026-11-04
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/102
- merge: 2d873b8af0a97f3ac5ddd26f8d09c51ba2153468
- summary: Ported the approved HowToLens Chapter 3 teaching improvements to directly observed galaxies: Goldilocks/log-evidence selection, mapping support and positivity, Fit Problems, and a combined Adaptive Reconstruction lesson. Preserved the original combined MGE/pixelization model-fit executable flow as Tutorial 5. Regenerated notebooks and navigation.
- validation: All eight GitHub jobs passed on 5d98c61, including Python 3.12 and 3.13 smoke; all 30 local executable smoke scripts passed. Independent review CLEAN with claim dispositions. Notebook schema/narrative parity/contents, API, strict declarations, navigation/catalogue determinism and terminal-completeness checks passed.
- limits: Full-size 1/3/4/5 passed. Full-size Tutorial 2 was terminated with SIGTERM/143 during its inherited fine-mesh comparison after the revised evidence section completed; its complete capped smoke passes. Nonlinear samplers use test mode 2, so posterior convergence is not validated.
- review-bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtogalaxy_chapter3_2026-11-04/index.html
- merge-authority: Explicit human prm; no release or CI override. Heart at shipping was YELLOW for the previously acknowledged AutoFit workspace timeout, with a stale release-rehearsal gap.

## Original prompt

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

## PR-open handoff — 2026-11-04
PR: https://github.com/PyAutoLabs/HowToGalaxy/pull/102
Commit: 5d98c61491cd7f03486731a855089e1b11d87d06
Status: awaiting human merge; judge tier, decision-taken. No scheduled monitoring.

Applied the Goldilocks/log-evidence explanation, mapping support and positivity, Fit Problems and one adaptive lesson. Original Model Fit is Tutorial 5 with its executable AST preserved. All 30 canonical smoke scripts pass; 30 generated notebooks validate, all five Chapter 3 contents match, narrative parity/API/navigation/search-memory/strict declarations/catalogue determinism/completeness pass. Independent review CLEAN with claim dispositions.

Full-size Tutorials 1, 3, 4 and 5 pass. New 3/4 captured 21/37 figures, with all coefficient scans evaluated. Full-size Tutorial 2 was terminated (SIGTERM/143, no Python traceback) during the inherited fine-mesh resolution comparison after the revised evidence section completed; capped Tutorial 2 passes completely. Nonlinear searches use mode 2 and do not establish convergence.

Heart at shipping: YELLOW only for the same-conversation acknowledged AutoFit workspace timeout (cloud#41432188469, MultiStartResumeNaNCounters.py); current release rehearsal absent is a STALE gap. Canonical manifest check clean. Heart smoke does not register howtogalaxy, so its repository-owned CI runner ran in the isolated task venv with declared optional dependencies.

Review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/howtogalaxy_chapter3_2026-11-04/index.html
Logs, validation report and independent review: task bundle review/; smoke JSON/Markdown: HowToGalaxy/test-results/.
