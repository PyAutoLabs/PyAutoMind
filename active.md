
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

## nfwtruncatedmcr-truncation-radius
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/732
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm (2bf4469f-e7e4-4011-9109-b942513ad05c)
- status: pr-open (decision-taken)
- worktree: /home/jammy/Code/PyAutoLabs-wt/nfwtruncatedmcr-truncation-radius
- repos:
  - PyAutoGalaxy: feature/nfwtruncatedmcr-truncation-radius
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/733
- prompt: active/nfwtruncatedmcr_truncation_radius_uses_kpc_as_ar.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - acknowledged by the human 2026-11-19 ("YELLOW acknowledged, go"): YELLOW score 100 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

## lossampler_hmf_import_fails_and_los_halos
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/867
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm (16bf1edd-888e-48da-9906-1a04abd3106f)
- status: ready-to-ship
- worktree: ~/Code/PyAutoLabs-wt/lossampler_hmf_import_fails_and_los_halos
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/868
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/681
- decision-taken: autolens_workspace#681 (simulator_jax batch loop fits colossus coefficients once and passes them; plan said pass none)
- follow-ups: autolens_workspace_developer/los/simulator.py has the same silent placeholder fallback; Heart colab_gate.yaml hmf entry is stale
- repos:
  - PyAutoLens: feature/los-sampler-colossus-mass-function
  - autolens_workspace: feature/los-sampler-colossus-mass-function
- prompt: active/lossampler_hmf_import_fails_and_los_halos.md
- tier: effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - acknowledged by the human 2026-11-19 ("YELLOW acknowledged, go"): manifest drift: end-at-deliverable blocks (generated); manifest drift: generated hooks (session-start + end-at-deliverable)

## nfwtruncatedsph-total-mass
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/734
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm (76a27cc3-6466-4707-8409-d4dc7e50e87a)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/nfwtruncatedsph-total-mass
- repos:
  - PyAutoGalaxy: feature/nfwtruncatedsph-total-mass
- prompt: active/nfwtruncatedsph_total_mass_method_omits_the_nfw.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - acknowledged by the human 2026-11-19 ("YELLOW acknowledged, go"): YELLOW score 100 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml
