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
