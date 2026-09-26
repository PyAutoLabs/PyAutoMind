# Active Tasks

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

## cosmos-web-ring-greeting
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/136
- issued: 2026-09-26
- prompt: active/cosmos_web_ring_greeting.md
- session: Claude Code (Fable 5.1 session; ID unavailable)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/cosmos-web-ring-greeting
- repos:
  - autolens_assistant: feature/cosmos-web-ring-greeting
  - PyAutoBrain: feature/cosmos-web-ring-greeting
- phases: 1 assistant (Abell removal, ring modelling, fit benchmark, audience routing) → 2 assistant Colab notebook → 3 website
- supersedes: abell-1201-point-mass (autolens_assistant#133)

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

## interferometer-mge-w-tilde-route
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/575
- issued: 2026-09-26
- prompt: active/interferometer_mge_w_tilde_route_mge_only.md
- session: Claude Code CLI (Opus 5.5), 2026-09-26
- status: workspace-dev
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/576
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/629
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/750
- heart-red-override: "2026-09-26 live user chose 'Override, open PRs' for this task (commit/push/pending-release PR only; merge via /prm on green checks; no release). RED reasons: release validation FAILED (stage integrate); workspace validation not passing (4 failed, cloud#35579888156); manifest drift hub organism blurb 7; manifest drift organism-map blocks 1. Gates passed: unit 1706/1240/757+1xf, smoke 24/24."
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mge-w-tilde-route
- autonomy: supervised (header); plan approved in-session 2026-09-26 (scope incl. interferometer profile-subtracted dirty-image seam fix in PyAutoGalaxy + PyAutoLens)
- repos:
  - PyAutoArray: feature/interferometer-mge-w-tilde-route
  - PyAutoGalaxy: feature/interferometer-mge-w-tilde-route
  - PyAutoLens: feature/interferometer-mge-w-tilde-route
  - autolens_profiling: feature/interferometer-mge-w-tilde-route
- workspace-scope: autolens_profiling library-path re-run of scripts/interferometer/likelihood_breakdown/mge.py (CPU + A100), VRAM rows in scripts/misc/vram/config.py, addendum to results/notes/interferometer_mge_breakdown_2026_09.md. Library PRs held by Heart freeze until 2026-09-26T14:45Z (release validation 2026.9.26.1.dev78601).
