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
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/benchmark-positions-inference
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

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

## over-sample-snr-helper
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/602
- issued: 2026-10-02
- prompt: active/over_sample_size_via_snr_from.md
- session: Codex GPT-6; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/over-sample-snr-helper
  - PyAutoGalaxy: feature/over-sample-snr-helper
- resume: Bundle autoarray — bundle 1; plan and branch approved 2026-10-02. One execution delegate per member; sequential shared worktrees; linked companion PRs authorized. Preserve unregistered sparse-operator-oversampling-cache worktree. Parent owns lifecycle and shipping. No merge authorization.

- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/606
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/644
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/606
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/644
- validation: Array 1922 passed, Galaxy 1307 passed, focused 23 passed; downstream API/equivalence passed; Heart GREEN. Logs in shared worktree scratch/snr-helper. Commits 54c360be / ba7c70dc. PRs open, merge remains human. Shared Array worktree advanced to next member.

- heart-ack:
  - "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- heart-stale: "release validation incomplete: no rehearsal for current source"
- authorization: Human acknowledged exact Heart YELLOW reason and authorized development PR shipping for this bundle; no release or merge, 2026-10-02.

- ci: Exact-head snapshot 2026-10-02: all required checks green on both linked PRs; open, awaiting human merge.

## mesh-interpolator-numerics-audit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/603
- issued: 2026-10-02
- prompt: active/final_numerics_audit_of_every_mesh_interpolator.md
- session: Codex GPT-6; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/mesh-interpolator-numerics-audit
  - autolens_workspace_test: feature/mesh-interpolator-numerics-audit
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

- heart-ack:
  - "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- heart-stale: "release validation incomplete: no rehearsal for current source"
- authorization: Human acknowledged exact Heart YELLOW reason and authorized development PR shipping for this bundle; no release or merge, 2026-10-02.

- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/611
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/342
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/611
- validation: Full snapshot 1940 passed/1 strict xfail/0 unexpected failures; final interpolation suite 90 passed/4 strict xfails/0 unexpected failures; smoke1 passed/0 failed; all exit0. Commits509fb814/a22ff41. Final added tests covered by final focused suite; production unchanged. Report scripts/imaging/mesh_interpolator_source_recovery.md; logs scratch/numerics-audit. Follow-up defects609/610 queued separately. Exact-head CI snapshot: Array611 three legs in progress; workspace342 no checks reported yet. No merge authorization. Library-first order; no new runtime API release needed by companion script.

## fit-util-masked-division
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/604
- issued: 2026-10-02
- prompt: active/fit_util_masked_division_grad_nan.md
- session: Codex GPT-6; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/fit-util-masked-division
  - autolens_workspace_test: feature/fit-util-masked-division
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/607
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/607
- validation: Full Array serial 1924 passed, exit 0; focused 33 passed; 3 targeted smoke checks passed (imaging unchanged retry after timeout). Logs scratch/masked-division.

- heart-ack:
  - "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- heart-stale: "release validation incomplete: no rehearsal for current source"
- authorization: Human acknowledged exact Heart YELLOW reason and authorized development PR shipping for this bundle; no release or merge, 2026-10-02.
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/340
- release-gate: PyAutoArray
- resume-shipping: Library e5e05217 / workspace95d696e, both ready PRs. Provenance-correct repeat fit-util/imaging smoke2pass exit0; earlier interferometer smoke passed. Full suite1924passed exit0 verified against bundle. Remaining human library-first merge/release. Scratch stash9b85ea65282820b33e73f5d4e360422fda43a3da retained recoverably; contents now committed. Shared worktree advanced to audit.

- ci: Exact-head snapshot 2026-10-02: all required checks green on both linked PRs; open, awaiting human merge.

## mesh-geometry-transformed-areas
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/605
- issued: 2026-10-02
- prompt: active/mesh_geometry_areas_transformed_adapt_image_indexerror.md
- session: Codex GPT-6; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/mesh-geometry-transformed-areas
  - autolens_workspace_test: feature/mesh-geometry-transformed-areas
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

- heart-ack:
  - "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- heart-stale: "release validation incomplete: no rehearsal for current source"
- authorization: Human acknowledged exact Heart YELLOW reason and authorized development PR shipping for this bundle; no release or merge, 2026-10-02.

- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/608
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/339
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/608
- release-gate: PyAutoArray
- validation: Full 1919 passed, focused34 passed, smoke2 passed, exit0; provenance verified. Logs scratch/mesh-geometry. Commits20ed237a/bdd698c. Explicit guard-cell geometry replaces obsolete uniform-partition expectations; standalone helper unchanged. Shared worktree advances to other bundle members. Awaiting human library-first merge/release.

- ci: Exact-head snapshot 2026-10-02: all required checks green on both linked PRs; open, awaiting human merge.

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
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/evaluation-grid-cap-field
- repos:
  - PyAutoGalaxy: feature/evaluation-grid-cap-field
  - autolens_workspace_test: feature/evaluation-grid-cap-field
  - autolens_profiling: feature/evaluation-grid-cap-field
- coordination: Human approved plan and separate-scope concurrency on 2026-10-02 alongside Galaxy docs, workspace numerical-audit and point-solver ledger tasks. Restrict edits to evaluation_grid, new operate tests, critical_curves CI and critical_curves campaign ledger/wiki. Prior phase-3a claim is released in its completion record; retained evidence worktree is not an active claim.
- resume: Approved effective Zoom2D footprint/centre and conservative subpixel rounding contract. Reproduce witness, implement bounded dimensional cap fix, test and ship library first; no engine/default/mask-support changes. One issued successor only.
