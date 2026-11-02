
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

## magnification-errors-source-science
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
- issued: 2026-10-31
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-errors-source-science
- repos:
  - autolens_workspace: feature/magnification-errors-source-science
- released-claims: PyAutoFit (2026-11-02 by results-library-p2-completeness session — #1751 merged + released in 2026.11.1.1; wt PyAutoFit is detached on main)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1751 (MERGED 2026-10-31 e9d3c6a2 via human /prm; pending-release)
- prompt: active/magnification_errors_source_science.md
- epic: cluster-strong-lensing (phase 7b)
- heart-red-override: authorized live by the human 2026-10-31 ("override heart red, go ahead with 7b"); RED reasons quoted on the issue; development only
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary

## likelihood-lifecycle-p6c-gradient-walls
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/509
- issued: 2026-11-01
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6c-gradient-walls
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p6c-gradient-walls
  - autolens_profiling: feature/likelihood-lifecycle-p6c-v2-walls
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/511 (v2 walls; MERGED 2026-11-02 1cdf84bf via human /prm)
- compute-pending: RAL 413890 (imaging CPU legs 0,4 at 512 GB, human go 2026-11-02)
- prompt: active/likelihood_lifecycle_p6c_gradient_runs.md
- epic: likelihood-lifecycle (phase 6c)
- compute: RAL submit checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ 97cdc88; human go per batch (batch 0 probe: go given 2026-11-01)
- tier: judge — merge mode: human /prm

## results-library-p2-completeness
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1752
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/results-library-p2-completeness
- repos:
  - PyAutoFit: feature/results-library-p2-completeness
  - autofit_workspace: feature/results-library-p2-completeness
- prompt: active/results_library_p2_completeness.md
- epic: results-library (phase 2)
- tier: judge — merge mode: human /prm

## rectangular-gradient-rtu-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/671
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-gradient-rtu-sparse
- repos:
  - PyAutoArray: feature/rectangular-gradient-rtu-sparse
- witness-harness: autolens_profiling read-only via p6c worktree (claimed by likelihood-lifecycle-p6c-gradient-walls; human ruled PyAutoArray-only 2026-11-02)
- prompt: active/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md
- tier: judge — merge mode: human /prm
