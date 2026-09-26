# Active Tasks

## gut-board
- issue: https://github.com/PyAutoLabs/PyAutoGut/issues/9
- issued: 2026-09-26
- prompt: active/gut_board.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-26; session ID unavailable
- status: library-dev
- autonomy: safe (header); epic organ-cockpit; scope widened by the human 2026-09-26 (one-tap void buttons); plan approved in session and on the issue; merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/gut-board
- repos:
  - PyAutoBrain: feature/gut-board
  - PyAutoGut: feature/gut-board
  - pyautolabs.github.io: feature/gut-board
- parallel-claim: "PyAutoBrain also claimed by eyes-organ-order + cosmos-web-ring-greeting (disjoint: this task touches board/_theme.py, config/policy.yaml boards list, agents/conductors/hygiene/_hygiene_condemned.py, tests); PyAutoGut by eyes-organ-order (AGENTS.md one-line organ-order edit; this task appends a new AGENTS.md section + scripts/board.py, .github/workflows/{gut_board,void}.yml, tests/, README.md); pyautolabs.github.io by eyes-organ-order (no diff; this task edits one cockpit ORGANS line). Own worktree per the #177 precedent, recorded 2026-09-26."
- plan: three PRs, merge order Brain (theme + policy + parser helper) → Gut (board, feed, gut_board.yml Pages birth, void.yml issue-triggered void) → hub (cockpit ORGANS feed line)
- summary: Gut board (Pages) + state.json feed + one-tap "Void permanently" via prefilled issues handled by void.yml; reconciles ls-remote refs against condemned.md (due / transit / held / orphans / dangling); Nerves decision: no board.

## eyes-organ-order
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/439
- issued: 2026-09-25
- prompt: active/eyes_organ_order.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-25; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan on the issue; reorder is the next leg, merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/eyes-organ-order
- repos:
  - PyAutoMind: feature/eyes-organ-order
  - PyAutoBrain: feature/eyes-organ-order
  - PyAutoHeart: feature/eyes-organ-order
  - PyAutoHands: feature/eyes-organ-order
  - pyautolabs.github.io: feature/eyes-organ-order
  - PyAutoScientist: feature/eyes-organ-order
  - PyAutoCortex: feature/eyes-organ-order
  - PyAutoNerves: feature/eyes-organ-order
  - PyAutoGut: feature/eyes-organ-order
- resume: bundle worktree created; implement the reorder per the issue plan (Eyes between Memory and Heart), then repos_sync --write, then ship

## oneshot-benchmark-harness
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/126
- issued: 2026-09-17
- prompt: active/oneshot_benchmark_harness.md
- session: claude --resume session_01YTzjiXh2fLocc6dNqLQ66d
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/380
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/127
- autonomy: supervised (header; launched on the human's "Go / continue" in-session — plan on the issue, shipped to PR-open 2026-09-17, merge is human; Brain PR first, it is the assistant PR's `Brain-ref:`)
- location: web-github (session clones /home/user/autolens_assistant + /home/user/PyAutoBrain, no task worktree)
- worktree: n/a — web-github session clones
- repos:
- note: "PyAutoBrain PR #380 and autolens_assistant PR #127 merged; issue #126 is closed. Both repo claims are released. The entry remains active only for the first real headless runs noted below; do not fully close it as part of codex-hook-parity."
- summary: |
    One-shot, machine-scored assistant benchmarks: headless `benchmark.py run`
    (harnesses.yaml adapters, private workdir without benchmarks/truth, compute
    shims), computed-score contract (common gates × card metrics → score.json,
    RESULTS.md medians), prompt freeze (prompt_sha256 + VERSIONS.lock), first
    one-shot card `oneshot-smoke`, 2026-07 cards retired to prompts/conversational/,
    Brain clone VALIDATION_PLAN/partition update. Cards
    benchmark_positions_initialised_inference / benchmark_forward_model_consistency
    stay in draft/, Blocked-by this task. Real headless runs need a laptop with
    the agents installed — the human's first step after merge.

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

## point-source-cpu-p4
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/314
- issued: 2026-09-26
- prompt: active/pointsolver_cpu_speed_phase_4.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-26; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4a: re-baseline + solver-config sweep, single-source, workspace-only)
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-cpu-p4
- repos:
  - autolens_profiling: feature/point-source-cpu-p4
- parallel-claim: |
    autolens_profiling also claimed by interferometer-transform-real-scatter (1 file: hpc/batch_gpu interferometer A100 submit); file sets disjoint; human-approved own worktree 2026-09-26

## interferometer-transform-real-scatter
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/577
- issued: 2026-09-26
- prompt: active/interferometer_transform_mapping_matrix_real_scatter.md
- session: Claude Code CLI (Opus 5.5), 2026-09-26
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-transform-real-scatter
- autonomy: supervised (header); plan approved in-session 2026-09-26
- repos:
  - PyAutoArray: feature/interferometer-transform-real-scatter
  - autolens_profiling: feature/interferometer-transform-real-scatter

## point-source-source-plane-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/315
- issued: 2026-09-26
- prompt: active/point_source_source_plane_chi_squared_speed.md
- epic: point-source-cpu-speed (phase 1 of the source-plane chi-squared campaign; single-source only, human steer 2026-09-26)
- session: Claude Code CLI (Fable 5.1), 2026-09-26
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-source-plane-breakdown
- autonomy: supervised (header); plan approved in-session 2026-09-26
- parallel-claim: autolens_profiling is also claimed by interferometer-transform-real-scatter (PyAutoArray#577); file sets are disjoint (theirs: one hpc/batch_gpu/ submit; ours: scripts/point_source/, results/breakdown/point_source/, results/notes/). Own worktree approved by the human 2026-09-26.
- repos:
  - autolens_profiling: feature/point-source-source-plane-breakdown
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/317 (DRAFT)
- resume: Phase 1 built + pushed (44c43d9, b480236, 1055c57; new cell at scripts/point_source_source/, results/breakdown/point_source_source/). BLOCKED on the scripts/point_source → point_source_image/point_source_source move-only split PR (merge order split → #315 → #314). Next: after the split merges, rebase, carry the guard-removal diff to the moved runtime cell, fix scripts/point_source/ refs in the note + cell docstring, regen README, undraft, /ship_workspace; re-run the local row on an idle host (phase-1 row taken at load ~16/8 cores) or take RAL rows before phase 2 is ranked.
- summary: Build scripts/point_source_source/likelihood_breakdown/source_plane.py (simple instrument, solved primary + plain control, fused control, cumulative prefixes, grad-cost row), retire the stale plain-path JIT guard in the runtime cell, publish local_cpu_fp64 row + README + campaign note with ranked residue and a carried-to-cluster note.

## point-source-folder-split
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/316
- issued: 2026-09-26
- prompt: active/point_source_folder_split.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 subagent), 2026-09-26; session ID unavailable
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/318
- autonomy: supervised (header); plan approved in-session 2026-09-26 ("give me the prompt and then go ahead"); move-only refactor
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-folder-split
- repos:
  - autolens_profiling: feature/point-source-folder-split
- parallel-claim: |
    autolens_profiling also claimed by interferometer-transform-real-scatter, point-source-cpu-p4 (#314) and point-source-source-plane-breakdown (#315); this split merges FIRST and the others rebase onto it; human-approved 2026-09-26
