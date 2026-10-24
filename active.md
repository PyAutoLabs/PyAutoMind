
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: RESUME 2026-10-25 — PR A #457 MERGED 2026-10-24. Batch 0 NOT yet submitted (human said 'set off batch', then 'wrap up, sort tomorrow'). RAL private lib checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.23.1 clone was IN PROGRESS at wrap-up (nohup, log clone.log; verify all 5 libs `git describe --tags` = 2026.10.23.1, re-clone any missing). Then: private autolens_profiling checkout on RAL at merged main (not the shared mirror) → sbatch hpc/batch_cpu/submit_campaign_p2a_imaging_batch0_ral_cpu_fp64 (ral, 14) + hpc/batch_gpu/submit_campaign_p2a_imaging_batch0_a100_fp64 (gres, 20, %2) from it; euclid_dr1 jobs on ral — never touch. Then walls.tsv → measured walls → batch 1 (human go) → PR B
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
