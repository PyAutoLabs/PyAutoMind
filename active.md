
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

## howto-paired-review
- issue: https://github.com/PyAutoLabs/HowToLens/issues/103
- issued: 2026-10-31
- prompt: active/howto_paired_review_ship.md
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howto-paired-review
- repos:
  - HowToLens: feature/howto-paired-review
  - HowToGalaxy: feature/howto-paired-review
- heart-red-override:
  - authorization: Human “Fix those plotting errors, rerun the tests and then prm everything. I approve the fixes and the Heart RED override.” (2026-10-31).
  - reasons: release validation FAILED (stage integrate)
  - validation: Galaxy full smoke 32 passed; Lens full smoke 49 passed plus corrected Tutorial 2 retest passed. Notebook/catalogue/path checks and actual mapping render passed. Final GitHub smoke required before merge.
  - scope: development shipping plus current-turn merge on green required checks; no release or CI bypass.

- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/93
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/104

## sky-orientation-p2
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/115
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sky-orientation-p2
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/land-v5-catalogue
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 2: 2.0 land v5 branch → 2a catalogue fix → 2b–2e)
- heart-red-override: extended live by the human 2026-10-31 to phase 2 ("Yes, extend it"); development only, merge via /prm
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
