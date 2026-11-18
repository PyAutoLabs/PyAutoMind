
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

## model-identifier-0d-array
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1784
- session: shift worker 2026-11-18-pm2 (d856a027)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1785
- worktree: ~/Code/PyAutoLabs-wt/model-identifier-0d-array
- prompt: active/model_identifier_raises_typeerror_iteration_over.md
- repos:
  - PyAutoFit: feature/model-identifier-0d-array
- heart-ack:
  - YELLOW score 85 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source

## stellar_m_l_gradient_profiles_sersicgradient_piv
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/725
- issued: 2026-11-18
- session: shift worker 2026-11-18-pm2 (b53f7ee2-2b5d-47c1-9042-4f2098218a54)
- status: library-shipped, awaiting-merge (decision-taken; ends at PR-open for /prm)
- worktree: ~/Code/PyAutoLabs-wt/stellar-ml-gradient-conventions
- repos:
  - PyAutoGalaxy: feature/stellar-ml-gradient-conventions
  - autolens_workspace_test: feature/stellar-ml-gradient-conventions
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/726
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/368
- prompt: active/stellar_m_l_gradient_profiles_sersicgradient_piv.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - acknowledged by the human 2026-11-18 ("YELLOW acknowledged, go"; launched with "can we start?"): YELLOW score 85 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source

## mind-writer-own-claim-update
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/681
- issued: 2026-11-18
- session: Claude Code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/mind-writer-own-claim-update
- repos:
  - PyAutoBrain: feature/mind-writer-own-claim-update
- prompt: active/mind_writer_own_claim_update.md
- tier: judge — merge mode: human /prm
