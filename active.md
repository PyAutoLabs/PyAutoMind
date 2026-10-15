# Active Tasks

## delaunay-nn-numba
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/623
- issued: 2026-10-15
- prompt: active/make_delaunaynn_fast_on_the_numba_numpy.md
- session: Claude Code CLI (Opus 5.5); session 0b91c774
- status: library-shipped, awaiting-merge (phase 1); phase 2 not started
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/624
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-numba
- phase: 1 of 2 (numba Sibson kernel) shipped as PR #624; phase 2 = routing audit (Aris measurement already shows all meshes on InversionInterferometerSparseNumba; remaining: NaN-weight guard, DelaunayNN routing tests, imaging audit + timing)
- next: human /prm on PyAutoArray#624 (CI green); phase 2 in progress stacked on it (branch feature/delaunay-nn-numba-routing)
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 0b91c774 ("I override, tests will be handled once the epic refactor elsewhere is sorted")
  - reasons: see issue #623 (verbatim reason strings recorded there)
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoArray: feature/delaunay-nn-numba, feature/delaunay-nn-numba-routing

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
- status: workspace-shipped, awaiting-merge
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
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/311
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/523
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/169
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/56
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/159
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/35
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/590
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/258
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/132
- next: human /prm in order PyAutoHands#311 first (the `search_roster` reusable job goes live at @main after it), then Brain#523 (tenant-firewall leg needs Mind main allowlist entry for autofit_inference in samplers/_samplers.py + samplers.sh — pushed 2026-10-15, re-run the leg), then the 7 consumers; blocks stamped from released autofit 2026.10.12.1 (source checkout reports stale 2026.8.17.1); witness 6/7 — the capability-matrix→B3-card link lives in PyAutoFit docs/_generate_searches.py (follow-up draft); stale al names outside ruled files flagged only (al wiki/core/stack/autofit.md, stack/autolens.md, concepts/non_linear_search.md, skills/al_update_wiki.md, literature); no third review round
