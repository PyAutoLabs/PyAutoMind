# Active Tasks

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

## benchmark-forward-model-consistency
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/142
- issued: 2026-10-02
- prompt: active/benchmark_forward_model_consistency.md
- session: Codex; session ID unavailable
- status: awaiting-merge
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/benchmark-forward-model-consistency
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/146
- commit: cfeedf5bcb3e10e698642a8da5a92c855676cefb
- validation: Final targeted 59 passed / 0 failed; earlier full suite 137 passed / 0 failed / 1 skipped. API/freeze and seven FITS byte-determinism checks pass. Three actual Claude calibration scores 0/0/0; failures retained, first timing confounded by test overlap.
- resume: PR open with pending-release label; human /prm after CI. Shared worktree now proceeds to other bundle branches. Logs in .worktrees/assistant/scratch/forward-*.log. No merge authorization.

## benchmark-positions-inference
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/143
- issued: 2026-10-02
- prompt: active/benchmark_positions_initialised_inference.md
- session: Codex; session ID unavailable
- status: awaiting-input
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/benchmark-positions-inference
- commit: a22696b
- validation: 42 final targeted passed / 0 failed; freeze-check passed; 3/3 recorded scores reproduce after cleanup. Genuine reference ESS6120.8, 58,200 calls. Calibration 0/0/0 (two no-result timeouts, one scientific success exceeding compute budget).
- resume: Implementation and evidence committed, clean tracked tree. PR body ready at .worktrees/assistant/scratch/positions-pr.md. Await live acknowledgment of Heart YELLOW generated organism-map drift, generated public-front-door drift, and missing release rehearsal; then push feature/benchmark-positions-inference and open its PR. No merge authorization. User considering quicker wrap leaving bootstrap/Colab queued.

## bootstrap-smoke-codex
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/144
- issued: 2026-10-02
- prompt: active/bootstrap_smoke_codex_and_bench_pr.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/bootstrap-smoke-codex
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## colab-refinement-throughout
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/145
- issued: 2026-10-02
- prompt: active/colab_refinement_throughout.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/colab-refinement-throughout
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## pointsolver-extent-sanity-check
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/763
- issued: 2026-10-02
- prompt: active/pointsolver_extent_sanity_check.md
- epic: point-source-cpu-speed
- session: Codex; session ID unavailable
- status: library-merged, awaiting-release
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pointsolver-extent-sanity-check
- repos:
  - PyAutoLens: feature/pointsolver-extent-sanity-check
  - autolens_workspace_test: feature/pointsolver-extent-sanity-check
  - autolens_profiling: feature/pointsolver-extent-sanity-check (campaign ledger only)
- coordination: Human approved the plan and concurrent disjoint workspace-test changes on 2026-10-02. Workspace scope is new scripts/point_source/jax_likelihood/solver_extent.py and its smoke list/profile entry; preserve all other tasks' edits.
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/764
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/338
- campaign-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/363
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/764
- release-gate: PyAutoLens
- resume: prm verified all 8 exact-head CI jobs green and Heart not frozen. PyAutoLens#764 merged 0dd420877; profiling#363 merged 134695058. Workspace#338 remains open/green behind its PyAutoLens release gate; latest release 2026.10.2.1 predates this merge and no fetched tag contains it. After a release contains #764, resume prm for workspace merge and full close-out. Issue/prompt/claims/worktrees retained; no second phase issued.

## evaluation-grid-cap-field
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/645
- issued: 2026-10-02
- prompt: active/evaluation_grid_cap_preserves_field.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: awaiting-merge, workspace-release-gated
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/evaluation-grid-cap-field
- repos:
  - PyAutoGalaxy: feature/evaluation-grid-cap-field
  - autolens_workspace_test: feature/evaluation-grid-cap-field
  - autolens_profiling: feature/evaluation-grid-cap-field
- coordination: Human approved plan and separate-scope concurrency on 2026-10-02 alongside Galaxy docs, workspace numerical-audit and point-solver ledger tasks. Restrict edits to evaluation_grid, new operate tests, critical_curves CI and critical_curves campaign ledger/wiki. Prior phase-3a claim is released in its completion record; retained evidence worktree is not an active claim.
- resume: Phase 3b shipped: Galaxy#646 f19a3377; profiling#365 d8a46c3; workspace#343 fcd6bd5 is DRAFT until library fix is available to CI dependencies. Library-first gate; no release performed or phase-3b merge authorized. All local checks pass. Resume /prm for library/research when green, release-dependent workspace afterward. No further phase issued.

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

## heart-publication-coverage
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/270
- issued: 2026-10-02
- prompt: active/heart_publication_coverage.md
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-publication-coverage
- coordination: Human approved concurrent isolated Heart work alongside pyautopulse-organ-row; that PR merged before worktree creation.
- repos:
  - PyAutoHeart: feature/heart-publication-coverage
- validation: 1177 Heart tests passed; tenant firewall passed; real snapshot round trip exported 16 monitoring families.
- heart-reasons:
  - manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml

- heart-ack: Human acknowledged both recorded YELLOW reasons on 2026-10-02: "do that i authorise"; unchanged at shipping, no RED blockers.
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/271
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/271
- commit: 0c1b7d6e98a620082e6f47c133db438e04fb51f2
- resume: PR open with pending-release label; Python 3.12 and 3.13 CI in progress at handoff. Run /prm on human authorization once green. No workspace API impact; scientific smoke not applicable.

## pyautopulse-organ-skeleton
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/1
- issued: 2026-10-02
- prompt: active/profiling_organ_p2_skeleton_registry_reader_board.md
- epic: profiling-organ-birth
- session: Claude Code CLI (Fable 5.1); session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/pyautopulse-organ-skeleton
- repos:
  - PyAutoPulse: feature/pyautopulse-organ-skeleton
  - PyAutoBrain: feature/pyautopulse-organ-skeleton
- resume: Phase 2 of profiling-organ-birth. Human 2026-10-02: one task, two PRs (PyAutoPulse first, Brain after); plan approved on the issue; Brain `boards: pulse` lands here. Heart YELLOW 85 at the door (Cortex checkout drift owned by another session; .github table; no rehearsal). Implementation delegated to Opus in the worktree; ship via /ship_library, end at PR-open; human enables Pages on PyAutoPulse; merge /prm.
