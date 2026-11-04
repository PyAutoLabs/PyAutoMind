# HowToLens Chapter 3 approved implementation

Type: docs
Consequence: judge
Issued: 2026-11-04
Issue: https://github.com/PyAutoLabs/HowToLens/issues/125
Target: @HowToLens Chapter 3 only

## Current authorization

The human reviewed and approved blocks 1–66 in Codex chat 01a1a5a6-2da3-79e0-9b7b-ae8072a3ea02, including Goldilocks evidence, explicit coefficient choice, the revised search difficulty explanation, Chapter 2 Tutorial 5 positions likelihood penalty references, embedded Maresca Figure 1, restored Fit Problems and one consolidated adaptive tutorial ending with a real lens-model search. This supersedes the prior cancellation of Fit Problems and five-block review instruction. No merge authority.

Original implementation request, verbatim:
> Yes, go ahead and implement all the approved changes, audit tutorial 1 and the start of tutorial 2 for missing content, regenerate the notebooks and run the checks.

## Implementation

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ch3-approved/HowToLens
Branch: feature/howtolens-ch3-approved
Base: a7bd32c (Chapter 2 #124 merged)
Exact approved conversation and extracted blocks: ../review/approved_conversation.md and ../review/blocks.json in the task bundle.
Edit canonical scripts, preserve existing accepted early text, restore lost teaching content where not covered later; regenerate notebooks and catalogues. Validate full-size numerical examples/figures separately from profile-driven smoke. Keep Chapter 2 unchanged.
Heart at start: YELLOW (Release YELLOW; monitoring RED); development and validation only. No shipping override carried from earlier tasks.
