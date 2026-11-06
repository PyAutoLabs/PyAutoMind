
## magnification-maps-wiring
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/818
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-maps-wiring
- repos:
  - PyAutoArray: feature/magnification-maps-wiring
  - PyAutoGalaxy: feature/magnification-maps-wiring
  - PyAutoLens: feature/magnification-maps-wiring
- prompt: active/magnification_maps_8d_wiring_pretty.md
- epic: cluster-strong-lensing (phase 8d)
- tier: judge — merge mode: human /prm (PyAutoArray → PyAutoGalaxy → PyAutoLens)

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## sky-orientation-p2
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/115
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: (none; removed 2026-11-06)
- repos:
  - euclid_strong_lens_modeling_pipeline: (no branch; phase 2 remaining: R2 upload last, ECLIPSE website thumbnails)
- 2d-pilot: 2026-11-05 RAL 414200+414205 → inspect/north_up_pilot_20261105_v2 (50 lenses, 431/431 fits pass witness; 1 sersic load_error). Review page Science/scratch/sky_orientation_dr1/north_up_pilot_20261105_v2/review/index.html — AWAITING human by-eye review; branch local (c4f1247), no PR yet
- 2d: pilot approved by human 2026-11-05; PR https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/120 open (judge → human /prm); FULL RUN RAL 414229 (80 tasks, 15,007 lenses) → inspect/north_up_full_20261105
- 2d-done: 2026-11-05 north-up release built (RAL 414376) → inspect/dr1_catalogue_v5_release_northup (release_name dr1_catalogue_v5, 76.12 GB, PNG-only diff vs skyframe passed); fit-frame fallbacks vis_pix 91 / multi_wavelength 66 / fit_sersic 8. NEXT: human /prm PR #120, 2b docs, R2 upload last
- merged: euclid#120 (2d north-up re-render) 2026-11-06 (1c7f24c); worktree + branch removed
- merged: euclid#121 (2b release docs) 2026-11-06 (4ce84a5); worktree + branch removed; RAL 414391 done 2026-11-06: final release inspect/dr1_catalogue_v5_release_northup, SHA256SUMS 26/26 OK, superseded builds removed
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 2: 2.0 land v5 branch → 2a catalogue fix → 2b–2e)
- heart-red-override: extended live by the human 2026-10-31 to phase 2 ("Yes, extend it"); development only, merge via /prm
- merged: euclid#116 (2.0 land v5 branch) 2026-10-31
- merged: euclid#117 (2a catalogue frame fix) 2026-10-31
- run: 2c DONE — 413892 live bundle (29,929 coolest regenerated, WCS on 74,772 FITS, 0 errors); re-package 414041 → inspect/dr1_catalogue_v5_release_skyframe (20 parts, 88.24 GB, verified); JSON hard-rule diff vs 10-29 PASSED (inspect/json_diff_skyframe_vs_20261029.txt); 414110 relink rebuilds docs with project-relative snapshot.json paths (2026-11-03). R2 upload deferred to the very end (human 2026-11-03). NEXT 2d north-up re-render pilot (~50, human review), 2b docs
- tier: judge — merge mode: human /prm
- merged: euclid#119 (catalogue parity `_EmptyRow` stub hotfix, human-authorized 2026-11-05 under this claim) 2026-11-05
- 2d-plan: APPROVED by human 2026-11-03 ~18:10 (not started; nothing written yet). scripts/tools/render_north_up.py on branch feature/sky-orientation-p2d: read each zip's image/dataset.fits + files/tracer.json + image/adapt_images.fits + image/adapt_image_plane_mesh_grids.fits; flipud arrays/adapt images, mesh grid + positions y->-y, tracer via sky_frame.plus_y_north_from; re-solve FitImaging at max-L (no search); WITNESS log-L == stored to ~1e-6 every lens, data panel vs rgb_north_up.jpg, positions on arcs; library subplot_fit + image_with_positions, util.subplot_rgb on rgb_north_up.jpg, segmentation from FITS, fit_multi_wavelength per band from output_sed; N/E compass. Pilot ~50 (paper lenses + grade-stratified random + asymmetric) as 2-CPU/5GB ral jobs -> inspect/north_up_pilot_20261103/ + side-by-side review page. Then full run, re-package, 2b docs; R2 upload last.

