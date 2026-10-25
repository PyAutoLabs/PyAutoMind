
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: BATCH 0 DONE 2026-10-25 (412877 ral CPU + 412884 A100, private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a @ e1f52f47): 20/34 ok; 12 breakdown failures = 4 script bugs fixed in PR #458 (awaiting human /prm); A100 task 2 (delaunay ao jax_gpu_dense breakdown) GPU OOM → HUMAN RULING: record as limitation, no rerun. Legs take 1–33 min (not 14000 s). NEXT: human /prm 458 → git pull the private RAL checkout to new main → resubmit only failed legs: hpc/batch_cpu sbatch --array=0,4,8,10 submit_campaign_p2a_imaging_batch0_ral_cpu_fp64; hpc/batch_gpu sbatch --array=0,4,6,10,12,14,16,18 submit_campaign_p2a_imaging_batch0_a100_fp64 → walls.tsv + sacct MaxRSS → batch 1 --time/--mem → human go → PR B.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
