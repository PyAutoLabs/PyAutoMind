
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

## ep-projected-model-shared-prior
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1773
- issued: 2026-11-13
- session: Claude Code desktop (WSL)
- status: library-dev
- prompt: active/ep_projected_model_shared_prior_keyerror.md
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-projected-model-shared-prior
- tier: judge — merge mode: human /prm
- repos:
  - PyAutoFit: feature/ep-projected-model-shared-prior
- conflict-override: PyAutoFit also claimed by three-autos-public-framing (docs, human-review); human approved 2026-11-13 a separate worktree off main (non-overlapping files: samples.py + tests)
- unblocks: Science/development/ep_gnfw_slope N=3 EP smoke

## galaxy-duplicate-pytree-registration
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/693
- session: Claude Code background job (shift 2026-11-14-pm2 worker)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/galaxy-duplicate-pytree-registration
- prompt: active/galaxy_duplicate_pytree_registration_after_jax_fitness.md
- heart-ack:
  - organism verdict RED/YELLOW/STALE on local-checkout rows (dirty or behind canonical checkouts, manifest drift), release-scope (no rehearsal for current source) and human-only rows (open PRs) — none on the touched repos; each close-out reads the dev-ship gate (readiness --dev --repos)
- repos:
  - PyAutoArray: feature/galaxy-duplicate-pytree-registration

## cluster-regime-narrative
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/670
- issued: 2026-11-14
- session: claude-code shift worker (batch 2026-11-14-pm2, --auto, supervised)
- status: awaiting-merge (PR open, decision-taken; extended_source parked awaiting-input)
- worktree: ~/Code/PyAutoLabs-wt/cluster-regime-narrative
- repos:
  - autolens_workspace: feature/cluster-regime-narrative
- prompt: active/cluster_regime_narrative.md
- tier: notify — merge mode: auto-merge on green (supervised --auto: decision-taken PR ends at PR-open)
- heart-ack:
  - organism verdict RED/YELLOW/STALE on local-checkout rows (dirty or behind canonical checkouts, manifest drift), release-scope (no rehearsal for current source) and human-only rows (open PRs) — none on the touched repos; each close-out reads the dev-ship gate (readiness --dev --repos)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/671
- next: human /prm on #671; answer the extended_source questions on #670, then resume phase 2 (feature + workspace_test script)

## dataset-model-free-grid-offset-pytree-roundtrip
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1777
- issued: 2026-11-16
- session: shift worker 2026-11-16-pm (b778571d)
- status: awaiting-input
- prompt: active/dataset_model_free_grid_offset_pytree_roundtrip.md
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1777#issuecomment-6925508074
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- suggested-branch: feature/model-pytree-tuple-prior
- blocked-by: ep-projected-model-shared-prior (using PyAutoFit) — override asked on the issue
- heart-ack:
  - acknowledged by the human 2026-11-16 ("Heart ack so its ok"): RED on local-checkout rows (7 library checkouts behind/dirty), 5 manifest-drift legs, release-scope (no rehearsal for current source) and human-only (PyAutoArray PR open 13d); none on the touched repos

## ellipse-multipole-latent-missing-m
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/719
- issued: 2026-11-16
- session: shift worker 2026-11-16-pm (af778bf0-0b22-4196-ad6e-ff5182aa5f0f)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/720
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/720
- heart-ack:
  - acknowledged by the human 2026-11-16 ("Heart ack so its ok"): RED on local-checkout rows (7 library checkouts behind/dirty: PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens x2, PyAutoCTI), 5 manifest-drift legs, release-scope (no rehearsal for current source) and human-only (PyAutoArray PR open 13d); none on the touched repos
- worktree: ~/Code/PyAutoLabs-wt/ellipse-multipole-latent-missing-m
- repos:
  - PyAutoGalaxy: feature/ellipse-multipole-latent-missing-m
- summary: |
    PR #720 open (glance, PR-open; close-out session runs witness + adversary and merges or refuses).
    Adds `m: Constant 4` prior config to EllipseMultipole/EllipseMultipoleScaled so latent_parameters_from works without an explicit m; regression test (fails on main, passes on branch).
    Workspace impact: (iii) none — every workspace script sets m explicitly. Follow-up (not filed): EllipseMultipoleScaled has no prior config for major_axis.

## dr1-sed-after-vis-lp
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/134
- issued: 2026-11-16
- session: claude-code (bounded Opus worker); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/dr1-sed-after-vis-lp
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/dr1-sed-after-vis-lp
