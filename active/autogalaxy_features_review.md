# PyAutoGalaxy feature introductions and images

Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/276
Issued: 2026-11-12
Consequence: judge
Difficulty: medium
Lane: local-dev

@PyAutoGalaxy @autogalaxy_workspace

## Original Prompt

I like these. Apply all 21 texts and images to autogalaxy_workspace, the main start_here.py and RTD, reusing the approved images as proposed. Open both PRs for review, don't merge yet.

## Approved Plan

1. Apply all 21 approved feature introductions from the 2026-11-12 review bundle, preserving teaching detail and executable behavior.
2. Reuse the approved RTD dataset/galaxy-system and shapelet figures; add the six approved galaxy-only image variants with their exact prompts.
3. Update workspace start_here.py and PyAutoGalaxy/docs/overview/overview_3_features.md with scientific use cases, feature links and these images. Preserve the recent new-user-guide introduction and existing technical teaching figures.
4. Regenerate 22 notebooks and navigation using PyAutoHands. Check draft/image parity, AST and notebook code-cell preservation, notebook schemas, local links, navigator, search-memory, size guard and Sphinx rendering.
5. Check current Heart readiness and open paired review PRs, library docs first. No merge or release.

Tier: judge — merge mode: human /prm

## Detailed Scope

Canonical sources: scripts/{imaging,interferometer,multi_dataset,multi_galaxy}/features/*/start_here.py; root start_here.py. No dataset-level features/start_here.py additions. Copy only approved images, with script image references targeting images/features or existing images/new_user_guide. Preserve shapelet basis and MGE teaching figures. Overview explanations must distinguish imaging PSF response from visibilities and galaxy photometry from lensing.

Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/autogalaxy_feature_review_20261112/

## Branch Survey

PyAutoGalaxy and autogalaxy_workspace canonical main clean, behind origin/main; new worktrees start at current origin/main. No active claims on target repos; legacy unregistered worktrees left untouched. Mind canonical contains other tasks, so isolated Mind worktree used.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autogalaxy-features-review
Branch: feature/autogalaxy-features-review
