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

## search-ext-a5-library
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1688
- issued: 2026-10-14
- prompt: active/search_ext_a5_library_run_ctx_migrations.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a5-library
- epic: search-extensibility
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1689
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1690
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1691
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1692
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1689
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1690
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1691
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1692
- next: human /prm in stack order 1689 → 1690 → 1691 → 1692 (stacked; GitHub retargets each base to main as the one below merges); all four full-suite green serially, byte-identical identifiers + seeded samples vs main df6d218f1; after merge+release: A5 consumers task (draft/refactor/autofit/search_ext_a5_consumers.md), BFGS resume follow-up (pre-existing KeyError on interrupted run), pre-existing workspace searches/ script failures (NUTS divergences, MultiStart n_resurrections, NSS log_evidence_error) are separate drafts
- repos:
  - PyAutoFit: feature/search-ext-a5-library, feature/search-ext-a5-nest-blackjax, feature/search-ext-a5-multistart, feature/search-ext-a5-framework

## search-ext-b4b-ep-baseline
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/4
- issued: 2026-10-14
- prompt: active/search_ext_b4b_ep_graphical_baseline_port.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b4b-ep-baseline
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/5
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/61
- next: human /prm autofit_profiling#5 (decision-taken: host pin = B4a laptop; witness "within 2x" NOT met — all six cells 0.14–0.48x faster, correctness exact, N30 sanity FAILs reproduced; sigma_q95 checked vs 12.15 not 12.18) then PyAutoPulse#61 after Pages is live (receipt/snapshot refresh on its branch first, as B4a). Ship gate: tests 16/16 + ruff + catalogue check; Pulse 207 + check --offline OK; review FINDINGS×2 fixed; Heart STALE acked ("no rehearsal for current source"). Follow-up: retire developer ep/ + graphical/ via Gut after merge
- repos:
  - autofit_profiling: feature/search-ext-b4b-ep-baseline
  - PyAutoPulse: feature/search-ext-b4b-ep-baseline

## search-ext-b5a-wave2
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/8
- issued: 2026-10-14
- prompt: active/search_ext_b5a_freeze_and_scored_wave2.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5a-wave2
- epic: search-extensibility
- next: Opus worker freezes @2, builds the scored-wave infra (PR 1), submits references + wave 2 on RAL `--partition=ral` against a private pinned PyAutoFit, then Cortex (PR 2) and Insight (PR 3); human /prm; row stays open as compute-running until B5b
- repos:
  - autofit_inference: feature/search-ext-b5a-wave2
  - PyAutoInsight: feature/search-ext-b5a-wave2
  - PyAutoCortex: feature/search-ext-b5a-wave2
