
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

## group-slam-sigma-bound-guard
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/679
- issued: 2026-11-19
- session: claude-code desktop (WSL), Opus 5.5 session
- status: workspace-shipped, awaiting /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/680
- worktree: ~/Code/PyAutoLabs-wt/group-slam-sigma-bound-guard
- repos:
  - autolens_workspace: feature/group-slam-sigma-bound-guard
- prompt: active/group_slam_sigma_upper_zero_flake.md
- tier: judge — merge mode: human /prm
