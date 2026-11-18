
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

## delaunay-interpolated-plot
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/700
- issued: 2026-11-17
- session: Claude Code cloud session (claude.ai/code, session_016nhQ8MtKvVD9fBkNBqcMb4)
- status: awaiting-merge (library + workspace PRs open; human /prm)
- location: cloud container clones (no worktrees on this surface); resume from the pushed branches
- repos:
  - PyAutoArray: feature/delaunay-interpolated-plot
  - PyAutoLens: feature/delaunay-interpolated-plot
  - autolens_workspace: feature/delaunay-interpolated-plot
  - autolens_workspace_test: feature/delaunay-interpolated-plot
  - HowToLens: feature/delaunay-interpolated-plot
  - autolens_assistant: feature/delaunay-interpolated-plot
  - autolens_visualization: feature/delaunay-interpolated-plot
- prompt: active/delaunay_plot_shows_likelihood_interpolant.md
- community: https://github.com/PyAutoLabs/.github/discussions/46 (draft the update for the human; do not post)
- coordination: human approved 2026-11-17 sharing PyAutoArray with galaxy-duplicate-pytree-registration (abstract_ndarray.py only) and autolens_workspace with cluster-regime-narrative (scripts/cluster/ only); no file overlap
- decisions: fit.png key `fit: subplot_fit_source_interpolated: true` (default ON, human 2026-11-17). Irregular-mesh source → imaging right column = Max Zoom / No Zoom (triangles) / Interpolated bottom right (max-zoom extent); false or rectangular/parametric → max/mid/no zoom. Interferometer: Zoomed (7) + Interpolated (11) by default, zoomed + no zoom when off; array-free 2x3 adds Interpolated in its free panel. PyAutoLens only; key mirrored with default true into autoarray plots.yaml and the 5 autolens workspaces
- follow-up: draft/feature/autolens/interferometer_fit_png_show_zoomed_no_zoom.md (interferometer fit.png should show zoomed + no zoom + interpolated; #864 drops no zoom when the key is on)
- laptop-follow-ups: workspace smoke for the affected workspaces; re-render Delaunay figures in autolens_visualization / autogalaxy_visualization (cloud session has no LFS datasets / gallery harness)
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/701
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/864
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/678
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/367
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/137
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/187
- workspace-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/19
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/701
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/864
- next: human /prm in library-first order (PyAutoArray#701 → PyAutoLens#864 → the 5 workspace PRs); laptop follow-ups before close-out; #46 update drafted for the human (not posted)

## shift-readiness-pass
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/671
- issued: 2026-11-18
- session: claude-code desktop (WSL), Opus 5.5, ~/Code/PyAutoLabs session
- status: awaiting-merge (slice 1; Mind#585 merges first; slice 2 stays on this prompt)
- worktree: /home/jammy/Code/PyAutoLabs-wt/shift-readiness-pass
- repos:
  - PyAutoBrain: feature/shift-readiness-pass
  - PyAutoMind: feature/shift-readiness-pass
- prompt: active/shift_readiness_pass_and_decisions_sheet.md
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/674
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/585
- epic: autonomous-orchestrators (phase 10, M3.3 slice 1; slice 2 follows the M3.2 shift)
- tier: judge — merge mode: human /prm

## worker-model-effort
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/672
- issued: 2026-11-18
- session: claude-code desktop (WSL), Opus 5.5, ~/Code/PyAutoLabs session
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs-wt/worker-model-effort
- repos:
  - PyAutoBrain: feature/worker-model-effort
- prompt: active/worker_model_effort_medium.md
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/673
- coordination: human approved sharing PyAutoBrain with shift-readiness-pass (same session, 2026-11-18); different functions in _orchestrator.py
- epic: autonomous-orchestrators
- tier: judge — merge mode: human /prm
