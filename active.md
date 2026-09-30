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

## raw-pdip-forward-polish
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/594
- issued: 2026-09-30
- prompt: active/raw_pdip_forward_amplitude_bias_fix.md
- epic: linear-solver-programme
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID unavailable
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 via Plan Mode (forward polish = the #573 mechanism returned as the forward value; regression fixture 8 #571 systems + euclid vis_lp with fnnls x_ref; gates on inactive-column/total/source flux ≤ 1e-3, not amp_rel_max)
- parallel-claim: "PyAutoArray is also claimed by streaming-p1-array-free-dataset (active). File sets disjoint (this task: autoarray/util/jax_nnls.py, autoarray/config/general.yaml, autoarray/settings.py docstring, autoarray/inversion/inversion/inversion_util.py docstring, test_autoarray/inversion/inversion/{test_nnls_raw_forward_amplitude.py,files/mge_solver_reference_systems.npz,files/README.md}; streaming-p1: autoarray/dataset/**, autoarray/fit/fit_interferometer.py, autoarray/inversion/inversion/interferometer/**). Whichever ships second rebases. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/raw-pdip-forward-polish
- repos:
  - PyAutoArray: feature/raw-pdip-forward-polish
  - autolens_profiling: feature/raw-pdip-forward-polish
- summary: Return the #573 polished iterate (≤ 10 tight warm-started Jacobi-system PDIP iterations) as the raw-forward PDIP forward value in both the custom_vjp forward and the primal, so jit/grad/eager agree; new amplitude regression test over the phase-1 corpus (8 #571 + euclid, fnnls reference) red on d4298445; euclid latent jit test then passes on library main with no override; downstream autolens_profiling ledger row after the library merge.
- heart-red-hold: 2026-09-30 ~16:25 BST ship_library gate RED — "release validation FAILED (stage integrate)"; YELLOW "workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)", "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"; none in PyAutoArray; human override + human push needed (auto-mode classifier denies the agent push)
- resume: "Library fix COMPLETE locally: PyAutoArray feature/raw-pdip-forward-polish head 31b1c2d7 (7e62fa4d red test + fixture, 31b1c2d7 fix), NOT pushed, no PR. Gates: new test 107/107 (12 red on base), full pytest 1890, euclid latent test 19/19 with +7.47e-5 jit-vs-eager (was +5.76e-2), corpus 81/81 == pdip_raw_polish, workspace_test 7 scripts pass, no pin moved. PR body drafted at scratchpad p2_pr_body.md (also to be posted on #594). Next: human RED override → push → gh pr create --label pending-release → /prm; then workspace phase in the same worktree's autolens_profiling (uncommitted re-run results with the colliding v2026.8.17.1 stamp; euclid_latent.py validation leg pinned to pre-fix 3.511 must be re-based; ledger row + campaign page + build_readme)."

## streaming-p2-fit-save-reload
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/638
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/639
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/758
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/639
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/758
- issued: 2026-09-30
- prompt: active/streaming_p2_fit_save_reload.md
- epic: streaming-visibilities (phase 2 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/streaming-p2-fit-save-reload
- autonomy: supervised (header); plan approved in-session 2026-09-30 (fit guards, SparseTerms FITS extensions in save_attributes, EXTNAME aggregator loader with re-attached operator; ag + al)
- repos:
  - PyAutoGalaxy: feature/streaming-p2-fit-save-reload
  - PyAutoLens: feature/streaming-p2-fit-save-reload
- heart-red-override: "RED 2026-09-30T12:42Z — exact reason: `release validation FAILED (stage integrate)` (unrelated release-integrate leg). Live human authorization in-session 2026-09-30 for #638 / feature/streaming-p2-fit-save-reload (PyAutoGalaxy + PyAutoLens): 'Authorize override for #638' (commit, push, pending-release PRs only; merge separate + checks green; no release). Branch gates: test_autogalaxy 1284 passed; test_autolens 770 passed + 1 xfailed; round-trip red-check; Codex astra review FINDINGS (3): #1 + #3 fixed in-branch (red-checked), #2 pre-existing → bug draft filed."
