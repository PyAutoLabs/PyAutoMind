# Active Tasks

## point-source-cpu-p1
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/297
- issued: 2026-09-23
- prompt: active/pointsolver_image_plane_chi_squared_cpu_speed.md
- session: Claude Code CLI (Fable 5.1), 2026-09-23
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-cpu-p1
- repos:
  - autolens_profiling: feature/point-source-cpu-p1
- summary: Phase 1 of the point-source CPU campaign: reproduce the CPU breakdown evidence (simple solved likelihood + 13-component two-source cluster cell) on a quiet RAL CPU host, recover the 2026-09-17 reported note/JSONs, freeze the unoptimized library revisions (PyAutoArray 22e6d608, PyAutoLens 2aaa1c1a8). No library edits; phase 2 is the throwaway jnp.unique lever.

## abell-1201-point-mass
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/133
- issued: 2026-09-22
- prompt: active/add_an_abell_1201_central_point_mass.md
- session: Codex (session ID unavailable)
- status: awaiting-input
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/134
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/414
- merge-order: Brain 414 first, assistant 134 second; assistant declares Brain-ref. Full scientific task remains open after these preparation PRs merge.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/abell-1201-point-mass
- repos:
- preparation-record: complete/2026/09/abell-1201-preparation.md
- claims-released: Both preparation branches merged; worktree retained for science continuation and ignored plots/reports (4.2 MB).
- repair-plan: Human "go" approved classifying the exact Abell README as domain in Brain and assistant template policy, with regression tests, then retrying shipping. Brain attached to existing task root; fresh Mind has no competing Brain claim (stale canonical claim belongs to merged Brain PR 409).
- summary: Preparation phase merged via human prm on 2026-09-22 (Brain 414 then assistant 134), all four CI jobs green. Full posterior budget and science validation remain checkpoints; no release or posterior execution authorised.
- heart-red-override:
  - authorization: User "continue i suthorize" in direct response to development-only shipping override for issue #133; no release, merge, posterior run or CI bypass.
  - red-reasons: "release validation FAILED (stage integrate)"
  - passed: 129 tests at refreshed head 79854cc; refreshed data preparation, finite coarse likelihood smoke and freeze-check pass.
  - repaired: Clone-boundary now passes with paired Brain classification; 56 clone tests pass. User "go" approved coordinated repair and shipping retry. Separate independent review not required on supervised path; no independent CLEAN verdict claimed.
- latest-shipping-attempt: Assistant f14293d (PR 134), Brain b1c8d89 (PR 414), both pushed with pending-release labels and dependency comments. Publication permission recorded at 79854cc with Nightingale et al. (2023)/HST credit. Heart remains RED for release purposes.
- resume: Preparation PRs are MERGED; do not rerun shipping. Retain issue 133 for full-run budget, posterior/scientific calibration and unresolved absolute photometric units. Approved F390W power-law + shear + point mass with nuisance parameters, cleaned 4 arcsec mask (31417 pixels). No posterior or headless run authorised/executed. Pre-removal originals deferred; RGB retains/discloses cut-out. Worktree retained, artifacts under scripts/scratch/abell_1201; preserve during cleanup. Originals untouched. Re-survey claims and branch before further implementation.

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
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Plan approved. Issue #102 filed. Implement and test in the isolated workspace, then ship and refresh the existing catalogue without rerunning fits.

## certified-positive-solver
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/566
- issued: 2026-09-23
- prompt: active/implement_and_optimize_certified_positive_solver.md
- session: claude (Fable CLI, 2026-09-23)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/certified-positive-solver
- repos:
  - PyAutoArray: feature/certified-positive-solver
- summary: |
    Phase A of the certified-positive-solver epic: port the harness certified
    active-set positive solver into PyAutoArray (autoarray/util/jax_active_set.py,
    budgeted while_loop, KKT certification, PDIP fallback, stop_gradient search +
    autodiffed final solve), wired behind Settings/general.yaml as OPT-IN
    (positive_only_solver: pdip default) and dispatched only for JAX mapper-only
    inversions; NumPy path untouched. Phase B (production jit(vmap) benchmark and
    default flip) is draft/research/autolens_profiling/certified_solver_production_default.md.
