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
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a0c-fit-repair
- repos:
  - PyAutoFit: feature/search-ext-a0c-fit-repair
  - autofit_workspace: feature/search-ext-a0c-fit-repair
  - autofit_workspace_test: feature/search-ext-a0c-fit-repair (+ feature/search-ext-a0c-fit-repair-scripts for the separate scripts PR)
  - autofit_workspace_developer: feature/search-ext-a0c-fit-repair
  - autofit_assistant: feature/search-ext-a0c-fit-repair
  - PyAutoBrain: feature/search-ext-a0c-fit-repair
- tier: judge (human /prm)
- plan: approved by the human 2026-10-08 (A0c part 1 prompt + issue plan); rulings: RTD generic example stays DynestyStatic; `autofit_workspace_developer/searches/nss/` deleted via Gut (condemned.md entry `autofit_workspace_developer/searches-nss`, committed deletion at 7cb97c6); one PR per repo for prose plus separate PRs for workspace_test scripts, Brain samplers gap rule, Brain sampler_pipeline docs
- heart-ack: release validation incomplete: no rehearsal for current source — same reason set the human acknowledged 2026-10-07 for B1; carried under the human's 2026-10-08 "do all that" ship authorization
