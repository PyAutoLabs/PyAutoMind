
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

## gnfw-mcr-ludlow-normalisation
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/723
- issued: 2026-11-18
- session: shift worker 2026-11-18-pm (1913ad55)
- status: library-shipped, awaiting-merge
- prompt: active/gnfwmcrludlow_normalises_kappa_s_with_the_nfw.md
- worktree: ~/Code/PyAutoLabs-wt/gnfw-mcr-ludlow-normalisation
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot (effective level: supervised)
- decision-taken: Ludlow c kept as r200/r_s (not r200/r_-2), which r_s -> inf at inner_slope 2 rules out; human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/724
- repos:
  - PyAutoGalaxy: feature/gnfw-mcr-ludlow-normalisation
