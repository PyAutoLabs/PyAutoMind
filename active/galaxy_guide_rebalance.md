Issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/281
# PyAutoGalaxy New User Guide rebalance
Type: docs
Consequence: judge
Targets: @PyAutoGalaxy @autogalaxy_workspace

## Original request
This looks good. Apply the revised PyAutoGalaxy New User Guide to RTD and keep the main start_here notebook consistent. Open both PRs for review, don't merge yet.

## Approved plan
Apply the reviewed draft at Science/scratch/galaxy_new_user_guide_rebalance_20261112/overview_2_new_user_guide.md. Shorten selection cards and restore explanatory guidance on choosing/running examples, Colab, HowToGalaxy and next steps. Keep all images and destination links. Synchronize root start_here.py, regenerate start_here.ipynb and synchronize markdown/start_here.md. Preserve the executable walkthrough and Features gallery. Validate Sphinx, notebook schema/executable parity, image/link retention, browser rendering, navigator, search-memory and size checks. Open two review PRs only; no merge or release.

Tier: judge — merge mode: human /prm
Branch: feature/galaxy-guide-rebalance

## Validated checkpoint
Approved text applied to RTD and root notebook. Strict focused Sphinx, notebook schema/code parity, preserved images/URLs, navigator/search-memory/size checks pass. Executable walkthrough and Features unchanged. PR bodies: organs/PyAutoMind/tmp/galaxy_guide_rebalance/*_pr.md. Applied preview: Science/scratch/galaxy_new_user_guide_rebalance_20261112/applied/index.html. No source commits or PRs yet; ship gate pending.

## PRs open — 2026-11-12
Live user approved development-only Heart RED override #281. Committed/pushed: PyAutoGalaxy c6182a63, autogalaxy_workspace 9ee49e9. Review PRs: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/714 and https://github.com/PyAutoLabs/autogalaxy_workspace/pull/282. No merge or release.
