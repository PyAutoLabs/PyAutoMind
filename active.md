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

## point-source-search-nautilus-leaf
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/15
- issued: 2026-09-28
- prompt: active/point_source_search_nautilus_leaf.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-28; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-28 (workspace-only, no library edits)
- worktree: ~/Code/PyAutoLabs-wt/point-source-search-nautilus-leaf
- repos:
  - autolens_inference: feature/point-source-search-nautilus-leaf
- resume: "Branch pushed (2307eea), NO PR yet. Probe RAL job 366937 COMPLETED (seed 0: wall_s 56.6 s, 4,850 evals, per_call 4.72 us batched, likelihood_share 0.041% [single-basis 1.8%], all truth |dsigma|<0.74; row committed). Seeds 1-4 = RAL array 367140 (%1, euclid-ral-gpu-2). Next: sacct -j 367140; scp euclid_jump:/mnt/ral/jnightin/autolens_inference-wt-psleaf/results/searches/point_source/nautilus/simple/source_plane_solved/hpc_a100_jax_cpu_dense_fp64/search_seed{1..4}.{json,png} into the same path in the local worktree (+ hpc/batch_cpu/{output,error}/*367140* logs by hand); check each seed recovers truth; build_readme.py; wiki admission-bar entry (wiki/project/state.md); scripts/point_source/searches/README.md leaf note; ruff/pytest/check_submits; /ship_workspace to PR (Heart YELLOW ack: PyAutoMemory open PR 7d old; other YELLOW -> DRAFT); then remove RAL worktree: cd /mnt/ral/jnightin/autolens_inference && git worktree remove /mnt/ral/jnightin/autolens_inference-wt-psleaf"

## ep-checkin-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/50
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/51
- issued: 2026-09-30
- prompt: active/ep_checkin_cleanup_2026_09_30.md
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID a45b0125
- status: library-shipped, awaiting-merge (PyAutoCortex PR open; supervised, merge is human via /prm)
- autonomy: supervised (header); plan approved in-session 2026-09-30 (ledgers on Cortex main via cortex.py verbs + checkin --apply; projects.yaml de-dup + duplicate-key guard via PR; PyAutoFit read-only, fixes route through /intake)
- worktree: ~/Code/PyAutoLabs-wt/ep-checkin-cleanup
- repos:
  - PyAutoCortex: feature/ep-checkin-cleanup
- summary: Clear the 2026-09-30 EP Cortex check-in issues in order (stale open runs, stale Now sections, tripled projects.yaml, stranded euclid_dr1 ledger edit), then prepare each of the four EP projects' next submission or name its blocker; stop at the go/no-go table.
- heart-red-override: authorised by the live human in-session 2026-09-30 ~10:55 BST ("Override for all three (Recommended)") for PyAutoCortex#50 push + PR-open; RED reasons at the 10:51 tick: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoLens: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)"; branch gates passed: pytest 65 green, cortex check OK, ledger_merge → code

## linear-solver-accuracy-study
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/354
- issued: 2026-09-30
- prompt: active/raw_forward_pdip_nnls_early_stopping.md
- epic: linear-solver-programme
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 (phase 1: autolens_profiling only, no library edits)
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-accuracy-study
- repos:
  - autolens_profiling: feature/linear-solver-accuracy-study
