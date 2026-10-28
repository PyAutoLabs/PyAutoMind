
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

## lenstwin-p3-stellar-dark
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/805
- issued: 2026-10-28
- session: Claude Code remote (web) session_016nhQ8NtZ6QtuqxKKAnhhdg
- location: remote session clone /home/user/pyautolens on feature/lenstwin-p3-stellar-dark (from origin/main 9a85d32); no task worktree
- status: library-dev
- epic: lenstwin (phase 3; ledger draft/feature/autolens/lenstwin_epic.md)
- prompt: active/lenstwin_p3_stellar_dark_transform.md
- repos:
  - PyAutoLens: feature/lenstwin-p3-stellar-dark
- summary: |
    Phase 3 of lenstwin issued 2026-10-28 via /start_dev → /create_issue: PyAutoLens#805
    (3A Einstein-radius aperture + `transform.ReplaceTotalMassWithStellarPlusDark`; 3B
    `al.twins.compare` / `compare_to_data` + `aplt.subplot_twin_comparison`). R3/R4/R6 ruled.
    Feature Agent suggested splitting; kept one issue/PR per the epic's one-issue-per-repo-per-phase
    rule (0B was the same size). Consequence: judge (human /prm). Implementation on Opus workers.
