
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## pyautolens-ii-case-studies
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautolens-ii-case-studies
- repos:
  - autolens_workspace_developer: feature/pyautolens-ii-case-studies
- prompt: active/pyautolens_ii_case_studies.md
- coordination: human approved PyAutoLens/paper_jax/paper.md-only edits alongside magnification-maps-wiring; no library code changes
- next: validate JWST PSF/noise and export calibrated ALMA visibilities, then joint gradient check and bounded pilots
- tier: judge — merge mode: human /prm

## shift-speed-worker-chat-loop
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/686
- issued: 2026-11-19
- session: claude-code desktop (WSL), Fable 5.2 architect + Opus 5.5 worker
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/shift-speed-worker-chat-loop
- repos:
  - PyAutoBrain: feature/shift-speed-worker-chat-loop
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/687
- prompt: active/shift_speed_worker_chat_loop.md
- epic: autonomous-orchestrators (M3.7a)
- tier: judge — merge mode: human /prm

## workspace-smoke-nightly
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/354
- issued: 2026-11-19
- session: claude-code desktop (WSL), Fable 5.2 architect + Opus 5.5 worker
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/workspace-smoke-nightly
- repos:
  - PyAutoHeart: feature/workspace-smoke-nightly
- prompt: active/workspace_smoke_nightly_and_pinned_shas.md
- epic: autonomous-orchestrators (M3.7d)
- tier: judge — merge mode: human /prm

## jax-0121-step0-structured
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/703
- issued: 2026-11-19
- session: claude-code desktop (WSL), Opus 5.5 (session + Opus worker)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-0121-step0-structured
- repos:
  - PyAutoArray: feature/jax-0121-step0-structured
- prompt: active/jax_0_12_1_step0_structured_containment_diverges.md
- blocks: pending library release (rehearsal fails on jax 0.12.1)
- tier: supervised — merge mode: human /prm
