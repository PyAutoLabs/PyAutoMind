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
- next: 2026-10-25 BATCH 1 COMPLETE 104/106 (2 known ao gpu-dense breakdown OOMs). PR B #461 OPEN (53 cells/104 rows copied, 13 superseded → history/, parity 53/53 match, coverage 2/6/238 → 104/7/135 current/stale/missing; tooling: release_pin from library_revisions via catalogue/release_revisions.json + history-aware series map; wiki/campaigns/imaging/likelihood_lifecycle_p2a.md). NEXT: human /prm 461 → Pulse: refetch lens receipt + adopt/close hst_mge_cpu_pilot (PyAutoPulse PR; human to confirm 'adopt' = supersede pilot question with the 2a mge/hst jax_cpu_dense cell) → close 2a (issue #456, record, worktree) → 2b.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (MERGED 86c287d1; batch-1 measured walls)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/459 (MERGED 510b9556; W~ triplets guard test)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/461 (PR B: batch 1 rows + regen + wiki)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
