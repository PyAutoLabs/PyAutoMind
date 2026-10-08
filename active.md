# Active Tasks

## inference-setup-producer
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/20
- issued: 2026-10-08
- prompt: active/inference_setup_producer.md
- epic: inference-setup-redesign
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-producer
- repos:
  - autolens_inference: feature/inference-setup-producer
- plan: human authorized all phases autonomously to the end, including in-turn merge on passed gates; no compute or scientific acceptance.

## inference-setup-browser
- issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/15
- issued: 2026-10-08
- prompt: active/inference_setup_browser.md
- epic: inference-setup-redesign
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-browser
- repos:
  - PyAutoInsight: feature/inference-setup-browser
- plan: human authorized all phases autonomously to the end, including in-turn merge on passed gates; no compute or scientific acceptance.

## inference-sampler-literature
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/124
- issued: 2026-10-08
- prompt: active/inference_sampler_literature.md
- epic: inference-setup-redesign
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inference-sampler-literature
- repos:
  - PyAutoMemory: feature/inference-sampler-literature
- plan: human authorized all phases autonomously to the end, including in-turn merge on passed gates; no compute or scientific acceptance.

## search-ext-a0c-downstream
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/776
- issued: 2026-10-08
- prompt: active/search_extensibility_a0c_downstream_sweep.md
- epic: search-extensibility (phase A0c part 2)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-dev
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

## inference-setup-advice
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/156
- issued: 2026-10-08
- prompt: active/inference_setup_advice.md
- epic: inference-setup-redesign
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-advice
- coordination: human explicitly approved "Coordinate the two tasks" with search-ext-a0c-downstream on 2026-10-08; preserve edits and reconcile shared discovery files before merge.
- repos:
  - autolens_assistant: feature/inference-setup-advice
- plan: human authorized all phases autonomously to the end, including in-turn merge on passed gates.

## linear-solver-p4a-jacobi-a100-divergence
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/397
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p4a-jacobi-a100-divergence
- repos:
  - autolens_profiling: feature/linear-solver-p4a-jacobi-a100-divergence
