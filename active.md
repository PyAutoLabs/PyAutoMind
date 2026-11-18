
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

## compound-prior-model-json
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1782
- issued: 2026-11-18
- session: shift worker 2026-11-18-pm (1100d086)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1783
- heart-ack:
  - manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml
  - release validation incomplete: no rehearsal for current source
- prompt: active/a_model_with_compound_priors_cannot_be.md
- worktree: ~/Code/PyAutoLabs-wt/compound-prior-model-json
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot (effective level: supervised)
- repos:
  - PyAutoFit: feature/compound-prior-model-json

## gnfw-mcr-ludlow-normalisation
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/723
- issued: 2026-11-18
- session: shift worker 2026-11-18-pm (1913ad55)
- status: library-dev
- prompt: active/gnfwmcrludlow_normalises_kappa_s_with_the_nfw.md
- worktree: ~/Code/PyAutoLabs-wt/gnfw-mcr-ludlow-normalisation
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot (effective level: supervised)
- repos:
  - PyAutoGalaxy: feature/gnfw-mcr-ludlow-normalisation
