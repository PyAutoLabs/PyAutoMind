
## howtofit-runtime-guidance
- issue: https://github.com/PyAutoLabs/HowToFit/issues/72
- issued: 2026-10-17
- prompt: active/tutorial_4_runtime_claim.md
- session: Codex Work; current chat
- location: /workspace/scratch/a05dd794807b/HowToFit
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/74
- head: 01fea776af72ff9a84e492fabce27f74423e8bb3
- validation: Script/notebook prose-only diff verified; notebook regeneration succeeded. CI smoke failed because BlackJAX is absent in the install epilogue; fixed in HowToFit#75. Re-run after #75 merges.
- heart: STALE; release validation source moved since rehearsal; no release readiness claimed.
- next: Review PR and required CI; human /prm required.
- authorization: Four linked HowToFit teaching tasks; human Go on 2026-10-17; stop at PR review. HowToFit members coordinated sequentially on separate branches.
- repos:
  - HowToFit: feature/howtofit-runtime-guidance

## howtofit-ep-shared-centre
- issue: https://github.com/PyAutoLabs/HowToFit/issues/73
- issued: 2026-10-17
- prompt: active/tutorial_5_ep_shared_centre_never_assigned.md
- session: Codex Work; current chat
- location: /workspace/scratch/a05dd794807b/HowToFit
- status: workspace-shipped, blocked-CI
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/75
- head: 297b3e9eb2b170329daa9fd871cd7c91e91e46d8
- validation: Real sampling passes; shared x3 centre; each dataset and regression factor updated 5/5 sweeps, zero stale. One rejected marginal projection, no convergence claim. All 19 smoke scripts passed across initial run and missing-BlackJAX retry; final EP guard passed. Notebook/catalogue regenerated.
- heart: STALE; release validation source moved since rehearsal; no release readiness claimed.
- next: Fix smoke_install.sh to install the declared Nautilus dependency, then revalidate Python 3.12/3.13 and rerun /prm. No merge or rerun on this red-CI pass.
- decision: Review the explicit FWHM_i ~ Normal(m*i+c, 5 pixels) teaching assumption and m/c priors before merging. Also installs BlackJAX for existing gradient smoke scripts; #74 depends on this CI prerequisite.
- authorization: Four linked HowToFit teaching tasks; human Go on 2026-10-17; stop at PR review. HowToFit members coordinated sequentially on separate branches.
- repos:
  - HowToFit: feature/howtofit-ep-shared-centre

- ci-blocker: HowToFit run 39055282617; both 3.12 and 3.13 fail tutorial_6_gradients.py because nautilus is absent. Logs captured in PR #75 comment. Navigator and Tutorials Complete pass.
## cluster-pointsolver-robust-settings
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/436
- issued: 2026-10-17
- prompt: active/cluster_pointsolver_robust_settings_p1.md
- session: Claude Code (Fable 5.1); https://claude.ai/code/session_01MJFczsaH2vYuhFWLneD7F5
- status: workspace-dev
- classification: research (autolens_profiling only; Pulse campaign cluster-pointsolver phase 1), Consequence judge, Autonomy supervised; plan approved in chat 2026-10-17; compute per-job human authorization; no laptop timing
- decision 2026-10-17 (human, chat): A2744 rows use a labelled synthetic prior-median 191-component model (no Bergamini+23 best fit exists in the workspace); the independent oracle supplies ground truth; representativeness caveat stated in the note
- worktree: ~/Code/PyAutoLabs-wt/cluster-pointsolver-robust-settings
- repos:
  - autolens_profiling: feature/cluster-pointsolver-robust-settings

## prior-stable-test-ids
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1701
- issued: 2026-10-17
- prompt: active/xdist_collection_ids_unstable_in_test_prior.md
- status: library-shipped, awaiting-merge
- session: Codex Work; current chat (session ID unavailable)
- worktree: /workspace/scratch/211f457a3795-wt/prior-stable-test-ids
- authorization: User requested four linked dashboard tasks; sequential coordinated model/prior fixes on isolated branches; stop at PR review, no merge or release.
- heart: STALE; published feed unreachable, local reports missing.
- repos:
  - PyAutoFit: feature/prior-stable-test-ids

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1707
- head: c2f9f8bdd43001e94fffe0414cd10a010ac90df7
- validation: Final serial suite: 3702 passed, 120 skipped, 1 xfailed. Four-worker property tests: 170 passed; collection mismatch reproduced before repair. Full parallel execution still blocked by separately filed shared-output races.
- logs: /tmp/prior-full-final.log; /tmp/prior-focused-after.log
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- next: Human /prm after exact-head GitHub checks pass. No merge or release performed.

