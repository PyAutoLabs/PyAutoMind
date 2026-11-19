
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

## gnfw_mge_deflections_lose_accuracy_for_inner
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/729
- issued: 2026-11-19
- session: shift worker 2026-11-19-am (f6597b74-14a0-449d-bfd4-c034bd8699d5)
- status: library-shipped, awaiting-merge (shift 2026-11-19-am ended early by the human; PR opened from the cockpit chat after targeted smoke)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/730
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/730
- worktree: ~/Code/PyAutoLabs-wt/gnfw-mge-inner-mass
- heart-ack:
  - acknowledged by the human 2026-11-19 ("YELLOW acknowledged, go"): YELLOW score 85 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source
- repos:
  - PyAutoGalaxy: feature/gnfw-mge-inner-mass
