# Active Tasks

## euclid-pipeline-parity
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/43
- prompt: active/pipeline_parity_with_science_euclid.md
- issued: 2026-08-29
- session: claude --resume 3ff83ca2-99bf-4ef9-bc56-d22ee835c306
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/44
- heart-ack: workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)
- worktree: ~/Code/PyAutoLabs-wt/euclid-pipeline-parity
- classification: workspace (euclid_strong_lens_modeling_pipeline only; PyAutoLens read-only reference)
- epic: euclid-dr1-prep (phase 1 of 10; gates phases 2, 3, 4)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-pipeline-parity
- next-skill: /prm (no CI on this repo yet — phase 2; merge on local evidence: pytest 24p, smoke 8/8)

## unpark-multi-galaxy-scaling-relation-slam
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/514
- prompt: active/unpark_multi_galaxy_scaling_relation_slam.md
- issued: 2026-08-29
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ci-smoke-bundle-2b
- classification: workspace (autolens_workspace only)
- bundle: ci-smoke — bundle 2b (shared worktree; own branch, own PR; worked before the guide task)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- repos:
  - autolens_workspace: feature/unpark-multi-galaxy-scaling-relation-slam
- next-skill: /ship_workspace

## multi-plane-guide-cross-validation
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/515
- prompt: active/multi_plane_cross_validation_guide.md
- issued: 2026-08-29
- status: workspace-dev (queued behind unpark-multi-galaxy-scaling-relation-slam in the same worktree)
- worktree: ~/Code/PyAutoLabs-wt/ci-smoke-bundle-2b
- classification: workspace (docs; phase 2 of PyAutoLens#714, library phase merged in #715)
- bundle: ci-smoke — bundle 2b (shared worktree; own branch, own PR)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- repos:
  - autolens_workspace: feature/multi-plane-guide-cross-validation
- next-skill: /ship_workspace
