
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## rectangular-28sq-profiling-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-28sq-profiling-rows
- repos:
  - autolens_inference: feature/rectangular-28sq-profiling-rows
- released-claims: autolens_profiling (#470 merged a1a4ccf1), PyAutoPulse (#80 merged 5474e3cb) — branches kept in the worktree until close-out
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/49 OPEN 2026-10-27 (size_match 32/0)
- prompt: active/rectangular_28sq_profiling_rows.md
- epic: likelihood-lifecycle
- heart-red-override: authorized by live human 2026-10-26 "I approve of the override" (this task incl. RAL jobs); reasons + gates recorded at ship
- scope-add: HUMAN 2026-10-26 chose "Yes, small Pulse PR first" (option text: "Same RED override extended to it. Ships before the profiling rows.") — PyAutoPulse one-current-per-key adds regime
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/80 MERGED 2026-10-26 5474e3cb via human /prm (regime in @3 one-current key)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/470 MERGED 2026-10-27 a1a4ccf1 via human /prm (rect28 rows, RAL 413044/413046 8/8); task stays open — NEXT autolens_inference size_match leg (branch has no commits yet); witness gap jax_cpu_dense + light_fixed unmeasured

## likelihood-lifecycle-p2d-galaxy-group
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/473
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2d-galaxy-group
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2d-galaxy-group
- prompt: active/likelihood_lifecycle_p2d_multi_galaxy_group_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2e-cluster
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/474
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2e-cluster
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2e-cluster
- prompt: active/likelihood_lifecycle_p2e_cluster_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2f-dataset-datacube
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/475
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2f-dataset-datacube
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2f-dataset-datacube
- prompt: active/likelihood_lifecycle_p2f_multi_dataset_datacube_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2g-weak
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/476
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2g-weak
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2g-weak
- prompt: active/likelihood_lifecycle_p2g_weak_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag; ends at a DRAFT PR for human review)
- parallel-claim: HUMAN 2026-10-28 "also do the work to set up the other dataset types" — parallel worktree stacked on #471 (80bbb028)
- batch-go: NONE — human: "leave this as something I then review before we do RAL runs"

## likelihood-lifecycle-p2c-point-source
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/472
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2c-point-source
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2c-point-source
- prompt: active/likelihood_lifecycle_p2c_point_source_campaign.md
- epic: likelihood-lifecycle
- autonomy: --auto (supervised → decide-and-flag, ends at PR-open; judge → human /prm)
- parallel-claim: HUMAN 2026-10-28 "yeah do it, run in auto mode" — parallel worktree beside 2b, stacked on #471 (80bbb028); disjoint files except regenerated catalogue/coverage
- batch-go: HUMAN 2026-10-28 "yeah do it" = go for the 2c RAL batch (ral CPU + A100); never touch 2b 413161/413191

## likelihood-lifecycle-p2b-interferometer
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/469
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2b-interferometer
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2b-interferometer
- prompt: active/likelihood_lifecycle_p2b_interferometer_campaign.md
- epic: likelihood-lifecycle
- heart-red-override: live human 2026-10-26 "Yes, authorise for 2b" (PRs + planned RAL batches)
- batch-go: HUMAN 2026-10-27 "do the next tasks to the point interferometry is hopefully running" = go for batch 0
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/471 OPEN 2026-10-27 (PR A, dff89226; Heart GREEN; judge → human /prm)
- batch0: chained on RAL 2026-10-27 (scratch/p2b_batch0_submit.log; CPU 0-13 + refs 0-1 on ral, A100 0-9%2) from branch head dff89226

## mesh-magnification-areas
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/659
- issued: 2026-10-28
- session: Claude Code (Opus 5.5); https://claude.ai/code/session_016nhQ8NkVvJhhqNSibeGcBQ
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/mesh-magnification-areas
- repos:
  - PyAutoArray: feature/mesh-magnification-areas
  - autolens_workspace_test: feature/mesh-magnification-areas
- prompt: active/mesh_magnification_areas.md
- epic: cluster-strong-lensing (Source & Cluster arc phase 4a)
- autonomy: --auto launched by human 2026-10-28; effective supervised → decide-and-flag, ends at PR-open; judge → human /prm

## compact-colab-setup
- heart-red-override:
  - authorization: "I authorize you to continue despite RED" (2026-10-28; development only, no merge/release)
  - reason: PyAutoArray: 4 uncommitted source change(s)
  - reason: PyAutoGalaxy: 9 commit(s) behind origin
  - reason: PyAutoLens: 7 commit(s) behind origin
  - reason: release validation stale: source moved since rehearsal (PyAutoGalaxy, PyAutoLens)
- checkpoint: Hands PR328 (584 tests pass), Fit workspace PR178 (8 scripts + 2 notebooks pass); six families regenerated; remaining smokes and assistant pinned-runtime validation underway
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/327
- issued: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/328
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/178
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/compact-colab-setup
- repos:
  - PyAutoHands: feature/compact-colab-setup
  - autolens_workspace: feature/compact-colab-setup
  - autogalaxy_workspace: feature/compact-colab-setup
  - autolens_assistant: feature/compact-colab-setup
  - autofit_workspace: feature/compact-colab-setup
  - HowToFit: feature/compact-colab-setup
  - HowToGalaxy: feature/compact-colab-setup
  - HowToLens: feature/compact-colab-setup

## results-library-p0-integrity
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1734
- issued: 2026-10-28
- epic: results-library (phase 0, shared with hpc-campaign)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/results-library-p0-integrity
- repos:
  - PyAutoFit: feature/results-library-p0-integrity

## hpc-campaign-p1-status-record
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1735
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/206
- issued: 2026-10-28
- epic: hpc-campaign (phase 1; merges after results-library PR 0a)
- session: Claude Code CLI (Opus 5.5) session_016nhQ8N4RdvbZz9cstLYtNF
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/hpc-campaign-p1-status-record
- repos:
  - PyAutoFit: feature/hpc-campaign-p1-status-record
  - PyAutoNerves: feature/hpc-campaign-p1-status-record
