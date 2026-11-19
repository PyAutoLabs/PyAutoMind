
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

## colab_gate_colossus_rationale_is_stale_once
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/356
- session: shift worker 2026-11-19-pm2 (4cccb01f-266e-40f6-bb37-5f0daf61a17c)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/colab-gate-colossus-rationale
- repos:
  - PyAutoHeart: feature/colab-gate-colossus-rationale
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/357

## substructure-padded-slot-grad
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/871
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm2 (40917658-06b8-4211-bdfc-15f1c8b24590)
- status: pr-open
- worktree: /home/jammy/Code/PyAutoLabs-wt/substructure-padded-slot-grad
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/738
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/872
- follow-ups: review nits (exact padding-row assert in the lens test; clearer error when vmapped_padding_params length mismatches n_radial)
- repos:
  - PyAutoGalaxy: feature/substructure-padded-slot-grad
  - PyAutoLens: feature/substructure-padded-slot-grad
- prompt: active/substructure_jax_grad_is_nan_when_a.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - acknowledged by the human 2026-11-19 ("Acknowledge, use these"): YELLOW score 100 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

## hpc-sync-submit-pass-through
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/71
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/72
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm2 (98526c76-b5d3-4133-a2cd-c6809ed6edbb)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/hpc-sync-submit-pass-through
- repos:
  - autolens_inference: feature/hpc-sync-submit-pass-through
- prompt: active/hpc_sync_submit_pass_time_requeue_env.md
- tier: judge — effective level: supervised; merge mode: human /prm
- heart-ack:
  - acknowledged by the human 2026-11-19 ("Acknowledge, use these"): YELLOW score 100 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

## queued-epics-drive-shifts
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/696
- issued: 2026-11-19
- session: claude-code desktop (WSL), Opus 5.5, ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/queued-epics-drive-shifts
- repos:
  - PyAutoBrain: feature/queued-epics-drive-shifts
  - PyAutoMind: feature/queued-epics-drive-shifts
- prompt: active/queued_epics_drive_shifts_and_ral_by_default.md
- epic: autonomous-orchestrators
- tier: judge — merge mode: human /prm
- note: PyAutoBrain is the running shift's watcher — merge only after 2026-11-19-pm2 stops (22:15Z + 45 min)

## lossampler-cosmology-mismatch
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/873
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm2 (2040fb28)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/lossampler-cosmology-mismatch
- repos:
  - PyAutoLens: feature/lossampler-cosmology-mismatch
- prompt: active/lossampler_silently_ignores_a_non_planck_cosmolo.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot

## nfwtruncatedsph_convergence_loses_precision_near_scale_radius
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/739
- issued: 2026-11-19
- session: shift worker 2026-11-19-pm2 (f77a9ef7)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/nfwtruncatedsph-near-scale-radius
- repos:
  - PyAutoGalaxy: feature/nfwtruncatedsph-near-scale-radius
- heart-ack:
  - acknowledged by the human 2026-11-19 ("Acknowledge, use these"): YELLOW score 100 — manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml
