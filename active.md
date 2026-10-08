# Active Tasks

## search-ext-a1-declare-gate
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1674
- issued: 2026-10-08
- prompt: active/search_extensibility_a1_declare_gate_registry.md
- epic: search-extensibility (phase A1)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-shipped + workspace-shipped, awaiting-merge — 4 PRs opened 2026-10-08 under --auto (decide-and-flag, `decision-taken` on #1675); merge PyAutoFit#1675 first, the three docs PRs after RTD latest rebuilds
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1675
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/778
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/653
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/116
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1675
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/778
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/653
- validation: 3409 passed / 2 skipped / 9 xfailed; nojax 1192 passed; Sphinx 30 warnings = baseline in full and emulated-minimal envs; downstream suites green; afT BlackJAXNUTS/MultiStartAdam accuracy asserts fail identically on main
- decision-taken: factor-graph backend rules (use_jax=None derives from factors; agreement check after the test-mode bypass; gradient_mode disagreement → reverse); judgement values for status/warm_start/resumable/batched listed in the PR
- autonomy: --auto launch 2026-10-08 ("do A1 and B2 auto"); effective supervised (feature@large); ship checkpoint = decide-and-flag; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a1-declare-gate
- repos:
  - PyAutoFit: feature/search-ext-a1-declare-gate
  - PyAutoLens: feature/search-ext-a1-declare-gate
  - PyAutoGalaxy: feature/search-ext-a1-declare-gate
  - PyAutoCTI: feature/search-ext-a1-declare-gate
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## search-ext-b2-harness
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/2
- issued: 2026-10-08
- prompt: active/search_extensibility_b2_harness_protocol.md
- epic: search-extensibility (phase B2)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: workspace-dev
- autonomy: --auto launch 2026-10-08; effective supervised (feature@large); ship checkpoint = decide-and-flag; Consequence judge → human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b2-harness
- repos:
  - autofit_inference: feature/search-ext-b2-harness
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## linear-solver-p5-mapper-corpus
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/399
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p5-mapper-corpus
- repos:
  - autolens_profiling: feature/linear-solver-p5-mapper-corpus

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

## brain-dashboard-scope
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/507
- issued: 2026-10-08
- prompt: active/brain_dashboard_scope.md
- session: Codex CLI, session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/brain-dashboard-scope
- repos:
  - PyAutoBrain: feature/brain-dashboard-scope
- coordination: user approved separate work alongside #504; no shared theme or board_update edits
- tier: judge (human /prm)

## eyes-focused-figure-browser
- issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/25
- issued: 2026-10-08
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/eyes-focused-figure-browser
- repos:
  - PyAutoEyes: feature/eyes-focused-figure-browser
