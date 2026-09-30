# Active Tasks

## interferometer-decision-matrix
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/356
- issued: 2026-09-30
- prompt: active/interferometer_decision_matrix.md
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-30
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 via Plan Mode (workspace-only, no library edits)
- parallel-claim: "autolens_profiling is also claimed by raw-pdip-forward-polish (workspace-pending). File sets disjoint (this task: instruments/interferometer.py, new hpc/batch_{cpu,gpu}/submit_breakdown_interferometer_*_{radius_gaps,sdp81}_*, new results/breakdown/interferometer/** JSONs, results/notes/interferometer_likelihood_decision_matrix_2026_09.md, wiki/campaigns/interferometer_likelihood.md, wiki/index.md row, results/README.md Campaign findings paragraph; raw-pdip: results/notes/linear_solver_accuracy_2026_09.md, wiki/campaigns/linear_solver_accuracy.md, euclid_latent.py). Whichever ships second merges results/README.md. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/interferometer-decision-matrix
- repos:
  - autolens_profiling: feature/interferometer-decision-matrix
- resume: "Issued; next start_workspace (worktree), then delegated execution: sdp81 preset, RAL CPU gap array + sdp81 CPU/A100 jobs, note."

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

## raw-pdip-forward-polish
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/594
- issued: 2026-09-30
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/595
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/595
- prompt: active/raw_pdip_forward_amplitude_bias_fix.md
- epic: linear-solver-programme
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID unavailable
- status: workspace-dev (library merged: PyAutoArray#595, pending release)
- autonomy: supervised (header); plan approved in-session 2026-09-30 via Plan Mode (forward polish = the #573 mechanism returned as the forward value; regression fixture 8 #571 systems + euclid vis_lp with fnnls x_ref; gates on inactive-column/total/source flux ≤ 1e-3, not amp_rel_max)
- parallel-claim: "PyAutoArray is also claimed by streaming-p1-array-free-dataset (active). File sets disjoint (this task: autoarray/util/jax_nnls.py, autoarray/config/general.yaml, autoarray/settings.py docstring, autoarray/inversion/inversion/inversion_util.py docstring, test_autoarray/inversion/inversion/{test_nnls_raw_forward_amplitude.py,files/mge_solver_reference_systems.npz,files/README.md}; streaming-p1: autoarray/dataset/**, autoarray/fit/fit_interferometer.py, autoarray/inversion/inversion/interferometer/**). Whichever ships second rebases. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/raw-pdip-forward-polish
- repos:
  - PyAutoArray: feature/raw-pdip-forward-polish
  - autolens_profiling: feature/raw-pdip-forward-polish
- summary: Return the #573 polished iterate (≤ 10 tight warm-started Jacobi-system PDIP iterations) as the raw-forward PDIP forward value in both the custom_vjp forward and the primal, so jit/grad/eager agree; new amplitude regression test over the phase-1 corpus (8 #571 + euclid, fnnls reference) red on d4298445; euclid latent jit test then passes on library main with no override; downstream autolens_profiling ledger row after the library merge.
- heart-red-override: authorised by the live human in the Claude Code session 2026-09-30 ("ok do phase 2" launched the task; at the ship gate the human pushed feature/raw-pdip-forward-polish directly ~16:35 BST after the auto-mode classifier denied the agent push); Heart at the 16:25 BST gate: RED "release validation FAILED (stage integrate)"; YELLOW "workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)", "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"; none in PyAutoArray; scope: push + pending-release PR #595; merge only via /prm on all-green required checks; no release
- resume: "Library phase DONE: PyAutoArray#595 MERGED 2026-09-30 (merge 7a89e19a0, head 42c52358) via /prm on green CI; pending release. Workspace phase NEXT in ~/Code/PyAutoLabs-wt/raw-pdip-forward-polish/autolens_profiling (branch feature/raw-pdip-forward-polish, 4 uncommitted re-run files that overwrote the v2026.8.17.1 stamp in place — pre-fix copies in git HEAD): (1) re-base scripts/lens/solver/euclid_latent.py validation leg from pre-fix jit 3.511093374 to eager 3.3198794874 (fixed pdip_raw = 3.320127537, +7.47e-5) and re-run it; (2) decide the artefact label for post-fix rows (branch/PR label or re-stamp) so pre/post both survive; (3) ledger row in results/notes/linear_solver_accuracy_2026_09.md + wiki/campaigns/linear_solver_accuracy.md (+ index) + build_readme.py; note tol_1e-2 no longer reproduces pdip_raw; (4) ruff/pytest/check_* gates; (5) /ship_workspace raw-pdip-forward-polish (library-first gate: #595 merged; release-gate: PyAutoArray until released), then /prm closes the task. euclid pipeline + autolens_workspace_test: no edits."
