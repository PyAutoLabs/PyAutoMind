# Active Tasks

## euclid-ci-test-mode
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/45
- prompt: active/ci_test_mode_simulated_datasets_latents.md
- issued: 2026-08-29
- session: claude --resume 3ff83ca2-99bf-4ef9-bc56-d22ee835c306
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/euclid-ci-test-mode
- classification: workspace (euclid_strong_lens_modeling_pipeline only; PyAutoLens read-only reference)
- epic: euclid-dr1-prep (phase 2 of 10; gates nothing hard, strongly preferred before phase 4)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-ci-test-mode
- next-skill: /ship_workspace (stages A → B → C → D in flight)

## overflow-flood-refs-smc-cell
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/196
- prompt: active/overflow_flood_refs_smc_cell.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/overflow-flood-refs-smc-cell
- classification: library (autolens_profiling only; Wave B of the overflow-flood fix wave, Wave A merged)
- repos:
  - autolens_profiling: feature/overflow-flood-refs-smc-cell
- next-skill: /ship_library
