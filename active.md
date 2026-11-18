
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
- coordination: human approved 2026-11-18 (Q8) sharing PyAutoFit with results_library_p5c_dr1_census — the census is read-only on RAL against released 2026.11.12.1 and writes only a PyAutoCortex ledger line; no PyAutoFit edits, no file overlap

## galaxy-duplicate-pytree-registration
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/693
- session: Claude Code live session 2026-11-18 (resumed the crashed shift 2026-11-14-pm2 worker's unpushed commit)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/702
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/702
- worktree: ~/Code/PyAutoLabs-wt/galaxy-duplicate-pytree-registration
- prompt: active/galaxy_duplicate_pytree_registration_after_jax_fitness.md
- heart-ack:
  - organism verdict RED/YELLOW/STALE on local-checkout rows (dirty or behind canonical checkouts, manifest drift), release-scope (no rehearsal for current source) and human-only rows (open PRs) — none on the touched repos; each close-out reads the dev-ship gate (readiness --dev --repos)
- repos:
  - PyAutoArray: feature/galaxy-duplicate-pytree-registration

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

## delaunay-interpolated-plot
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/700
- issued: 2026-11-17
- session: Claude Code cloud session (claude.ai/code, session_016nhQ8MtKvVD9fBkNBqcMb4); laptop follow-ups 2026-11-18 in Claude Code desktop (Opus 5.5, session ID unavailable)
- status: awaiting-merge (library + workspace PRs open; human /prm)
- location: cloud container clones (no worktrees on this surface); resume from the pushed branches
- worktree: ~/Code/PyAutoLabs-wt/delaunay-interpolated-plot (laptop, created 2026-11-18 for the follow-ups)
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
- decisions: fit.png key `fit: subplot_fit_source_interpolated: true` (default ON, human 2026-11-17, re-approved 2026-11-18). Source column (human 2026-11-18): No Zoom always bottom right (11); middle right (7) = Source Plane (Interpolated) (Delaunay/KNN + key on, max-zoom extent) else Mid Zoom; top right (3) = Max Zoom. Same column in imaging fit.png, fit_log10.png and interferometer fit.png (interferometer drops Dirty S/N; Dirty Model Image -> panel 2; source panels share vmax). Delaunay/KNN inversion_#.png right column = Max Zoom / Interpolated / No Zoom; rectangular inversion unchanged. Interpolated panel square, full-height colorbar. Array-free interferometer 2x3 untouched. Key mirrored into autoarray plots.yaml and the 5 autolens workspaces
- follow-up: draft/feature/autolens/interferometer_fit_png_show_zoomed_no_zoom.md SUPERSEDED by PyAutoLens#864 commit 1e212b43b (interferometer fit.png now Max Zoom / Interpolated / No Zoom); delete at close-out
- laptop-follow-ups: DONE 2026-11-18 - smoke 124/124 pass (autolens_workspace 42 + 2 notebooks, autolens_workspace_test 39, HowToLens 41) at the final heads; Delaunay/KNN figures re-rendered in autolens_visualization + autogalaxy_visualization and pixel-diffed vs main (6 changed as intended, 44 identical, rectangular control identical); results: https://github.com/PyAutoLabs/PyAutoArray/issues/700#issuecomment-6975110365 ; review page C:\Users\Jammy\Workspace\Science\scratch\delaunay_interpolated_plot_2026-11-18\index.html ; re-rendered gallery PNGs not committed
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
- next: human /prm in library-first order (PyAutoArray#701 -> PyAutoLens#864 -> the 5 workspace PRs; heads e8a174a6 / 1e212b43b / 627a35cb / bee5f24 / 9b3cbab / 787cc0a / e99de4c); #46 update drafted for the human (not posted)

## batch-claim-gate-declared-repos
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/675
- issued: 2026-11-18
- session: Claude Code desktop (WSL)
- status: library-dev
- prompt: active/batch_claim_gate_target_overrides_declared_repos.md
- worktree: /home/jammy/Code/PyAutoLabs-wt/batch-claim-gate-declared-repos
- tier: notify — merge mode: auto-merge on green (effective level supervised)
- repos:
  - PyAutoBrain: feature/batch-claim-gate-declared-repos
