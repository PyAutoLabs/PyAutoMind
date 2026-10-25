
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: 2026-10-25 BATCH 1 SUBMITTED (human 'prm and continue' = go) from private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a @ 86c287d1 (#460 merged): ral CPU arrays ao 412923 / euclid 412924 / hst 412925 / jwst 412926 (1h, 44 cells) + A100 jobs ao 412927 / euclid 412943 / hst 412944 / jwst 412945 (3h, hst 3.5h; 62 cells). Rows → output/p2a_batch1/results/ (scratch). Expected ao A100 jax_gpu_dense breakdown OOMs = known limitation. NEXT: check sacct + walls.tsv (START without WALL = killed at --time) → pull complete cells → PR B (copy complete rows into results/, superseded → history/<pin>_<date>/, parity_witness --check, regen catalogue → dashboard → coverage; adopt+close Pulse hst_mge_cpu_pilot).
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (MERGED 86c287d1; batch-1 measured walls)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
