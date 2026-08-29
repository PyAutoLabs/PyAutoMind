# Active Tasks

## euclid-pipeline-parity
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/43
- prompt: active/pipeline_parity_with_science_euclid.md
- issued: 2026-08-29
- session: claude --resume 3ff83ca2-99bf-4ef9-bc56-d22ee835c306
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/euclid-pipeline-parity
- classification: workspace (euclid_strong_lens_modeling_pipeline only; PyAutoLens read-only reference)
- epic: euclid-dr1-prep (phase 1 of 10; gates phases 2, 3, 4)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-pipeline-parity
- next-skill: /ship_workspace (stages A+B → C → D → E in flight)

## harvest-0829-phase8b-final
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/194
- prompt: active/harvest_0829_phase8b_final_verdict.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/harvest-0829-phase8b-final
- classification: library (autolens_profiling only — results, ledger notes, wall rates, submit exit-code guard)
- epic: jax-inference-profiling
- repos:
  - autolens_profiling: feature/harvest-0829-phase8b-final
- library-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/195
- commit: 45c3abd
- workspace-impact: none — autolens_profiling exports no API and no library source changed; the only executable edits are wall/rates.py (additive table row), one SLURM submit header, and a SLURM-scoped guard in activate.sh
- heart: YELLOW at ship time, acknowledgement OUTSTANDING — reasons are release-chain and in other repos ("workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)", "release validation incomplete: no rehearsal for current source"); surfaced verbatim in the PR body for the human to answer before merge
- next-skill: /prm (merge stays human)

## multi-plane-cross-validation
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/714
- prompt: active/cross_validate_multi_plane_ray_tracing.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/ci-smoke-bundle-2
- classification: library (phase 1 — PyAutoLens test module; phase 2 workspace guide filed as a follow-up prompt)
- bundle: ci-smoke — bundle 2 (shared worktree; own branch, own PR)
- repos:
  - PyAutoLens: feature/multi-plane-cross-validation
  - PyAutoGalaxy: feature/ci-smoke-bundle-2 (claimed, no edits expected)
- next-skill: /ship_library

## unpark-imaging-scaling-relation-slam
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/512
- prompt: active/unpark_imaging_scaling_relation_slam.md
- issued: 2026-08-29
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ci-smoke-bundle-2
- classification: workspace (autolens_workspace only)
- bundle: ci-smoke — bundle 2 (shared worktree; own branch, own PR)
- repos:
  - autolens_workspace: feature/unpark-imaging-scaling-relation-slam
- next-skill: /ship_workspace
