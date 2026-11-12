# Consolidate the RTD Tutorials pages

Type: docs
Targets: @PyAutoLens @PyAutoGalaxy
Status: local implementation complete; issue/ship registration deferred, no PR requested
Date: 2026-11-12

## Original request

Review the Tutorials sections of the PyAutoLens and PyAutoGalaxy Read the Docs sites, including the HowToLens and HowToGalaxy landing and chapter-summary pages.

Use the recently merged New User Guides as the editorial reference:
PyAutoLens PR #839 and PyAutoGalaxy PR #705.

Help readers quickly understand what each chapter teaches, what background it assumes and which notebook to open. Use concise introductions, plain headings and direct notebook/Google Colab links where available.

Reduce repeated descriptions, promotional prose and excessive AI framing. Offer AI-guided learning briefly and optionally, without replacing the Python examples or scientific teaching.

Preserve the educational progression and necessary scientific detail. Suggest existing scientific figures or new diagrams where they clarify a concept; avoid decorative images.

Read PyAutoBrain’s writing and tutorial guidance. Verify chapter names, notebook locations and links against the actual HowToLens and HowToGalaxy repositories. Initially review only the RTD pages; flag any corresponding notebook changes separately.

Show me findings and a proposed structure first, then draft previews before applying changes. Do not raise PRs or modify Installation, Overview or General.

## User direction and approvals

> I dont think we need 5 RTD pages, one for each chapter, I thinkw e can make this all a lot more concise and also ensure links to chapters are like on the GItHub with a github / Colab type setup.

> Yes, show me draft previews of the two consolidated pages with the GitHub / Colab links. Don't apply changes yet.

> These look good, apply the two consolidated pages and preserve the old chapter links. Don't raise PRs yet, and leave Installation, Overview and General unchanged.

The conflict guard originally found installation-docs-polish claiming both repositories (now merged and closed; see [completion record](../../../complete/2026/11/installation-docs-polish.md)). Asked permission to proceed in separate worktrees restricted to Tutorials and its navigation block; user answered:

> Proceed with the separate Tutorials worktrees

## Local handoff

- Session: OpenAI Codex desktop; session ID unavailable.
- Worktree bundle: /home/jammy/Code/PyAutoLabs/.worktrees/rtd-tutorials-consolidated
- Both branches: feature/rtd-tutorials-consolidated
- Bases: PyAutoLens e4051fe31; PyAutoGalaxy 8c9260da.
- Applied approved preview wording in docs/howtolens/howtolens.md and docs/howtogalaxy/howtogalaxy.md.
- Five old chapter pages per project remain as orphan HTML redirect pages, with clickable fallback links to chapter table anchors.
- docs/index.md changes remove only the five old Tutorials navigation entries per project.
- Seven changed files per repository, uncommitted. No pushes or PRs.
- Installation, Overview and General unchanged; canonical checkouts and other task edits preserved.
- Focused Sphinx/MyST/Furo builds pass with -W; rendered wording matches approved previews; all ten redirect/fallback destinations and anchors verified; diff whitespace checks pass.
- Full API-doc builds, numerical suites and Colab execution not run for this prose-only scope.
- Heart at entry: YELLOW — Release YELLOW; monitoring RED; development permitted.
- Evidence and builds: scratch/rtd-tutorials-consolidated/ under the main workspace.
- Human review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/rtd_tutorial_review_2026-11-12/
- Next: review applied pages; register issue/claims through start_dev/create_issue before later shipping if requested. Installation is now merged; refresh the Tutorials branches against current main before shipping, preserving the Installation navigation. No merge/release authority.
