
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

## dataset-model-free-grid-offset-pytree-roundtrip
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1777
- issued: 2026-11-16
- session: shift worker 2026-11-16-pm (b778571d); Claude Code worker 2026-11-18 (session ID unavailable)
- status: library-shipped, awaiting-merge (PR #1779 opened 2026-11-18; tests 4295 passed, smoke autofit+autogalaxy 26/26; human runs /prm)
- prompt: active/dataset_model_free_grid_offset_pytree_roundtrip.md
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1777#issuecomment-6925508074
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
- worktree: ~/Code/PyAutoLabs-wt/dataset-model-free-grid-offset-pytree-roundtrip
- repos:
  - PyAutoFit: feature/model-pytree-tuple-prior
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1779
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1779
- coordination: shares PyAutoFit with ep-projected-model-shared-prior (#1773, PR #1778 awaiting /prm); human-approved override, separate worktree off main, no file overlap (that task: samples/samples.py + test_unification.py; this one: prior_model.py, tuple_prior.py, jax/pytrees.py + new test)
- heart-ack:
  - acknowledged by the human 2026-11-16 ("Heart ack so its ok"): RED on local-checkout rows (7 library checkouts behind/dirty), 5 manifest-drift legs, release-scope (no rehearsal for current source) and human-only (PyAutoArray PR open 13d); none on the touched repos
