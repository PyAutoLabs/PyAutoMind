# Active Tasks

## board-one-click-update
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/504
- issued: 2026-10-08
- prompt: active/board_one_click_update.md
- session: Codex CLI, session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-one-click-update
- repos:
  - PyAutoBrain: feature/board-one-click-update
- tier: judge (human /prm)
- approval: user approved shared authenticated Update service with "ok do it"
- next: awaiting hosting preference after explaining setup; local service prototype preserved, shared button integration and shipping incomplete

## timing-noise-audit-p1-inventory
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p1-inventory
- repos:
  - autolens_profiling: feature/timing-noise-audit-p1-inventory

## search-ext-a2-objective-bridge
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1676
- issued: 2026-10-08
- prompt: active/search_extensibility_a2_objective_bridge.md
- epic: search-extensibility (phase A2; A3 runs in parallel in this worktree's second checkout `PyAutoFit_a3` on `feature/search-ext-a3-samples-checkpointer`; A3b stacks on both)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-dev
- autonomy: --auto launch 2026-10-08 ("A2, A3, A3b and B3 in auto mode"); effective safe (refactor); Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a2-objective-bridge
- repos:
  - PyAutoFit: feature/search-ext-a2-objective-bridge (+ feature/search-ext-a3-samples-checkpointer in PyAutoFit_a3; + feature/search-ext-a3b-nss-preflight stacked later)
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## search-ext-b3-pilot
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/4
- issued: 2026-10-08
- prompt: active/search_extensibility_b3_wave1_pilot.md
- epic: search-extensibility (phase B3)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: workspace-dev
- autonomy: --auto launch 2026-10-08; effective supervised (feature@large); decide-and-flag at ship; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b3-pilot
- repos:
  - autofit_inference: feature/search-ext-b3-pilot
  - PyAutoInsight: feature/search-ext-b3-pilot
  - PyAutoCortex: feature/search-ext-b3-pilot
  - autofit_assistant: feature/search-ext-b3-pilot
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## broca-cockpit
- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/33
- issued: 2026-10-08
- session: Codex (session ID unavailable)
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/broca-cockpit
- repos:
  - pyautolabs.github.io: feature/broca-cockpit
- heart-ack: Existing user acknowledgement of manifest drift (workspace checkouts, 1 mismatch versus repos.yaml); recheck exact reasons before ship.
- library-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/34
- validation: 10 Node tests pass; browser navigation, overview and deep-link reload pass at 390px and 1440px.
- next: Await explicit no-PR-CI merge exception required by prm; then merge and verify Pages.