## function-config-priors
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1702
- issued: 2026-10-17
- prompt: active/model_function_cannot_resolve_config_priors.md
- status: library-shipped, awaiting-merge
- session: Codex Work; current chat (session ID unavailable)
- worktree: /workspace/scratch/211f457a3795-wt/function-config-priors
- authorization: User requested four linked dashboard tasks; sequential coordinated model/prior fixes on isolated branches; stop at PR review, no merge or release.
- heart: STALE; published feed unreachable, local reports missing.
- repos:
  - PyAutoFit: feature/function-config-priors

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1705
- head: c0fa0b6ee5500d69f3ba9d6dde598dbe1b59f157
- validation: Full serial suite: 3706 passed, 121 skipped, 1 xfailed; model subtree 204 passed. Configured/explicit function priors, frozen evaluation, missing-config errors, and class initializer behavior covered.
- logs: /tmp/function-config-priors-full.log; /tmp/function-model-tests.log
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- next: Human /prm after exact-head GitHub checks pass. No merge or release performed.

## prior-summary-ranges
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1703
- issued: 2026-10-17
- prompt: active/pyautofit_prior_model_summary_header_prints_wron.md
- status: library-shipped, awaiting-merge
- session: Codex Work; current chat (session ID unavailable)
- worktree: /workspace/scratch/211f457a3795-wt/prior-summary-ranges
- authorization: User requested four linked dashboard tasks; sequential coordinated model/prior fixes on isolated branches; stop at PR review, no merge or release.
- heart: STALE; published feed unreachable, local reports missing.
- repos:
  - PyAutoFit: feature/prior-summary-ranges

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1706
- head: ec8bbf6d91952f34bc2979381ec7528792c9efa1
- validation: Full serial suite: 3703 passed, 121 skipped, 1 xfailed; representation and GraphSpec 89 passed. Numeric suffixes, lexical fallback, padding, singletons, and integer gaps covered.
- logs: /tmp/prior-summary-ranges-full.log; /tmp/ranges-tests.log
- identifier-evidence: Free/fixed/mixed model hashes, search IDs and output paths equal unmodified main 99d714c71; no identifier code changed.
- next: Human /prm after exact-head GitHub checks pass. No merge or release performed.

## fixed-model-json
- constraint: Human confirmed 2026-10-17 that existing model/search unique IDs and output-folder names must not change; baseline hashes and exact output paths checked across all four branches.
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1704
- issued: 2026-10-17
- prompt: active/model_from_json_drops_zero_free_parameter_components.md
- status: library-shipped, awaiting-merge
- session: Codex Work; current chat (session ID unavailable)
- worktree: /workspace/scratch/211f457a3795-wt/fixed-model-json
- authorization: User requested four linked dashboard tasks; sequential coordinated model/prior fixes on isolated branches; stop at PR review, no merge or release.
- heart: STALE; published feed unreachable, local reports missing.
- repos:
  - PyAutoFit: feature/fixed-model-json

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1708
- head: b4b9e2e0af657ebacbb63394f96d6499361bc951
- validation: Final full serial suite 3704 passed, 120 skipped, 1 xfailed; affected model/graph/aggregator tests 305 passed. Initial five from_instance regressions repaired; legacy instance JSON behavior retained.
- identifier-evidence: Free/fixed/mixed baseline model hashes, search IDs and exact output paths unchanged; converted-instance JSON and hash also unchanged. JSON roundtrip preserves original persistent identifiers.
- witness-detail: GraphSpec comparison excludes process-local obj_id/prior_id counters (pre-existing JSON limitation); all semantic graph fields compared. No identifier algorithm edits.
- logs: /tmp/fixed-model-json-final.log; /tmp/json-repair.log
- next: Human /prm after exact-head GitHub checks; remove lens cookbook reload warning after library release. No merge or release performed.
