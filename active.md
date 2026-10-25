
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: 2026-10-25 #458 MERGED 7679f564 (human /prm); private RAL checkout ff'd to 7679f564; RERUN of the 12 failed batch-0 legs SUBMITTED: CPU 412911 (--array=0,4,8,10) + A100 412915 (--array=0,4,6,10,12,14,16,18%2). A100 task 2 (delaunay ao jax_gpu_dense breakdown) OOM = recorded limitation (human ruling), not rerun. Follow-up pix_sizes check on 3 interferometer/datacube scripts: NO BUG (curvature triplets unmasked by design, as in the library); guard-test-only commit acd83363 on local branch feature/likelihood-lifecycle-p2a-pix-sizes-followup, unpushed pending human choice. NEXT: rerun done → walls.tsv + sacct MaxRSS → batch 1 --time/--mem → human go → PR B.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md
