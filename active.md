# Active Tasks

## nerves-unused-keys
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/174
- issued: 2026-09-26
- prompt: active/organ_cockpit_nerves_unused_keys.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-26; session ID https://claude.ai/code/session_01SbKQQHRRgm2b69aT9t7771
- status: library-dev (BUILT, committed 079b182, unpushed — awaiting Heart YELLOW ack + /ship_library; checkpoint on the issue 2026-09-26)
- resume: /ship_library bundle cockpit-followups → push + PR + merge on green → dispatch nerves_board.yml / gut_board.yml → /prm. 206 tests; AST scan; real counts Fit 8 / Array 1 / Galaxy 1 / Lens 58 (dead Dynesty block) / CTI 8 unused
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
- status: library-dev (BUILT, committed d956c380, unpushed — awaiting Heart YELLOW ack + /ship_library; checkpoint on the issue 2026-09-26)
- resume: /ship_library bundle cockpit-followups → push + PR + merge on green → dispatch nerves_board.yml / gut_board.yml → /prm. 23 tests; PAT_PYAUTOLABS path masked; 8 overdue sibling refs in the void-plan; Void links 44→53
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
- status: library-dev (BUILT, committed e31d92f, unpushed — awaiting Heart YELLOW ack + /ship_library; checkpoint on the issue 2026-09-26)
- resume: /ship_library bundle cockpit-followups → push + PR + merge on green → dispatch nerves_board.yml / gut_board.yml → /prm. 41 targeted tests; heart_feed.py live STALE exit 1; step 0a in start_dev + start_bundle + route + WORKFLOW
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

## pointsolver-step0-gather
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/579
- issued: 2026-09-26
- prompt: active/pointsolver_step0_gather_containment.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 subagent), 2026-09-26; session ID unavailable
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4b: step-0 containment without the (N,3,2) gather; prototype + laptop measurement first)
- worktree: /home/jammy/Code/PyAutoLabs-wt/pointsolver-step0-gather
- repos:
  - PyAutoArray: feature/pointsolver-step0-gather
  - autolens_profiling: feature/point-source-cpu-p4b
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4 (PR #321 open), interferometer-mesh-breakdown-a100 and point-source-source-plane-p2a. p4b is the human-approved sequential follow-on of p4: its branch feature/point-source-cpu-p4b is based on feature/point-source-cpu-p4 until #321 merges, then rebases onto main. It touches scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py and later results/breakdown/point_source_image/ + point_source_cpu_campaign.md (Phase 4b section); disjoint from the interferometer and source-plane tasks. Human-approved 2026-09-26."
- checkpoint: 2026-09-26 WIP commit 8755072f on PyAutoArray feature/pointsolver-step0-gather (LOCAL only, not pushed): 4 step-0 routes behind array._STEP0_CONTAINMENT, scratch bit-identity OK; resume = tests (fuzz, refinement, HLO guard red-on-main) -> PyAutoArray+PyAutoLens suites -> --step0-route laptop A/B in the p4b profiling worktree (no changes there yet) -> pick default (see issue #579 checkpoint comment)

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
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/324
- heart-ack: "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml; release validation stale: source moved since rehearsal (PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens) (acknowledged 2026-09-27, none touch autolens_profiling)"
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-breakdown-a100
- autonomy: supervised (header); plan approved in-session 2026-09-26
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4, point-source-source-plane-breakdown and point-source-folder-split. File sets are disjoint: this task touches scripts/interferometer/, hpc/batch_gpu/submit_breakdown_interferometer_*, results/breakdown/interferometer/ and results/notes/interferometer_mesh_*. The only shared surface is the generated README dashboards, regenerated at ship. Human-approved 2026-09-26, #177 precedent."
- repos:
  - autolens_profiling: feature/interferometer-mesh-breakdown-a100
- resume: PHASES A+B+C DONE (2026-09-27). Phase C shipped: findings note results/notes/interferometer_mesh_a100_breakdown_2026_09.md with ranked levers (commit 0b80f88); origin/main merged in (75e7be4, README findings-list conflict with #322 resolved, build_readme --check clean); branch pushed, PR https://github.com/PyAutoLabs/autolens_profiling/pull/324 open (Closes #320). Next = human /prm 324, then close-out (lifecycle record). Follow-ups filed: C2 amendment appended to draft/feature/autofit/certified_solver_batched_guard_c2.md (lever 1, interferometer sparse cells); draft/research/autolens_profiling/interferometer_w_tilde_fft_size_levers.md (lever 2); draft/research/autolens_profiling/interferometer_fixed_mapper_curvature_preload.md (lever 3).
