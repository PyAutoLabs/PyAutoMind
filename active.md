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

## search-ext-b5b-score
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/10
- issued: 2026-10-15
- prompt: active/search_ext_b5b_pull_judge_publish_wave2.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto
- status: workspace-dev
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5b-score
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Yes, override for development (Recommended)'
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready — v2026.10.15.1.dev81701 profile=release (2026-10-15T07:04:34+00:00)"; "[red] Worktree drift: 5 orphan / 0 missing / 4 dirty"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - autofit_inference: feature/search-ext-b5b-score
  - PyAutoInsight: feature/search-ext-b5b-score
  - PyAutoCortex: feature/search-ext-b5b-score

## search-ext-a5-consumers
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/310
- issued: 2026-10-15
- prompt: active/search_ext_a5_consumers.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto
- status: workspace-dev
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a5-consumers
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Yes, override for development (Recommended)'
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready — v2026.10.15.1.dev81701 profile=release (2026-10-15T07:04:34+00:00)"; "[red] Worktree drift: 5 orphan / 0 missing / 4 dirty"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoHands: feature/search-ext-a5-consumers
  - PyAutoBrain: feature/search-ext-a5-consumers
  - PyAutoMemory: feature/search-ext-a5-consumers
  - autofit_assistant: feature/search-ext-a5-consumers
  - autolens_assistant: feature/search-ext-a5-consumers
  - autogalaxy_assistant: feature/search-ext-a5-consumers
  - autofit_workspace: feature/search-ext-a5-consumers
  - autolens_workspace: feature/search-ext-a5-consumers
  - autogalaxy_workspace: feature/search-ext-a5-consumers

## search-ext-b4b-dev-retire
- issue: https://github.com/PyAutoLabs/autofit_workspace_developer/issues/34
- issued: 2026-10-15
- prompt: active/retire_ep_graphical_after_b4b.md
- session: Claude Code CLI (Fable 5.1); session 6ffb59e9; launched --auto
- status: workspace-shipped, awaiting-merge (glance: tiered merge pending — repo has no CI checks)
- epic: search-extensibility
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b4b-dev-retire
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 6ffb59e9, AskUserQuestion answer 'Yes, override for development (Recommended)'
  - reasons: "Heart: RED — Release RED; monitoring RED · 10/100 · 415 unresolved"; "[red] release validation FAILED (stage integrate)"; "[red] PyAutoHands/workflows/Python Version Matrix: failure"; "[red] PyAutoHeart/workflows/Release Integrate: failure"; "[red] PyAutoMind/workflows/Lifecycle Drift: failure"; "[red] PyAutoArray/Tests: red"; "[red] autofit_workspace_test/Smoke Tests: red"; "[red] autogalaxy_workspace_test/Smoke Tests: red"; "[red] autolens_workspace_test/Smoke Tests: red"; "[red] Release validation: NOT release_ready — v2026.10.15.1.dev81701 profile=release (2026-10-15T07:04:34+00:00)"; "[red] Worktree drift: 5 orphan / 0 missing / 4 dirty"; "[red] autolens_inference: red"; "[red] autolens_profiling: red"; "[red] euclid_strong_lens_modeling_pipeline: red"
  - permitted: commit, push, PR-open; merge separate
- repos:
  - autofit_workspace_developer: feature/search-ext-b4b-dev-retire
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/35
- next: tiered merge (glance) once the human rules on the no-CI-checks case; then /prm close-out; follow-up: delete dead `aggregate_profiles.py` (out of #34 scope)
