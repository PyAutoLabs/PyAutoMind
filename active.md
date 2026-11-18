
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

## model-pytree-fixed-attributes
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1780
- issued: 2026-11-18
- session: claude-code (WSL), Opus 5.5 worker; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/model-pytree-fixed-attributes
- repos:
  - PyAutoFit: feature/model-pytree-fixed-attributes
- prompt: active/model_pytree_fixed_attributes_roundtrip.md
- approval: human approved 2026-11-18 ("Do the small follow up after prm"); follow-up to PyAutoFit#1777/#1779
- tier: glance — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1781
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1781
- next: human /prm (glance tier; worker stopped at PR-open by instruction)
