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
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1685 (MERGED 2026-10-14 8e5487ae9)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1686
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1687
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1685
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1686
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1687
- next: human /prm in order #1685 → #1686 → #1687 (stacked; #1687 carries Closes #1684). Human RULED 2026-10-14: MultiStart explicit-seed re-key ACCEPTED (no override). Codex gpt-6-astra review DONE: FINDINGS 4 (`search_extensibility_epic_reviews/07_codex_astra_a4_stack_premerge.md`): old default NUTS/SMC JSON re-keys via aggregator recompute (P1, #1686), Dynesty rstate double-kwarg breaks SeededDynestyStatic (P2, #1686), grid child streams bypass raw-seed backends + MultiStart (P2, #1686), Drawer/SMC positional slot shift (P2, #1687); ALL FOUR ENACTED on the branches (#1686 head 175d91a58, #1687 rebased 09834b9c0; +47 tests, identifier dump unchanged); CI re-running at hand-back. Decisions for the human in the worker report: grid children of default-seeded searches now get child backend seeds (no longer replay identical randomness); `SearchOutput.id` prefers the saved `.identifier` for every output; SMC conformance signature gains `legacy_positional`. Companion (recommended, not required): autofit_workspace_test graphical SeededDynestyStatic → `af.DynestyStatic(seed=)` (text in #1686 body). /prm 2026-10-14: #1685 MERGED (8e5487ae9); #1686 STOPPED on red CI — unittest (3.13) `test_autofit/interpolator/test_covariance.py::test_single_variable` (27.5 vs 25±2): the module's `seed_search_randomness` fixture seeds stdlib `random` for the old initializer, but #1686's Initializer now draws from `np.random.default_rng()` so the fixture no longer controls it (documented 3.6 % miss rate returns). Test-fixture gap introduced by #1686, not a flake; FIXED test-only (fixture now seeds the initializer via `seed.seed_sequence`; 20/20 deterministic; #1686 head 114adeebd, #1687 rebased 4b86167b4, full suite 3776/1/0 on #1687); CI re-running; human re-runs /prm #1686 → #1687 when green. Companion changes (Brain sampler_pipeline/reference.md ~129-136, developer-tier ultranest + pyswarms searches) listed in #1687 body — file as separate tasks after merge
- repos:
  - PyAutoFit: feature/search-ext-a4-decompose
  - PyAutoFit: feature/search-ext-a4-seed
  - PyAutoFit: feature/search-ext-a4-family-bases
