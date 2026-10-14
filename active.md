# Active Tasks

## hst-mge-pilot-qualification
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
- issued: 2026-10-13
- session: Codex; session ID unavailable
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/418
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/hst-mge-pilot-qualification
- next: Review and merge #418; independently validated witness implementation, coefficient tolerances and production collection remain separate pending work.
- repos:
  - autolens_profiling: feature/hst-mge-pilot-qualification

## search-ext-a4-decompose
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1684
- issued: 2026-10-14
- prompt: active/search_ext_a4_decompose_seed_family_bases.md
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a4-decompose
- epic: search-extensibility
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1685
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1686
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1687
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1685
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1686
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1687
- next: human /prm in order #1685 → #1686 → #1687 (stacked; #1687 carries Closes #1684). Open call in #1686 body: MultiStart explicit seed re-keys output folders (hash when not None) vs one-line override keeping it unhashed. Companion changes (Brain sampler_pipeline/reference.md ~129-136, developer-tier ultranest + pyswarms searches) listed in #1687 body — file as separate tasks after merge
- repos:
  - PyAutoFit: feature/search-ext-a4-decompose
  - PyAutoFit: feature/search-ext-a4-seed
  - PyAutoFit: feature/search-ext-a4-family-bases
