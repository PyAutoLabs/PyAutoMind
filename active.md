
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

## ral-category-paths-autolens-profiling
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
- issued: 2026-10-18
- prompt: active/ral_category_paths_autolens_profiling.md
- session: Claude Code (Opus 5.5)
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/437
- heart-red-override:
  - authorization: human, live chat 2026-10-18, "I authorize override" (this task, Cortex#67); development shipping only, merge = separate human /prm
  - red-reasons: PyAutoFit: CI failure — https://api.github.com/repos/PyAutoLabs/PyAutoFit/actions/runs/39111874604; PyAutoFit: PyAutoFit: CI failure; PyAutoFit/Tests: failure; PyAutoFit/workflows/Tests: failure; PyAutoArray/Tests: red; PyAutoArray/Tests: red; PyAutoFit/Tests: red; PyAutoFit/Tests: red; PyAutoFit/Tests: red; PyAutoFit/Tests: red; autofit_workspace_test/Smoke Tests: red; autogalaxy_workspace_test/Smoke Tests: red; autolens_workspace_test/Smoke Tests: red; CI wall-clock: 27 gates · slowest PyAutoBrain Nightly Release 90m · 9 hang events; PyAutoFit: PyAutoFit: CI failure; PyAutoArray: red; autolens_inference: red; autolens_profiling: red; Worktree drift: 5 orphan / 0 missing / 4 dirty; euclid_strong_lens_modeling_pipeline: red
  - passed-gates: Witness empty; bash -n + py_compile; lint.yml steps local PASS; pytest 1457 passed 6 skipped; author diff review path-only; smoke n/a
- classification: refactor (autolens_profiling only), Consequence judge, Autonomy supervised; plan approved in chat 2026-10-18; human Heart-RED override 2026-10-18 recorded on #67
- parallel-worktree: human-approved 2026-10-18 beside cluster-pointsolver-robust-settings (disjoint files: 29 path files vs that branch's 9)
- worktree: ~/Code/PyAutoLabs-wt/ral-category-paths-autolens-profiling
- repos:
  - autolens_profiling: feature/ral-category-paths-autolens-profiling
