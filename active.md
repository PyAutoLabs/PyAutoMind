
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: 2026-10-25 BATCH 0 COMPLETE: 32/34 legs (reruns 412911/412915 clean; 2 ao jax_gpu_dense breakdowns = A100 OOM limitation, human ruling; rect ao one found on rerun). #459 guard-test MERGED 510b9556. Batch-1 walls PR #460 OPEN (ac566251+931b11be; RAL arrays 1h, mem ao 64 / others 32; A100 3h, hst 3.5h). NEXT: human /prm 460 → ff private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a (nohup; slow FS) → HUMAN GO → submit 4 RAL arrays (hpc/batch_cpu/submit_campaign_p2a_imaging_ral_cpu_<inst>_fp64) + 4 A100 jobs (hpc/batch_gpu/submit_campaign_p2a_imaging_a100_<inst>_fp64) → PR B.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (batch-1 measured walls)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## assertion-repr
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1716
- issued: 2026-10-25
- session: ChatGPT Work Codex (session ID unavailable)
- status: draft-pr, awaiting-smoke
- prompt: active/assertion_repr_recurses_forever.md
- worktree: /workspace/scratch/c07c1c24c298/worktrees/assertion-repr
- coordination: four-task group explicitly requested 2026-10-25; independent PRs, shared validation, human merge
- repos:
  - PyAutoFit: feature/assertion-repr

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1720
- validation: combined exact four-head serial suite 3913 passed, 1 skipped, 1 xfailed; identifier parity with main; clean four-way merge; 600 seeded-test repetitions passed
- blocked-by: downstream smoke workspaces absent; draft PR is not cleared for merge
- next: complete downstream workspace smoke and required GitHub checks, then human /prm; prefer #1723 first to remove the existing start-point flake

- head: 04ae11791d905eda26992f89b1084ddbc1617f52
- evidence: https://github.com/PyAutoLabs/PyAutoFit/pull/1720 (validation results and combined commit set)

## assertion-names
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1717
- issued: 2026-10-25
- session: ChatGPT Work Codex (session ID unavailable)
- status: draft-pr, awaiting-smoke
- prompt: active/add_assertion_name_silently_dropped.md
- worktree: /workspace/scratch/c07c1c24c298/worktrees/assertion-names
- coordination: four-task group explicitly requested 2026-10-25; independent PRs, shared validation, human merge
- repos:
  - PyAutoFit: feature/assertion-names

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1721
- validation: combined exact four-head serial suite 3913 passed, 1 skipped, 1 xfailed; identifier parity with main; clean four-way merge; 600 seeded-test repetitions passed
- blocked-by: downstream smoke workspaces absent; draft PR is not cleared for merge
- next: complete downstream workspace smoke and required GitHub checks, then human /prm; prefer #1723 first to remove the existing start-point flake

- head: 45474dcf7291213e0393d07610c3f53dcb880dcd
- evidence: https://github.com/PyAutoLabs/PyAutoFit/pull/1721 (validation results and combined commit set)

## fixed-instance-tuples
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1718
- issued: 2026-10-25
- session: ChatGPT Work Codex (session ID unavailable)
- status: draft-pr, awaiting-smoke
- prompt: active/direct_instance_tuples_double_counts_constants.md
- worktree: /workspace/scratch/c07c1c24c298/worktrees/fixed-instance-tuples
- coordination: four-task group explicitly requested 2026-10-25; independent PRs, shared validation, human merge
- repos:
  - PyAutoFit: feature/fixed-instance-tuples

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1722
- validation: combined exact four-head serial suite 3913 passed, 1 skipped, 1 xfailed; identifier parity with main; clean four-way merge; 600 seeded-test repetitions passed
- blocked-by: downstream smoke workspaces absent; draft PR is not cleared for merge
- next: complete downstream workspace smoke and required GitHub checks, then human /prm; prefer #1723 first to remove the existing start-point flake

- head: fa8db344be35c80996fcd5a6004c35c25527d46b
- evidence: https://github.com/PyAutoLabs/PyAutoFit/pull/1722 (validation results and combined commit set)

## seed-start-point-tests
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1719
- issued: 2026-10-25
- session: ChatGPT Work Codex (session ID unavailable)
- status: draft-pr, awaiting-smoke
- prompt: active/start_points_test_unseeded_identical_figures_of_merit_flake.md
- worktree: /workspace/scratch/c07c1c24c298/worktrees/seed-start-point-tests
- coordination: four-task group explicitly requested 2026-10-25; independent PRs, shared validation, human merge
- repos:
  - PyAutoFit: feature/seed-start-point-tests

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1723
- validation: combined exact four-head serial suite 3913 passed, 1 skipped, 1 xfailed; identifier parity with main; clean four-way merge; 600 seeded-test repetitions passed
- blocked-by: downstream smoke workspaces absent; draft PR is not cleared for merge
- next: complete downstream workspace smoke and required GitHub checks, then human /prm; prefer #1723 first to remove the existing start-point flake

- head: 5284f039bec44fdd06aa196373026031a706f9fb
- evidence: https://github.com/PyAutoLabs/PyAutoFit/pull/1723 (validation results and combined commit set)
