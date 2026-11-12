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

## Implementation checkpoint
# PyAutoGalaxy feature review #276

Applied, staged and validated; no source commits, pushes or PRs yet. Awaiting live development-only Heart RED override for #276.

22 scripts preserve executable ASTs; 22 regenerated notebooks validate and preserve every code cell; 97 notebook links resolve; 21 approved drafts and images match; all 21 linked from both overviews; recent root walkthrough and new-user guide preserved; full RTD feature-page Sphinx build passes with warnings as errors; navigator, search-memory, size guard and staged whitespace checks pass. Numerical suites were not rerun for documentation-only changes; required CI remains mandatory before merge.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autogalaxy-features-review
Branch: feature/autogalaxy-features-review

## Exact Heart RED reasons
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: on branch feature/autogalaxy-features-review (not main)
- PyAutoGalaxy: 7 uncommitted source change(s)
- PyAutoLens: 1 uncommitted source change(s)
- PyAutoLens: 35 commit(s) behind origin
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Next: after task-specific approval, record the override in all four required sinks and commit/push/open PyAutoGalaxy PR first, then workspace PR. Do not merge.

## Development-only Heart RED override

Live user authorization: "Approve development-only override for #276", replying to the task-specific request to commit, push and open both PRs for review, with no merge or release.

Exact RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: on branch feature/autogalaxy-features-review (not main)
- PyAutoGalaxy: 7 uncommitted source change(s)
- PyAutoLens: 1 uncommitted source change(s)
- PyAutoLens: 35 commit(s) behind origin
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Passed branch checks: 22 script ASTs and all notebook code cells preserved; 22 notebook schemas valid; 97 notebook links resolve; approved text/image parity; full feature-page Sphinx build with warnings as errors, navigator, search-memory, size and whitespace checks pass. Numerical suites not rerun for documentation-only scope; required CI remains mandatory. Human approved previews and implementation.

No release, merge or CI bypass authorized.

## PR-open checkpoint
- Library PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/710
- Workspace PR: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/277
- PyAutoGalaxy head: e2cd2b5bafc81d8123f5777fc1beb27947933cdd
- autogalaxy_workspace head: 9090eb78b0aba5f53ca2edede3c770da35128d20
- Both open for review; no merge or release. Live development-only Heart RED override recorded in issue, PR bodies, active registry and first autonomy-log table.
- Next: human review; on a separate explicit merge request, verify every exact-head CI job and the release freeze, merge library first, then close #276.
