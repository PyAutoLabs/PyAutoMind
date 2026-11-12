Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/664
# New User Guide rebalance
Type: docs
Consequence: judge
Targets: @PyAutoLens @autolens_workspace

## Original request
This looks much better. Apply the revised New User Guide to the RTD and keep the main start_here notebook consistent. Open PRs for review, don't merge yet.

## Approved plan
Apply the reviewed draft at Science/scratch/new_user_guide_rebalance_20261112/overview_2_new_user_guide.md. Shorten scale cards, restore explanatory prose for choosing and running examples, Colab, HowToLens and next steps. Preserve images and destination links, plus newly merged #658 multi-band and weak-lensing additions. Synchronize root start_here.py, regenerate start_here.ipynb and synchronize markdown/start_here.md, keeping executable code and the Features gallery unchanged. Validate Sphinx, notebook schema and executable parity, preserved links/images, navigator and size checks. Open two review PRs; no merge or release.

Tier: judge — merge mode: human /prm
Branch: feature/new-user-guide-rebalance

## Validated checkpoint
Approved guide applied; merged #658 additions preserved. Sphinx, notebook schema/executable parity, images/URLs, browser, navigator/search-memory/size checks pass. Features and executable walkthrough unchanged. Task-specific Heart RED override #664 pending; no source commits or PRs yet. Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/new_user_guide_rebalance_20261112/applied/index.html. PR drafts: organs/PyAutoMind/tmp/new_user_guide_rebalance/*_pr.md.

## PRs open — 2026-11-12
Live user approved development-only Heart RED override #664. Committed and pushed: PyAutoLens ef3d66637, autolens_workspace 11d16c17. Review PRs: https://github.com/PyAutoLabs/PyAutoLens/pull/856 and https://github.com/PyAutoLabs/autolens_workspace/pull/665. No merge or release.
