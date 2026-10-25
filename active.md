## pre-release-docs-config
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
- issued: 2026-10-25
- status: workspace-dev
- session: codex health/hygiene cleanup
- location: /workspace/scratch/f77499d15f98 (session clones)
- prompt: active/pre_release_docs_config.md
- next: implement five documentation boundary repairs and 25 config mirrors; verify AST, prose, effective config, generated notebooks and smoke. No source shipping/merge/release authorization under Heart RED yet.
- repos:
  - HowToFit: feature/pre-release-docs-config
  - autofit_workspace: feature/pre-release-docs-config
  - autogalaxy_workspace: feature/pre-release-docs-config


## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: 2026-10-25 BATCH 1 COMPLETE 16:04 UTC (#460 merged 86c287d1; jobs ral CPU 412923-6 + A100 412927/412943-5 from private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a): 104/106 legs, only the 2 known ao jax_gpu_dense breakdown OOMs failed (human ruling: limitation); none killed at --time; outputs rsynced to worktree output/p2a_batch1 + p2a_logs. PR B IN PROGRESS (Opus worker) on feature/likelihood-lifecycle-p2a-imaging-results: history moves → copy complete rows → catalogue/dashboard/coverage regen → wiki page. Then Pulse refetch + adopt/close hst_mge_cpu_pilot → human /prm → close 2a.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (MERGED 86c287d1; batch-1 measured walls)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/459 (MERGED 510b9556; W~ triplets guard test)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
