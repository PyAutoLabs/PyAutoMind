
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

## campaign-task-records-wait-loop
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1749
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/campaign-task-records-wait-loop
- repos:
  - PyAutoFit: feature/campaign-task-records-wait-loop
- prompt: active/campaign_task_records_and_wait_loop.md
- epic: hpc-campaign (phase 5a follow-up)
- heart-red-override: extended live by the human 2026-10-31 ("yes extend the override, go ahead"); RED reasons quoted on the issue; development only, merge via /prm
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

## sky-orientation-dr1-p1
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/113
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sky-orientation-dr1-p1
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sky-orientation-dr1-p1
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 1 of 5)
- heart-red-override: authorized live by the human 2026-10-31 ("I override for work on RED"); RED reasons quoted on the issue; development only, merge via /prm
- tier: judge — merge mode: human /prm

## ag-results-quick-fit-tags
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/266
- session: claude-code desktop (session 03dd203b)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ag-results-quick-fit-tags
- repos:
  - autogalaxy_workspace: feature/ag-results-quick-fit-tags
- corrective-red:
  - reason: "release validation FAILED (stage integrate)"
  - authorization: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/266#issuecomment-6542894772

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
