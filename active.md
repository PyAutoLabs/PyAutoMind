
## adaptsplit-logdet-backend-parity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/627
- issued: 2026-10-15
- prompt: active/adaptsplit_regularization_log_det_differs_betwee.md
- session: Claude Code CLI (Fable 5.1); session 3e3dea38; launched --auto
- status: library-dev
- decision: human chose (b) 'Delaunay only (Recommended by review)' on 2026-10-15 (https://github.com/PyAutoLabs/PyAutoArray/issues/627#issuecomment-6200058449); un-parked
- worktree: ~/Code/PyAutoLabs-wt/adaptsplit-logdet-backend-parity
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 3e3dea38, AskUserQuestion answer 'Yes, override for development (Recommended)' (evening launch, three PyAutoArray Aris prompts)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red" (as listed on PyAutoArray#626)
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoArray: feature/adaptsplit-logdet-backend-parity

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

## search-ext-a5-capmatrix-cards
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1694
- issued: 2026-10-15
- prompt: active/capability_matrix_links_b3_catalogue_cards.md
- status: pr-open (glance tier; Heart RED override forbids auto-merge — awaiting human /prm) — PyAutoFit#1696 green (Docs 2/2, Tests 3/3); Catalogue column links every manifest search to its card at pinned autofit_inference bea1d8746
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1696
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1696
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto (second Heart RED override grant, recorded on #1694 and autonomy_log)
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a5-capmatrix-cards
- repos:
  - PyAutoFit: feature/search-ext-a5-capmatrix-cards
- classification: library (PyAutoFit docs generator), Consequence glance, Autonomy safe
- suggested-branch: feature/search-ext-a5-capmatrix-cards

## cortex-project-readability
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/521
- issued: 2026-10-14
- prompt: active/cortex_projects_readability.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto 2026-10-15
- status: pr-open (awaiting human /prm; tier undeclared) — Brain renderer + tests only; PyAutoCortex pages self-heal from Brain main via Cortex Dashboard Refresh (nightly 03:35 UTC or next Cortex push) — no Cortex PR; CI green at a7a02e88
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/526
- worktree: ~/Code/PyAutoLabs-wt/cortex-project-readability
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Both, override for development (Recommended)' (third grant, night launch)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- approval: User approved both phases in session: "I approve"; tier undeclared → human /prm
- repos:
  - PyAutoBrain: feature/cortex-project-readability
