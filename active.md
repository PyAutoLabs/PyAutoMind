# Active Tasks

## heart-dashboard-remaining
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/274
- issued: 2026-10-04
- prompt: active/restore_dashboard_green.md
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge; native-confirmed dependency repair prepared
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/restore-dashboard-green
- repos:
  - PyAutoHeart: feature/restore-dashboard-green
- heart-red-override:
  - authorization: I authorize development investigation and repair despite the current RED reason above. Follow start-dev and record the task-specific authorization wherever required.
  - reasons: "release validation FAILED (stage integrate)"
  - scope: Heart dashboard repair #274 and bounded timeout investigation; applicable tests and independent review remain required; human /prm only.
  - passed-gates: 1222 full Heart tests; YAML/firewall/whitespace; independent Sol CLEAN; exact-wheel candidate 3/3. Diagnostic comparison remains inconclusive, not release validation.
- authorization: Human approved phased dashboard repair plan on 2026-10-04; tier undeclared, merge via human /prm. Preserve unfinished work and scientific evidence.
- diagnostic-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/280
- diagnostic-head: f5bad35e46f0a4b6264f5cd240ee156d28c1f26e
- diagnostic-validation: 1222 full Heart tests PASS; YAML/firewall/whitespace PASS; independent Sol CLEAN including41 focused tests; native replay37205459198 reproduces LAPACK deadlock; comparison37206724174 inconclusive (3 controls/3 candidates pass); no release clearance.
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/275
- completed-phase: PR279 merged at3d86fd8; complete/2026/10/retired-repo-sidecars.md. Both CI legs passed, issue278 closed.
- validation: Heart 1181 tests passed; focused 20 passed (4 regression cases failed before fix); independent review CLEAN; Python 3.12/3.13 CI green at 1c9b924.
- resume: PR280 f5bad35 repairs old JAX bounds to>=0.11.2,<0.12 across3 recipes. Native control replay deadlocked in LAPACK; source removes captured path,3 exact-wheel candidate passes. Same-run comparison honestly inconclusive. Human /prm only; final-head CI must be judged. Canonical RED60 integratefail and monitoring RED33 preserved/published; timings refreshed, science/worktrees and Anthropic blocker untouched. See final continuation in prompt.

## vis-lp-inspection-bundle
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/102
- issued: 2026-09-22
- session: claude (Fable CLI, 2026-09-23; resumed from Codex 2026-09-22)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Implemented + committed locally as c6b514d on feature/vis-lp-inspection-bundle (133 tests green, not pushed). Human reviews diff (scratchpad part1_diff.txt) before ship_workspace; then sync tooling to the euclid_dr1 science clone/RAL and submit the 4,922-tile vis_lp-only bundle (OUTPUT_DIR=dr1_full, INITIAL_SEARCH_NAME=vis_lp, DATASET_NAMES_PATH=all, TAR_TO set) as a Cortex run.

## evaluation-grid-cap-field
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/645
- issued: 2026-10-02
- prompt: active/evaluation_grid_cap_preserves_field.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: library-merged, workspace-release-gated
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/evaluation-grid-cap-field
- repos:
  - PyAutoGalaxy: feature/evaluation-grid-cap-field
  - autolens_workspace_test: feature/evaluation-grid-cap-field
- coordination: Human approved plan and separate-scope concurrency on 2026-10-02 alongside Galaxy docs, workspace numerical-audit and point-solver ledger tasks. Restrict edits to evaluation_grid, new operate tests, critical_curves CI and critical_curves campaign ledger/wiki. Prior phase-3a claim is released in its completion record; retained evidence worktree is not an active claim.
- resume: 2026-10-02 /prm merged Galaxy#646 (2e36de4e) and profiling#365 (9d0b1317); autolens_profiling claim released (branch merged, Pulse tasks may proceed there). workspace#343 fcd6bd5 stays DRAFT until PyAutoGalaxy is released with the fix; then mark ready and /prm it to close the task. No release performed. No further phase issued.

- heart-ack:
  - "manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- authorization: Human answered "Acknowledge both and ship" for phase 3b on 2026-10-02. No release authority; no additional phase queued.
- validation: Before fix six geometry failures/two compatibility passes; after fix 49 focused and 1315 full Galaxy tests pass. Real-decorator probe yields 1000x1000 at 0.06 arcsec with pixel-centre bounds ±29.97. Companion CI example passes standalone; full workspace smoke in progress.

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- library-commit: f19a3377; 1315 full and 49 focused tests pass. Linked CI witness and profiling ledger/wiki prepared; full workspace smoke in progress.
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/343
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/365
- final-validation: Galaxy 1315 passed; focused 49 passed; full companion smoke 33/33 in 501.91s (changed example 2.2s). Galaxy exact-head CI all green; new companion CI pending. Wiki/results-layout and whitespace checks pass. No raw phase-3a evidence changed.
