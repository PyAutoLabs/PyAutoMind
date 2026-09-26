# Active Tasks

## nerves-unused-keys
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/174
- issued: 2026-09-26
- prompt: active/organ_cockpit_nerves_unused_keys.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-26; session ID https://claude.ai/code/session_01SbKQQHRRgm2b69aT9t7771
- status: library-dev
- autonomy: safe (header); bundle cockpit-followups (with gut-void-sibling-reach, start-dev-heart-gate); epic organ-cockpit; plan approved in session and on the issue; merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/cockpit-followups
- repos:
  - PyAutoNerves: feature/nerves-unused-keys
- parallel-claim: "PyAutoNerves is also claimed by eyes-organ-order (one-line organ-order edits). This member touches scripts/board.py, .github/workflows/nerves_board.yml, test_autonerves/test_board.py, README.md, AGENTS.md. Disjoint; shared bundle worktree per the #177 precedent, recorded 2026-09-26."
- summary: Nerves board flags library config keys no library code reads (conf.instance lookup scan; used / section-read / unused; info items only).

## gut-void-sibling-reach
- issue: https://github.com/PyAutoLabs/PyAutoGut/issues/11
- issued: 2026-09-26
- prompt: active/organ_cockpit_gut_void_sibling_reach.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-26; session ID https://claude.ai/code/session_01SbKQQHRRgm2b69aT9t7771
- status: library-dev
- autonomy: safe (header); bundle cockpit-followups (with nerves-unused-keys, start-dev-heart-gate); epic organ-cockpit; plan approved in session and on the issue; merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/cockpit-followups
- repos:
  - PyAutoGut: feature/gut-void-sibling-reach
- parallel-claim: "PyAutoGut is also claimed by eyes-organ-order (one-line organ-order edits). This member touches scripts/board.py, .github/workflows/void.yml, tests/, README.md, AGENTS.md. Disjoint; shared bundle worktree per the #177 precedent, recorded 2026-09-26."
- summary: Gut Void button reaches refs held on sibling repos via PAT_PYAUTOLABS in void.yml; elsewhere rows get the button; per-ref failure reporting.

## start-dev-heart-gate
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/423
- issued: 2026-09-26
- prompt: active/organ_cockpit_start_dev_heart_gate.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-26; session ID https://claude.ai/code/session_01SbKQQHRRgm2b69aT9t7771
- status: library-dev
- autonomy: safe (header); bundle cockpit-followups (with nerves-unused-keys, gut-void-sibling-reach); epic organ-cockpit; plan approved in session and on the issue; merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/cockpit-followups
- repos:
  - PyAutoBrain: feature/start-dev-heart-gate
- parallel-claim: "PyAutoBrain is also claimed by eyes-organ-order (one-line organ-order edits and cosmos-web-ring-greeting (clone conductor)). This member touches bin/heart_feed.py, skills/start_dev/start_dev.md, skills/start_bundle/start_bundle.md, skills/route/route.md, skills/WORKFLOW.md, tests/. Disjoint; shared bundle worktree per the #177 precedent, recorded 2026-09-26."
- summary: start_dev 'Heart at the door': bin/heart_feed.py reads the Heart state.json (fallback pyauto-heart readiness), RED stops before planning, YELLOW warns; mirrored in start_bundle and route.

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
- status: awaiting-merge (phase 4a PR #321 open; human runs /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/321
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4a: re-baseline + solver-config sweep, single-source, workspace-only)
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-cpu-p4
- repos:
  - autolens_profiling: feature/point-source-cpu-p4
- parallel-claim: |
    autolens_profiling also claimed by interferometer-transform-real-scatter (1 file: hpc/batch_gpu interferometer A100 submit); file sets disjoint; human-approved own worktree 2026-09-26

## interferometer-mesh-breakdown-a100
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/320
- issued: 2026-09-26
- prompt: active/interferometer_mesh_breakdown_jax_a100.md
- session: Claude Code CLI (Opus 5.5), 2026-09-26
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-breakdown-a100
- autonomy: supervised (header); plan approved in-session 2026-09-26
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4, point-source-source-plane-breakdown and point-source-folder-split. File sets are disjoint: this task touches scripts/interferometer/, hpc/batch_gpu/submit_breakdown_interferometer_*, results/breakdown/interferometer/ and results/notes/interferometer_mesh_*. The only shared surface is the generated README dashboards, regenerated at ship. Human-approved 2026-09-26, #177 precedent."
- repos:
  - autolens_profiling: feature/interferometer-mesh-breakdown-a100

## point-source-source-plane-p2a
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/322
- issued: 2026-09-26
- prompt: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md (campaign prompt retained in draft/; this row is phase 2a)
- epic: point-source-cpu-speed
- session: Claude Code CLI (Fable 5.1), 2026-09-26
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-source-plane-p2a
- autonomy: supervised (header); plan approved in-session 2026-09-26
- parallel-claim: autolens_profiling also claimed by point-source-cpu-p4 (#314: hpc/batch_cpu/*point_source_image*, results/breakdown/point_source_image/, point_source_cpu_campaign.md) and interferometer-mesh-breakdown-a100; phase 2a touches only scripts/point_source_source/, results/breakdown/point_source_source/, point_source_source_plane_campaign.md, hpc/batch_*/submit_breakdown_point_source_source_*, README hand-bullets. Own worktree approved by the human 2026-09-26.
- repos:
  - autolens_profiling: feature/point-source-source-plane-p2a
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/323
- status: awaiting-merge
- heart-ack: "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens)" (acknowledged 2026-09-26, none touch autolens_profiling)
- resume: PR #323 open (ec29705, fc510b0). RAL CPU 8490H fused solved 0.1465 ms, grad 2.26×; pytree/flat_vector 1.361 (0.0385 ms saved) → human kept NO-GO on the PyAutoFit flatten fast path; phase 2b = backward-pass lever. Next: human /prm #323 → close-out; then file phase 2b (backward pass: jacfwd/jacrev ordering + analytic SIE Hessian study) from the campaign prompt.
- summary: RAL CPU (hpc_ral_cpu_fp64) + A100 (hpc_a100_fp64) rows for the source-plane breakdown cell; new interleaved A/B cell pytree_input_ab.py (pytree vs flat_vector vs flat_leaves argument routes, forward + value_and_grad, floors); phase-2a note section with the phase-2b go/no-go (PyAutoFit flatten fast path).
