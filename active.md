# Active Tasks

## ral-category-paths
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
- issued: 2026-10-15
- prompt: active/science_ral_folder_restructure.md
- session: Claude Code CLI (Opus 5.5); session 4b6b15e2
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ral-category-paths
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 4b6b15e2 ("can we sort out the 8 remaining links" after being asked for the override; plan approved with "go")
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoArray/Tests: red"; "[red] autofit/autogalaxy/autolens_workspace_test Smoke Tests: red"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] Worktree drift"
  - permitted: commit, push, PR-open; merge separate
- next: phase 1 PRs (autolens_inference, autofit_profiling, PyAutoMind policy/hpc_ral.md, PyAutoPulse) + euclid project scripts; phase 2 parked in planned.md (ral-category-paths-phase2)
- repos:
  - autolens_inference: feature/ral-category-paths
  - autofit_profiling: feature/ral-category-paths
  - PyAutoPulse: feature/ral-category-paths
  - PyAutoMind: feature/ral-category-paths

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

## search-ext-b5b2-remainder
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/12
- issued: 2026-10-15
- prompt: active/search_ext_b5b2_remainder_and_summary_records.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto
- status: workspace-dev
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5b2-remainder
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Yes, override for development (Recommended)' (second grant, evening launch)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - autofit_inference: feature/search-ext-b5b2-remainder
  - PyAutoInsight: feature/search-ext-b5b2-remainder
  - PyAutoCortex: feature/search-ext-b5b2-remainder
- compute: RAL 409930_[0-19]%20 --partition=ral — wave-2 probe-first remainder (980 runs); 10/20 tasks COMPLETED, 10 RUNNING at 1h19 on 2026-10-15 evening; pulled and judged by this task

## search-ext-kwarg-typos
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1693
- issued: 2026-10-15
- prompt: active/search_kwarg_typos_in_workspace_scripts.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto
- status: library-dev
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-kwarg-typos
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Yes, override for development (Recommended)' (second grant, evening launch)
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready"; "[red] Worktree drift"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoFit: feature/search-ext-kwarg-typos
  - autofit_workspace: feature/search-ext-kwarg-typos
  - autofit_workspace_test: feature/search-ext-kwarg-typos