## results-library-p5a-assistant
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/176
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: workspace-shipped, awaiting-merge (judge → human /prm; wiki-currency waits on a PyAutoFit release)
- worktree: ~/Code/PyAutoLabs-wt/results-library-p5a-assistant
- repos:
  - autolens_assistant: feature/results-library-p5a-assistant
- prompt: active/results_library_p5a_assistant.md
- epic: results-library (phase 5a)
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/177
- heart-ack: STALE 'release validation incomplete: no rehearsal for current source' (human 2026-11-02)

## gradient-correctness-sweep
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/517
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-correctness-sweep
- repos:
  - autolens_profiling: feature/gradient-correctness-sweep
- prompt: active/gradient_correctness_sweep.md
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/518 MERGED 2026-11-02 via /prm (32e13e85; items 10, 11 + sweep note). Umbrella stays open; further profiling-repo work re-syncs feature/gradient-correctness-sweep to main first
- phase: order approved 2026-11-02; done 10, 11 (PR #518), 12 (retired), 1 (re-filed narrower into draft/bug/autogalaxy/wrong_jax_gradient_on_mge_likelihoods_fd.md); item 2 IN PROGRESS (paused 2026-11-02 night, RAL 413991 PENDING)
- resume: (1) `sacct -j 413991` → when done pull output/p517_item2/{A_sparse_main,B_dense_main,C_sparse_tag}/…/gradient.json + .log from the RAL worktree into Science/scratch/gradient_correctness_sweep_2026-11-02/ral_item2/ and run small_step_check on them (A vs C = library effect incl #672; A vs B = sparse path vs CPU backend); (2) then items 3, 5 (local, seconds), 6, 13, 8/9/7 per the approved order in wiki/research/gradient_correctness_sweep.md
- compute-tracking: RAL 413991 (item 2, group/delaunay/euclid CPU, legs A sparse@main / B dense@main / C sparse@tag 2026.10.25.1; partition ral; human go 2026-11-02). RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/gradient-correctness-sweep (9d2ee2d3), private libs /mnt/ral/jnightin/PyAuto_wt/gradient-correctness-sweep; rows under output/p517_item2/<leg>/
- tier: judge — merge mode: human /prm

## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p4e-ingest
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/59
- issued: 2026-11-05
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p4e-ingest
- repos:
  - autolens_inference: feature/likelihood-lifecycle-p4e-ingest
- prompt: active/likelihood_lifecycle_p4e_ingest.md
- epic: likelihood-lifecycle (phase 4e)
- tier: judge — merge mode: human /prm; PR waits for the remaining phase-4 legs (human 2026-11-05)

## howtolens-stored-results
- issue: https://github.com/PyAutoLabs/HowToLens/issues/130
- issued: 2026-11-06
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/howtolens-stored-results
- repos:
  - HowToLens: feature/howtolens-stored-results
- prompt: active/howtolens-stored-results.md
- epic: howto-stored-results (phase 1 of 4: HowToLens ch2 + design gate)
- tier: judge — merge mode: human /prm

## critical-curves-jax-viz-feasibility
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/521
- issued: 2026-11-06
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/critical-curves-jax-viz-feasibility
- repos:
  - autolens_profiling: feature/critical-curves-jax-viz-feasibility
- prompt: active/critical_curves_jax_modeling_viz_feasibility.md
- pulse: organs/PyAutoPulse/tasks/critical_curves_jax_modeling_viz_feasibility.md
- parallel-claim: human ruled 2026-11-06 to share autolens_profiling with gradient-correctness-sweep (#517, paused); this task touches only scripts/lens/critical_curves/ + the critical-curves wiki
- tier: judge — merge mode: human /prm

## cti-docs-yml-caller
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/125
- issued: 2026-11-06
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cti-docs-yml-caller
- repos:
  - PyAutoCTI: feature/cti-docs-yml-caller
  - PyAutoHeart: feature/cti-docs-yml-caller
- prompt: active/docs_yml_caller.md
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
