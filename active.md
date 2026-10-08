# Active Tasks

## search-ext-a0c-downstream
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/776
- issued: 2026-10-08
- prompt: active/search_extensibility_a0c_downstream_sweep.md
- epic: search-extensibility (phase A0c part 2)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-shipped + workspace-shipped, awaiting-merge — 9 PRs opened 2026-10-08 under --auto; glance tier → in-turn auto-merge on green with the Witness held
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/777
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/652
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/115
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/777
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/652
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/97
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/86
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/257
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/37
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/157
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/34
- autonomy: --auto launch 2026-10-08 ("do all A0 tasks in --auto"); effective safe (docs@medium); Consequence glance, Witness = pyswarms/multinest grep empty + no dead autosummary target
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a0c-downstream
- repos:
  - PyAutoLens: feature/search-ext-a0c-downstream
  - PyAutoGalaxy: feature/search-ext-a0c-downstream
  - PyAutoCTI: feature/search-ext-a0c-downstream
  - HowToLens: feature/search-ext-a0c-downstream
  - HowToGalaxy: feature/search-ext-a0c-downstream
  - autogalaxy_workspace: feature/search-ext-a0c-downstream
  - autocti_workspace: feature/search-ext-a0c-downstream
  - autolens_assistant: feature/search-ext-a0c-downstream
  - autogalaxy_assistant: feature/search-ext-a0c-downstream
- tier: glance (auto-merge on green if the Witness passes, in-turn)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source); STALE passes gate leg 4, no YELLOW reason acknowledged

## search-ext-a0b-hygiene
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1670
- issued: 2026-10-08
- prompt: active/search_extensibility_a0b_hygiene.md
- epic: search-extensibility (phase A0b)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-dev
- autonomy: --auto launch 2026-10-08; effective safe (refactor); Consequence judge → ends at PR-open, human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a0b-hygiene
- repos:
  - PyAutoFit: feature/search-ext-a0b-hygiene (+ feature/search-ext-a0a2-backend-conformance stacked on it for the A0a(ii) PR)
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## linear-solver-p4a-jacobi-a100-divergence
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/397
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p4a-jacobi-a100-divergence
- repos:
  - autolens_profiling: feature/linear-solver-p4a-jacobi-a100-divergence
