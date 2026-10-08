# Active Tasks

## linear-solver-p3b-gpu-timing
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/395
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p3b-gpu-timing
- repos:
  - autolens_profiling: feature/linear-solver-p3b-gpu-timing

## search-ext-a0c-fit-repair
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1668
- issued: 2026-10-08
- prompt: active/search_extensibility_a0c_fit_repair.md
- epic: search-extensibility (phase A0c part 1)
- session: Claude CLI (Fable 5.1, /start_dev); session ID unavailable
- status: library-shipped + workspace-shipped, awaiting-merge — 9 PRs opened 2026-10-08 (two Opus workers + one ship worker); merge order: PyAutoFit#1669 first (library-first gate), then the workspace/organ PRs in any order, autofit_workspace_test#107 before #108
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a0c-fit-repair
- repos:
  - PyAutoFit: feature/search-ext-a0c-fit-repair
  - autofit_workspace: feature/search-ext-a0c-fit-repair
  - autofit_workspace_test: feature/search-ext-a0c-fit-repair (+ feature/search-ext-a0c-fit-repair-scripts for the separate scripts PR)
  - autofit_workspace_developer: feature/search-ext-a0c-fit-repair
  - autofit_assistant: feature/search-ext-a0c-fit-repair
  - PyAutoBrain: feature/search-ext-a0c-fit-repair (+ feature/search-ext-a0c-pipeline-docs for the sampler_pipeline docs PR)
- tier: judge (human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1669
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1669
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/168
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/107
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/108
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/29
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/55
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/502
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/503
- validation: PyAutoFit 3066 passed / 2 skipped / 5 xfailed (docs-only PR); autofit_workspace smoke 4/4 under PYAUTO_TEST_MODE=1; workspace_test new scripts 5/5 in and out of test mode; autofit_assistant 59 passed / 1 failed + citation check failed — BOTH pre-existing on origin/main (test_repo_readme_prompts_match_cards; missing wiki/literature/bibliography/literature.bib), untouched by this branch; Brain samplers 10 passed, full suite 1273 passed / 1 worktree-only failure that passes on canonical main
- follow-ups: Drawer crashes under NullPaths (draft/bug/autofit/drawer_crashes_under_nullpaths_timer_none.md); NSS docstring block-quote Sphinx warning now rendered (A0b); part 2 downstream ghost sweep to file after part 1 merges
- plan: approved by the human 2026-10-08 (A0c part 1 prompt + issue plan); rulings: RTD generic example stays DynestyStatic; `autofit_workspace_developer/searches/nss/` deleted via Gut (condemned.md entry `autofit_workspace_developer/searches-nss`, committed deletion at 7cb97c6); one PR per repo for prose plus separate PRs for workspace_test scripts, Brain samplers gap rule, Brain sampler_pipeline docs
- heart-ack: release validation incomplete: no rehearsal for current source — same reason set the human acknowledged 2026-10-07 for B1; carried under the human's 2026-10-08 "do all that" ship authorization

## shapelets-smoke-slow-park
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/586
- issued: 2026-10-08
- session: Claude CLI (Opus 5.5 worker, --auto); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/shapelets-smoke-slow-park
- repos:
  - autolens_workspace: feature/shapelets-smoke-slow-park
- tier: glance (auto-merge on green if Witness passes)
- plan: --auto launch by the human 2026-10-08 (review_release 2026.10.7.1 follow-up); plan on the issue

## sandbox-citation-agents-md
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/154
- issued: 2026-10-08
- session: Claude CLI (Opus 5.5 worker, --auto); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sandbox-citation-agents-md
- repos:
  - autolens_assistant: feature/sandbox-citation-agents-md
- tier: notify (auto-merge on green)
- plan: --auto launch by the human 2026-10-08 (review_release 2026.10.7.1 follow-up); plan on the issue
