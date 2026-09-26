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

## interferometer-mge-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/308
- issued: 2026-09-25
- prompt: active/interferometer_mge_breakdown_jax_cpu_gpu.md
- session: Claude Code CLI (Opus 5.5), 2026-09-25
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-25 (research only, no library edits)
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mge-breakdown
- repos:
  - autolens_profiling: feature/interferometer-mge-breakdown
- parallel-claim: "autolens_profiling is also claimed by certified-solver-phase-c1-lane-rate (feature/certified-solver-phase-c1-lane-rate). Disjoint file sets: that task is imaging/nautilus capture + imaging submits + results/breakdown/imaging/nautilus_batches_*; this task adds scripts/interferometer/likelihood_breakdown/mge.py, hpc/batch_gpu/submit_breakdown_interferometer_mge_*, results/breakdown/interferometer/mge_*, results/notes/interferometer_mge_breakdown_2026_09.md and edits scripts/misc/vram/config.py. Only shared surface is the generated README dashboard (regenerate at ship). Recorded 2026-09-25 per the #177 precedent."
- ral-jobs: final A100 round r3 on nufftax 0.6.1 (human upgraded shared RAL venv 2026-09-25): sma 351083, alma 351078, alma_high 351079/351080(mp), jvla 351081/351082(mp) — all COMPLETED and pulled. RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mge-breakdown @6a9f2be.
- resume: PHASE C DONE; PR https://github.com/PyAutoLabs/autolens_profiling/pull/312 open (pending-release), Heart YELLOW acknowledged by human 2026-09-26 (unrelated reasons). Next = /prm (merge + completion record). 5 follow-ups filed in draft/: interferometer_mge_w_tilde_route_mge_only, interferometer_chunked_transform_mapping_matrix, interferometer_transform_mapping_matrix_real_scatter, ral_venv_dependency_floor_drift, workspace_interferometer_mge_sparse_operator_memory_docs.
- summary: Interferometer likelihood campaign 1/3: interferometer MGE breakdown cell on the shared harness (+ exploratory W~ func-list arm), JAX CPU + RAL A100 fp64 (mp on A100) across sma/alma/alma_high(/jvla), VRAM block re-test, ranked lever note + follow-up prompts.

## multistart-cpu-memory-probe
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1646
- issued: 2026-09-26
- prompt: active/multistart_cpu_memory_probe_doubles_compile.md
- session: Claude Code CLI (Opus 5.5 subagent), 2026-09-26
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-26
- worktree: /home/jammy/Code/PyAutoLabs-wt/multistart-cpu-memory-probe
- repos:
  - PyAutoFit: feature/multistart-cpu-memory-probe
- resume: Fix + tests committed locally as 3220566e3 on feature/multistart-cpu-memory-probe (NOT pushed; 139 mle tests pass, new tests red->green). Parked at ship gate: Heart YELLOW for unrelated reasons (workspace validation 4 failed cluster/weak notebooks; manifest drift x3; release validation stale). Next = human acks YELLOW, then push + PR (label pending-release; body drafted by session).
- summary: Skip MultiStartGradient's unbatched-memory probe on the CPU JAX backend (two throwaway full-model compiles; caused the 2026-09-26 release-integrate start_here.py 3605 s TIMEOUT, run 36226772178).
