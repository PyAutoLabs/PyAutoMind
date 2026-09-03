# Active Tasks

## positions-threshold-repin
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/721
- prompt: active/positions_threshold_knife_edge_repin.md
- issued: 2026-09-03
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: library-shipped, awaiting-merge (corrective PR open 2026-09-03; /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/722
- worktree: ~/Code/PyAutoLabs-wt/positions-threshold-repin
- repos:
  - PyAutoLens: feature/positions-threshold-repin
- heart-ack: 2026-09-03 human-authorized corrective PR for RED reason "PyAutoLens: CI failure" (cause PyAutoArray#519, test-only re-pin) and acknowledged "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old" for PR-open — never merge

## gaussian-precompute-p2
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/604
- prompt: active/gaussian_precompute_p2_jax_trace_time_constant.md
- issued: 2026-09-03
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; merge order PyAutoArray → PyAutoGalaxy → autolens_profiling; close-out via /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/520
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/605
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/216
- worktree: ~/Code/PyAutoLabs-wt/gaussian-precompute-p2
- repos:
  - PyAutoArray: feature/gaussian-precompute-p2
  - PyAutoGalaxy: feature/gaussian-precompute-p2
  - autolens_profiling: feature/gaussian-precompute-p2
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"; "PyAutoLens: CI failure" (third reason added 2026-09-03 evening, cause PyAutoArray#519, corrective PR PyAutoLens#722)
- heart-note: acknowledgement covers these three reasons; a further new reason at ship time re-blocks
- epic: gaussian-deflections-precompute (phase 2; ledger draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)

## euclid-cpu-two-stage-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49
- prompt: active/cpu_vis_lp_jax_vis_pix_numba_submission.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01BhD2t684rJZi1tT34u2KgR
- status: pr-open — https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50 (opened 2026-09-03; workspace-only, no pending-release, merge is human via /prm). Ship gate: pytest 72 passed, smoke 9/9. Both RAL routes COMPLETED (GPU 1 h 14 min on an A100, two-stage CPU 3 h 17 min on 8 cores).
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50
- heart-ack: human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "PyAutoLens: CI failure"; "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"
- follow-ups filed: draft/bug/euclid/gpu_per_lens_time_vs_documented_10_min.md (measured 74 min/lens vs the documented ~10 min; carries the apply_sparse_operator else-branch verdict), draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md (control test found no hang; boundary kept as the conservative default)
- worktree: ~/Code/PyAutoLabs-wt/euclid-cpu-two-stage-route
- repos:
  - euclid_strong_lens_modeling_pipeline (feature/euclid-cpu-two-stage-route)
- epic: euclid-dr1-prep (Mind phase 4; gates PyAutoCortex phases/euclid/dr1_prelim_10_lens_science_run)

## image-source-mappings-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/525
- prompt: active/mappings_guide_and_tutorial_rewrite.md
- issued: 2026-09-03
- session: claude --resume 7edd9743-c486-48ec-be0a-9f184a4898d4
- status: workspace-dev
- epic: image-source-mappings (phase 3 — ledger draft/feature/autoarray/image_source_mappings_epic.md; opened 2026-09-03 by user decision ahead of the PyAutoArray/PyAutoLens releases that gated it; every PR carries pending-release)
- heart-ack: human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"
- worktree: ~/Code/PyAutoLabs-wt/image-source-mappings-p3
- parallel-claim: autolens_workspace — over-sample-snr-double-division (#523) ran in its own worktree with disjoint files; MERGED 2026-09-03 (autolens_workspace#527), claim released — rebase onto main before shipping
- repos:
  - autolens_workspace: feature/image-source-mappings-p3
  - HowToLens: feature/image-source-mappings-p3
  - HowToGalaxy: feature/image-source-mappings-p3
  - autogalaxy_workspace: feature/image-source-mappings-p3
- summary: |
    Phase 3 of image-source-mappings (workspace). New guide autolens_workspace/scripts/guides/mappings.py
    (point → parametric region → pixelized region mappings with the 0.2/0.5/0.8 clump threshold demo,
    subplot_mappings, 4MOST brightest-position recipe with guide-level astropy WCS, magnification per image);
    HowToLens/HowToGalaxy tutorial_2_mappers rewritten to draw polygons via mapper.mappings_from + regions=,
    BUGGY line dropped; dead slim_indexes_for_pix_indexes sections in the pixelization delaunay.py /
    likelihood_function.py scripts fixed; prose + total_mappings_pixels config sweep. One issue, four PRs,
    one worktree. Fable session; execution delegated to Opus (subagent A guide, subagent B tutorials/dead sections).
