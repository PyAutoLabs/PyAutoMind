
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: BATCH 0 SUBMITTED 2026-10-25 from private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a (main e1f52f47; libs /mnt/ral/jnightin/profiling/PyAuto_2026.10.23.1, all 5 verified at tag; pin guard passed in both arrays): ral CPU array 412877 (14, %8) + A100 gres array 412884 (20, %2), --time 12h each leg-set. NEXT: when done, read output/p2a_logs/walls.tsv + sacct MaxRSS in that checkout → set batch 1 --time/--mem from measured walls → human go for batch 1 → PR B. Never touch euclid_dr1 jobs or the shared mirror.
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
