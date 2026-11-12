# New User Guide rebalance

Completed 2026-11-12. Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/664

Restored helpful guidance around concise selection cards in the PyAutoLens RTD New User Guide and main autolens_workspace start_here notebook. Preserved images, destination links, merged #658 multi-band/weak-lensing additions, the executable walkthrough and Features gallery.

## Merge receipts
- PyAutoLens#856: 63f21ac04acb9c491ed93530cc4676087b6106a4
- autolens_workspace#665: 639a8ae2671a20f4f7f7175c852948400fc45095

## Validation and authorization
Focused Sphinx build with warnings as errors; notebook regeneration, schema and executable parity; retained images/URLs; browser image checks; navigator/search-memory/size checks passed. Ten exact-head CI jobs passed. One workspace smoke job skipped; live human approved: “Yes, I approve merging both New User Guide PRs with the smoke skip.” Freeze clear. Development-only Heart RED override #664 recorded at ship. No release performed.

Review bundle: C:\Users\Jammy\Workspace\Science\scratch\new_user_guide_rebalance_20261112\applied\index.html

## Original prompt

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
