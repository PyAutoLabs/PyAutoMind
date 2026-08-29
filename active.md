# Active Tasks

## euclid-ci-test-mode
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/45
- prompt: active/ci_test_mode_simulated_datasets_latents.md
- issued: 2026-08-29
- session: claude --resume 3ff83ca2-99bf-4ef9-bc56-d22ee835c306
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/46
- heart-ack: workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)
- worktree: ~/Code/PyAutoLabs-wt/euclid-ci-test-mode
- classification: workspace (euclid_strong_lens_modeling_pipeline only; PyAutoLens read-only reference)
- epic: euclid-dr1-prep (phase 2 of 10; gates nothing hard, strongly preferred before phase 4)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-ci-test-mode
- next-skill: /prm (wait for PR #46 CI — Smoke Tests + Tests unit/slow, the repo's first runs)
