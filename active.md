# Active Tasks

## ral-category-paths
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
- issued: 2026-10-15
- prompt: active/science_ral_folder_restructure.md
- session: Claude Code CLI (Opus 5.5); session 4b6b15e2
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/22
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/6
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/504
- worktree: ~/Code/PyAutoLabs-wt/ral-category-paths
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 4b6b15e2 ("can we sort out the 8 remaining links" after being asked for the override; plan approved with "go")
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoArray/Tests: red"; "[red] autofit/autogalaxy/autolens_workspace_test Smoke Tests: red"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] Worktree drift"
  - permitted: commit, push, PR-open; merge separate
- next: /prm the three PRs; then human `git pull` on RAL inference/autolens_inference + profiling/autofit_profiling and removes those two links. euclid DONE (untracked scripts edited, pushed to RAL active/euclid, 0 old-path hits; link removable now). PyAutoPulse needed no change (all hits are verbatim historical tasks/). Phase 2 parked in planned.md (ral-category-paths-phase2)
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
- status: pr-open (supervised --auto; Heart RED dev override); awaiting human /prm library-first: PyAutoFit#1695 → autofit_workspace#170 → autofit_workspace_test#112; worker extending the same PRs to the missed copies (cookbooks/search.py, searches/DynestyDynamic.py) before hand-back
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1695
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/170
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/112
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1695
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

## memory-domain-routing
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/524
- issued: 2026-10-15
- prompt: active/memory_domain_routing.md
- status: library-dev
- session: Codex
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/memory-domain-routing
- approval: Accepted ownership plan; live human "Proceed" after exact Heart RED reasons. Development and PR-open only; merge separate.
- heart-red-override:
  - authorized-by: live human "Proceed", 2026-10-15
  - permitted: development, commit, push, PR-open; no merge/release
  - validation: pending implementation
  - reasons:
    - [red] release validation FAILED (stage integrate)
    - [red] PyAutoHands/workflows/Python Version Matrix: failure
    - [red] PyAutoHeart/workflows/Release Integrate: failure
    - [red] PyAutoMind/workflows/Lifecycle Drift: failure
    - [red] PyAutoArray/Tests: red
    - [red] PyAutoArray/Tests: red
    - [red] autofit_workspace_test/Smoke Tests: red
    - [red] autogalaxy_workspace_test/Smoke Tests: red
    - [red] autolens_workspace_test/Smoke Tests: red
    - [red] CI wall-clock: 26 gates · slowest PyAutoBrain Nightly Release 63m · 5 hang events
    - [red] Release readiness: release validation FAILED (stage integrate)
    - [red] autofit_test: red
    - [red] Release validation: NOT release_ready — v2026.10.15.1.dev81701 profile=release (2026-10-15T07:04:34+00:00)
    - [red] validation_report/stages/integrate: fail
    - [red] PyAutoArray: red
    - [red] autolens_inference: red
    - [red] autolens_profiling: red
    - [red] Worktree drift: 5 orphan / 0 missing / 4 dirty
    - [red] euclid_strong_lens_modeling_pipeline: red
- repos:
  - PyAutoBrain: feature/memory-domain-routing
  - PyAutoMemory: feature/memory-domain-routing
