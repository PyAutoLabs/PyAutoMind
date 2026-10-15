# Active Tasks

## ral-category-paths-phase2
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
- issued: 2026-10-15
- prompt: active/ral_category_paths_phase2.md
- session: Claude Code CLI (Opus 5.5); session 4b6b15e2
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ral-category-paths-phase2
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 4b6b15e2 — the override granted for PyAutoCortex#67 (phase 1), carried to this remainder of the same issue on the human's "go"
  - reasons: unchanged from phase 1 (recorded on PyAutoCortex#67)
  - permitted: commit, push, PR-open; merge separate
- next: autofit_inference + PyAutoCortex + PyAutoMemory now; autolens_profiling (+_wt, _corpus) once autolens_profiling#418 (hst-mge-pilot-qualification) merges and releases it
- repos:
  - autofit_inference: feature/ral-category-paths-phase2
  - PyAutoCortex: feature/ral-category-paths-phase2
  - PyAutoMemory: feature/ral-category-paths-phase2

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

## interferometer-sparse-data-vector
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/626
- issued: 2026-10-15
- prompt: active/interferometer_sparse_inversion_compute_data_vec.md
- session: Claude Code CLI (Fable 5.1); session 3e3dea38; launched --auto
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-sparse-data-vector
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 3e3dea38, AskUserQuestion answer 'Yes, override for development (Recommended)' (evening launch, three PyAutoArray Aris prompts)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoArray: feature/interferometer-sparse-data-vector

## search-ext-a5-capmatrix-cards
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1694
- issued: 2026-10-15
- prompt: active/capability_matrix_links_b3_catalogue_cards.md
- status: library-dev
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto (second Heart RED override grant, recorded on #1694 and autonomy_log)
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a5-capmatrix-cards
- repos:
  - PyAutoFit: feature/search-ext-a5-capmatrix-cards
- classification: library (PyAutoFit docs generator), Consequence glance, Autonomy safe
- suggested-branch: feature/search-ext-a5-capmatrix-cards