- summary: Phase 1 of the linear-solver programme — a dedicated `scripts/lens/solver/` package in autolens_profiling (system corpus, solver-candidate registry, accuracy + early-stopping cells, README stats), a pre-registered rule, and a campaign page recording which raw-PDIP variant fixes the ~4 % amplitude bias while keeping 48/48 SLaM points converged. Library fix = phase 2 (own prompt, PyAutoArray).
- heart-red-hold: 2026-09-30 ship gate RED (PyAutoArray/PyAutoLens 2 behind origin; release validation FAILED stage integrate; workspace validation 1 timeout cloud#36404726969; manifest drift front-door tables) — none in autolens_profiling; human override/ack needed
- resume: "Phase 1 COMPLETE locally: branch feature/linear-solver-accuracy-study head 18a9b70 (5 commits), all gates green, NOT pushed, no PR (Heart RED at ship). Verdict: no drop-in candidate; post-hoc euclid latent: polish +7.5e-5 / tol 1e-5 +5.1e-4 / jaxnnls cap>50 -3e-8 all green. Next: human ack/override → /ship_workspace linear-solver-accuracy-study (PR body drafted on issue #354 comment); then /prm; then phase 2 draft/bug/autoarray/raw_pdip_forward_amplitude_bias_fix.md once PyAutoArray claim sparse-data-none-guard clears."

## ep-projection-exception
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1653
- issued: 2026-09-30
- prompt: active/ep_project_nonfinite_suff_stats_ic50_n50.md
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID a45b0125
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 (Plan Mode)
- heart-red-override: authorised by the live human in the Claude Code session 2026-09-30 ~10:55 BST ("Override for all three (Recommended)", offered for PyAutoCortex#50 and "for opening the two PyAutoFit tasks (issue + worktree + plan; no merge, no release)"); RED reasons at the 10:51 BST tick: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoLens: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)"; scope: issue + worktree + plan; PR-open permitted; no merge/release; plan approved in-session ~11:20 BST via Plan Mode
- parallel-claim: "PyAutoFit is also claimed by ep-moment-projection (registered in the same session, 2026-09-30). File sets disjoint (A: messages/abstract.py, mapper/prior/abstract.py, non_linear/result.py, graphical/expectation_propagation/optimiser.py:150-162, exc.py, test_autofit/messages/test_project_nonfinite.py, test_autofit/graphical/functionality/test_factor_failure_recovery.py; B: graphical/laplace/*, graphical/mean_field.py, graphical/declarative/factor/hierarchical.py, graphical/expectation_propagation/diagnostics.py:47, graphical/README.md, test_autofit/graphical/functionality/test_moment_projection.py). A ships first; B rebases. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/ep-projection-exception
- repos:
  - PyAutoFit: feature/ep-projection-exception
- summary: Replace the bare assert in AbstractMessage.project with ProjectionException(ValueError) naming the non-finite input (prior id + path context added at Prior.project / Result.projected_model); list it in factor_step's recovery tuple so one bad projection degrades to the previous message instead of killing the EP run; tests for both.

## ep-moment-projection
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1654
- issued: 2026-09-30
- prompt: active/ep_hierarchical_scatter_moment_matching.md
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID a45b0125
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 (Plan Mode); default projection stays "mode"
- heart-red-override: authorised by the live human in the Claude Code session 2026-09-30 ~10:55 BST ("Override for all three (Recommended)", offered for PyAutoCortex#50 and "for opening the two PyAutoFit tasks (issue + worktree + plan; no merge, no release)"); RED reasons at the 10:51 BST tick: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoLens: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)"; scope: issue + worktree + plan; PR-open permitted; no merge/release; plan approved in-session ~11:20 BST via Plan Mode
- parallel-claim: "PyAutoFit is also claimed by ep-projection-exception (#1653, registered in the same session, 2026-09-30). File sets disjoint (B: graphical/laplace/*, graphical/mean_field.py, graphical/declarative/factor/hierarchical.py, graphical/expectation_propagation/diagnostics.py:47, graphical/README.md, test_autofit/graphical/functionality/test_moment_projection.py; A: messages/abstract.py, mapper/prior/abstract.py, non_linear/result.py, graphical/expectation_propagation/optimiser.py:150-162, exc.py, test_autofit/messages/test_project_nonfinite.py, test_autofit/graphical/functionality/test_factor_failure_recovery.py). A ships first; B rebases on it. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/ep-moment-projection
- repos:
  - PyAutoFit: feature/ep-moment-projection
- summary: LaplaceOptimiser(projection="mode"|"moments"): nested quadrature (outer Gauss–Legendre over the scale variable on its support, inner conditional Laplace) ported from the analytic_ep_minimal referee; MeanField.from_weighted_nodes; SUCCESS/BAD_PROJECTION/FAILURE semantics; tests; phase 2 = autofit_workspace_test un-park via start_workspace after merge.

## streaming-p1-array-free-dataset
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/592
- issued: 2026-09-30
- prompt: active/streaming_p1_array_free_dataset.md
- epic: streaming-visibilities (phase 1 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/streaming-p1-array-free-dataset
- autonomy: supervised (header); phase plan + design decisions (a)-(e) approved in-session 2026-09-30
- repos:
  - PyAutoArray: feature/streaming-p1-array-free-dataset
