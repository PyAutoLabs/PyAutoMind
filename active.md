
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## hpc-campaign-p5a-assistant
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/172
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p5a-assistant
- repos:
  - autolens_assistant: feature/hpc-campaign-p5a-assistant
- prompt: active/hpc_campaign_p5a_assistant.md
- epic: hpc-campaign (phase 5)
- heart-red-override: authorized live by the human 2026-10-30 ("Override + approve") for hpc-campaign phase 5; RED reasons quoted on the issue; development only, merge via /prm
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/173 (MERGED 2026-10-31)
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/174
- resume: 2026-10-31 — #173 merged; #174 (feature/hpc-campaign-p5a-v2, retargeted to main) green on boundary + colab, RED on wiki-currency only because it audits RELEASED PyAutoFit, which lacks autofit.campaign (pending-release) — /prm #174 after the next PyAutoFit release (rerun wiki-currency first); then close out p5a

## likelihood-lifecycle-p2bc-quiet-ingest
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/493
- issued: 2026-10-31
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2bc-quiet-ingest
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2bc-quiet-ingest
- prompt: active/likelihood_lifecycle_p2bc_quiet_rerun_ingest.md
- heart-override: RED overridden by the human 2026-10-31 (release validation integrate failure; autogalaxy + autolens_profiling red; 1 dirty worktree)
- tier: judge — merge mode: human /prm
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/494 (DRAFT)
- state 2026-10-31: 9/21 quiet cells ingested (7 sma 2b + 2 2c), regenerated, pushed (ad17175b). 12 cells above sma HELD: witnesses not_assessed.
- in flight (RAL): 413675 refs in autolens_profiling_p2b_rerun (alma _0/_3 refs written; false 'no row' fixed by mkdir output/p2b_batch1); finalise 413682 afterany:413675 (log /mnt/ral/jnightin/scratch/p2b_quiet_finalise.<jobid>.out, marker P2BQUIETFINALISEDONE). Also 413669 = phase-3 2b A100 refs in autolens_profiling_p2dg (step 3).
- resume: sacct 413682 → re-pull output/p2b_quiet into output/quiet_logs/ (tar over ssh) → python3 output/quiet_logs/ingest_quiet.py output/quiet_logs/pin.json --apply (script in PR #494 body logic: parity match, fit.png, final write, pinned revisions; history/2026.10.25.1_2026-10-28) → commit → regenerate (build_catalogue, build_setup_wiki, coverage_matrix, build_dashboard w/ PYAUTO_BRAIN, build_readme) → commit → update 2b journal → gh pr ready → /ship_workspace.

## sky-orientation-p2
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/115
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sky-orientation-p2
- repos:
  - euclid_strong_lens_modeling_pipeline: (no branch; next sub-phase 2c)
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 2: 2.0 land v5 branch → 2a catalogue fix → 2b–2e)
- heart-red-override: extended live by the human 2026-10-31 to phase 2 ("Yes, extend it"); development only, merge via /prm
- merged: euclid#116 (2.0 land v5 branch) 2026-10-31
- merged: euclid#117 (2a catalogue frame fix) 2026-10-31 → NEXT 2c RAL bundle run (stages 1b + 3b over dr1_sep1) + north-up re-render pilot (~50 lenses, human review), then 2b docs
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p3-jax-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/495
- issued: 2026-10-31
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p3-jax-rows
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p3-jax-rows (stacked on feature/likelihood-lifecycle-p2bc-quiet-ingest, human 2026-10-31)
- prompt: active/likelihood_lifecycle_p3_jax_rows.md
- heart-override: RED overridden by the human 2026-10-31 (release validation integrate failure)
- tier: judge — merge mode: human /prm
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/496 (DRAFT, base feature/likelihood-lifecycle-p2bc-quiet-ingest)
- state 2026-10-31: 61/63 cells + 5 experiments committed (dc2d64a7). HELD: 2b A100 jvla jax_gpu_sparse_fp64_wtilde x2 → RAL 413669_2/_5 (p2dg) finalises witnesses.
- FINDING: JAX CPU slower on 0.11.2 + eigen flag (ral imaging median 1.46x; GPU unchanged) → re-check cpu_many_core designation proposals in step 4.
- resume: sacct 413669 → tar-pull p2dg output/p2b_batch1/results/interferometer/*/jvla/jax_gpu_sparse_fp64_wtilde → python3 output/ingest_rows.py output/pin.json <root> --apply (narrow root; never re-run on already-ingested dirs) → commit → regenerate → 2b/2c journals → gh pr ready (after #494 merges: retarget main, regenerate).

## magnification-errors-source-science
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
- issued: 2026-10-31
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-errors-source-science
- repos:
  - autolens_workspace: feature/magnification-errors-source-science
  - PyAutoFit: feature/magnification-errors-source-science
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1751 (judge, human /prm; pending-release)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1751
- prompt: active/magnification_errors_source_science.md
- epic: cluster-strong-lensing (phase 7b)
- heart-red-override: authorized live by the human 2026-10-31 ("override heart red, go ahead with 7b"); RED reasons quoted on the issue; development only
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary
## howtolens-ray-tracing-merge
- issue: https://github.com/PyAutoLabs/HowToLens/issues/105
- issued: 2026-10-31
- session: Codex chat 01a191e7-652b-7620-a3ca-9e78dadd948e
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ray-tracing-merge
- repos:
  - HowToLens: feature/howtolens-ray-tracing-merge
- prompt: active/ray_tracing_merge.md
- heart-red-override: user approved development on Heart RED for this task; exact reasons in issue 105
- tier: judge — merge mode: human /prm
- resume: apply approved Tutorial 2 Units and multi-galaxy blocks; continue Tutorial 3 five-block review, using one tracer

