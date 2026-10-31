
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
- merged: euclid#117 (2a catalogue frame fix) 2026-10-31
- run: RAL 413687 sky_frame_bundle MODE=dry over inspect/dr1_catalogue_v5 (private code /mnt/ral/jnightin/active/euclid_dr1_p2c_code @910e5c8; submitted via scratch hpc/sync copy) → NEXT read dry report, MODE=live, re-package; then re-render pilot (~50, human review), 2b docs
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p3-jax-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/495
- issued: 2026-10-31
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p3-jax-rows
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p3-jax-rows (was stacked on #494; retargeted to main after #494 merged)
- prompt: active/likelihood_lifecycle_p3_jax_rows.md
- heart-override: RED overridden by the human 2026-10-31 (release validation integrate failure)
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/496 (READY, base main, CI lint pass on c218a428, MERGEABLE/CLEAN 2026-10-31 16:26)
- state 2026-10-31: all 63 cells + 5 experiments in; #494 merged first, #496 retargeted to main and regenerated; full suite 1920 passed locally.
- FINDING: JAX CPU slower on 0.11.2 + eigen flag (ral imaging median 1.46x; GPU unchanged) → re-check cpu_many_core designation proposals in step 4.
- next: human /prm on #496 (Heart RED: merge needs an explicit /prm in the same turn).

## magnification-errors-source-science
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
- issued: 2026-10-31
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-errors-source-science
- repos:
  - autolens_workspace: feature/magnification-errors-source-science
  - PyAutoFit: feature/magnification-errors-source-science
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1751 (MERGED 2026-10-31 e9d3c6a2 via human /prm; pending-release)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1751
- prompt: active/magnification_errors_source_science.md
- epic: cluster-strong-lensing (phase 7b)
- heart-red-override: authorized live by the human 2026-10-31 ("override heart red, go ahead with 7b"); RED reasons quoted on the issue; development only
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary

## howtolens-point-data
- issue: https://github.com/PyAutoLabs/HowToLens/issues/109
- issued: 2026-10-31
- session: Codex chat 01a191e7-652b-7620-a3ca-9e78dadd948e
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-point-data
- repos:
  - HowToLens: feature/howtolens-point-data
- prompt: active/tutorial_5_point_data.md
- heart-red-override: continuing approved HowToLens development under the session override and explicit instruction to apply/check Tutorial 5; `release validation FAILED (stage integrate)`; no release/test bypass
- tier: judge — merge mode: human /prm
- resume: approved point dataset section applied; run notebook/render and full smoke checks
