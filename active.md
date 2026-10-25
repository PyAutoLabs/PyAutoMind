## pre-release-docs-config
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/261
- issued: 2026-10-25
- status: blocked
- session: codex health/hygiene cleanup
- location: /workspace/scratch/f77499d15f98 (session clones)
- prompt: active/pre_release_docs_config.md
- next: local patch prepared and AST/prose/config/notebook generation verified; 41 script smoke checks passed. AutoFit two-notebook smoke blocked before cell execution by host ZMQ ip_resolver Operation not permitted; obtain compatible-runtime validation, then specific task Heart RED development authorization. Preserve three local source branches; no source commits, PRs, merges or releases. See issue #261 checkpoint.
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
- next: 2026-10-25 BATCH 1 COMPLETE 104/106 (2 known ao gpu-dense breakdown OOMs). PR B #461 OPEN (53 cells/104 rows copied, 13 superseded → history/, parity 53/53 match, coverage 2/6/238 → 104/7/135 current/stale/missing; tooling: release_pin from library_revisions via catalogue/release_revisions.json + history-aware series map; wiki/campaigns/imaging/likelihood_lifecycle_p2a.md). HUMAN 10-25 confirmed 'adopt' = supersede pilot → PyAutoPulse#75 OPEN (beab2d6; hst_mge_cpu_pilot status superseded; board rendered offline). NEXT: human /prm 461 FIRST → on the Pulse#75 branch run `pyauto-pulse board` ONLINE (lens receipt refetch) + check, commit → /prm 75 (merge main in if scheduled refresh conflicts) → close autolens_profiling#415 → close 2a (issue #456, record, worktree; restore task-root PyAutoPulse symlink) → 2b.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (MERGED 86c287d1; batch-1 measured walls)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/459 (MERGED 510b9556; W~ triplets guard test)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/461 (PR B: batch 1 rows + regen + wiki)
- workspace-pr: PyAutoPulse https://github.com/PyAutoLabs/PyAutoPulse/pull/75 (hst_mge_cpu_pilot superseded; refetch lens receipt after #461)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign
  - PyAutoPulse: feature/likelihood-lifecycle-p2a-pulse-adopt

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
