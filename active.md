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

## critical-curves-dispatch-audit
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/337
- issued: 2026-10-02
- prompt: active/critical_curves_dispatch_audit.md
- epic: cluster-strong-lensing
- session: Codex, 2026-10-02
- status: workspace-dev, blocked-at-ship-gate
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/critical-curves-dispatch-audit
- repos:
  - autolens_workspace_test: feature/critical-curves-dispatch-audit
  - autolens_profiling: feature/critical-curves-dispatch-audit
- coordination: Human authorized concurrent separate scope alongside point-source-search-nautilus-leaf / profiling#361 on 2026-10-02.
- resume: Phase 3a research/JSON/PNG/wiki and independent CI example implemented, uncommitted in both feature worktrees. Profiling 1002 passed/5 skipped; lint/docs/artifact validation green. Refreshed Heart RED: PyAutoFit/PyAutoGalaxy/PyAutoLens each 1 commit behind origin, plus manifest YELLOW. Smoke retry passed first five then stopped at gate; remainder unrun. Resolve Heart, complete full smoke, ship two companion PRs for #337. Raw workers/logs/PR drafts in scratch. No successor issue, phase completion or merge authorization.

- heart-ack: "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- authorization: Human answered "Acknowledge YELLOW and proceed" on 2026-10-02; ship phase-3a PRs after smoke, merge under this turn's explicit /prm when all CI passes. No release authority.

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

## mesh-interpolator-numerics-audit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/603
- issued: 2026-10-02
- prompt: active/final_numerics_audit_of_every_mesh_interpolator.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/mesh-interpolator-numerics-audit
  - autolens_workspace_test: feature/mesh-interpolator-numerics-audit
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

- heart-ack:
  - "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- heart-stale: "release validation incomplete: no rehearsal for current source"
- authorization: Human acknowledged exact Heart YELLOW reason and authorized development PR shipping for this bundle; no release or merge, 2026-10-02.

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

## pyautopulse-organ-row
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/463
- issued: 2026-10-02
- prompt: active/profiling_organ_p0_name_row_and_boundaries.md
- epic: profiling-organ-birth
- session: Claude Code CLI (Fable 5.1); session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/pyautopulse-organ-row
- repos:
  - PyAutoMind: feature/pyautopulse-organ-row
  - PyAutoBrain: feature/pyautopulse-organ-row
  - PyAutoHeart: feature/pyautopulse-organ-row
  - PyAutoHands: feature/pyautopulse-organ-row
  - pyautolabs.github.io: feature/pyautopulse-organ-row
  - PyAutoCortex: feature/pyautopulse-organ-row
  - PyAutoNerves: feature/pyautopulse-organ-row
  - PyAutoGut: feature/pyautopulse-organ-row
  - PyAutoScientist: feature/pyautopulse-organ-row
  - PyAutoEyes: feature/pyautopulse-organ-row
- resume: Phase 0 of profiling-organ-birth. Human decisions 2026-10-02: PyAutoPulse, organ key `pulse`, organ row AFTER Hands before Nerves, `boards:` entry deferred to phase 2, plan approved. Repo PyAutoLabs/PyAutoPulse created (public, empty). Next: /start_library then implement per issue #463; PRs Mind → Brain → Heart → Hands → hub (+ map-block PRs Cortex/Nerves/Gut/Scientist); merge human via /prm.

## pointsolver-extent-sanity-check
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/763
- issued: 2026-10-02
- prompt: active/pointsolver_extent_sanity_check.md
- epic: point-source-cpu-speed
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
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
- resume: Human acknowledged Heart YELLOW (85) via “prm and continue”. Three PRs opened; CI pending at judgment (library docs + Python 3.12/3.13/no-JAX, workspace Python 3.12/3.13, profiling lint). No merge. Next prm must judge every exact-head run/leg, then library-first and release gates. Local evidence: 820 passed/1 xfailed, 27 focused tests, 33 distinct smoke passes after documented recovery. Keep this sole bounded phase active; no next phase or solver default changes.
