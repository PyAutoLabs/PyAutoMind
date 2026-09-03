# Active Tasks

## gaussian-precompute-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/528
- prompt: active/gaussian_precompute_p3_downstream_sweep.md
- issued: 2026-09-03
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gaussian-precompute-p3
- repos:
  - autolens_workspace: feature/gaussian-precompute-p3
- parallel-claim: autolens_workspace also claimed by image-source-mappings-p3 (#525); file sets disjoint (that branch touches features/pixelization/*, smoke_tests.txt, workspace_index.json, tutorials; this task touches only scripts/**/mass_stellar_dark/slam.py + its notebook) — human-approved 2026-09-03; second to merge rebases
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"; "PyAutoLens: CI failure" (cleared on main by PyAutoLens#722, snapshot may lag) — a further new reason at ship time re-blocks
- epic: gaussian-deflections-precompute (phase 3; ledger draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)

## cortex-checkin-p1-shed-review-slot
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/9
- prompt: active/cortex_checkin_p1_shed_review_slot.md
- issued: 2026-09-03
- session: claude --resume session_013HsZA1ufn3msgPiDFxEXa6
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-checkin-p1-shed-review-slot
- repos:
  - PyAutoCortex: feature/cortex-checkin-p1-shed-review-slot
  - PyAutoBrain: feature/cortex-checkin-p1-shed-review-slot
- epic: cortex-checkin (phase 1; ledger draft/maintenance/pyautocortex/cortex_checkin_epic.md)

## euclid-cpu-two-stage-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49
- prompt: active/cpu_vis_lp_jax_vis_pix_numba_submission.md
- issued: 2026-09-02
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01BhD2t684rJZi1tT34u2KgR
- status: pr-open — https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50 (opened 2026-09-03; workspace-only, no pending-release, merge is human via /prm). Ship gate: pytest 72 passed, smoke 9/9. Both RAL routes COMPLETED (GPU 1 h 14 min on an A100, two-stage CPU 3 h 17 min on 8 cores). Two commits added post-open: d32d58e fixes the apply_sparse_operator drift on the JAX path (initial_lens_model.py and full_model.py), f092efe records the GPU re-measurement (job 342264, 1 h 44 min on a 25% slower node — the fix is a correctness fix, not a speed-up).
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50
- heart-ack: human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "PyAutoLens: CI failure"; "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"
- follow-ups filed: draft/bug/euclid/gpu_per_lens_time_vs_documented_10_min.md (re-scoped 2026-09-03 — the apply_sparse_operator drift is fixed in PR #50 and measured not to be the cause; the ~7x gap to the documented ~10 min stays open against the science config/, per-lens JIT and visualisation, or the claim's provenance), draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md (control test found no hang; boundary kept as the conservative default)
- worktree: ~/Code/PyAutoLabs-wt/euclid-cpu-two-stage-route
- repos:
  - euclid_strong_lens_modeling_pipeline (feature/euclid-cpu-two-stage-route)
- epic: euclid-dr1-prep (Mind phase 4; gates PyAutoCortex phases/euclid/dr1_prelim_10_lens_science_run)
