# Active Tasks

## point-source-cpu-p3
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/568
- issued: 2026-09-24
- prompt: active/pointsolver_cpu_speed_phases_3_4.md
- session: Claude Code CLI (Opus 5.5), 2026-09-24
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-24 (tolerance gate, geometric 11 859-vertex table, on-by-default for the JAX PointSolver if the A/B accepts)
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-cpu-p3
- repos:
  - PyAutoArray: feature/point-source-cpu-p3
  - PyAutoLens: feature/point-source-cpu-p3
  - autolens_profiling: feature/point-source-cpu-p3
- heads: "PyAutoArray ad0bf97b, PyAutoLens b346b6a0, autolens_profiling 2f5c1c3 (all pushed on feature/point-source-cpu-p3)"
- ral-jobs: "350636 CPU ral euclid-ral-compute-10-2 (folding off + on) and 350637 A100 euclid-ral-gpu-1, both COMPLETED 2026-09-24, ingested in autolens_profiling 2f5c1c3: ACCEPT (CPU 2.0x simple, 5.2x cluster, 31/31 gates bit-identical); tie-case gate decision pending at ship"
- ral-state: "RAL branch clones /mnt/ral/jnightin/autolens_profiling_wt/PyAutoArray_point-source-cpu-p3 and /mnt/ral/jnightin/autolens_profiling_wt/PyAutoLens_point-source-cpu-p3 (plus worktree /mnt/ral/jnightin/autolens_profiling_wt/point-source-cpu-p3) to delete after release"
- parallel-claim: "autolens_profiling is also claimed by certified-solver-phase-b (feature/certified-solver-phase-b). Disjoint file sets: that task edits scripts/imaging/likelihood_breakdown/fixed_light_trace.py, adds hpc/batch_gpu/submit_breakdown_imaging_fixed_light_certified_policy_a100_hst_fp64 and results/notes/certified_solver_policy_phase_b_2026_09.md; this task adds scripts/point_source/likelihood_breakdown/static_lattice_ab.py, RAL CPU + A100 submits, results/breakdown/point_source/static_lattice_ab_* and the phase-3 section of results/notes/point_source_cpu_campaign.md. Recorded 2026-09-24 per the residue-p1/#267 precedent."
- summary: Phase 3 of the point-source CPU campaign: precompute the static step-0 triangle lattice of the JAX PointSolver as a cached geometric unique-vertex table (11 859 of 69 849 slots for the ±9.9/0.2 lattice) so step 0 deflects only unique vertices. PyAutoArray adds the cached builder + opt-in static_vertices; PyAutoLens turns it on in the JAX _initial_triangles; autolens_profiling measures with static_lattice_ab.py (laptop witness, RAL CPU host-pinned + A100). Library-first ship; reject by the stop rule.

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
- session: claude (Fable CLI, 2026-09-23; resumed from Codex 2026-09-22)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Implemented + committed locally as c6b514d on feature/vis-lp-inspection-bundle (133 tests green, not pushed). Human reviews diff (scratchpad part1_diff.txt) before ship_workspace; then sync tooling to the euclid_dr1 science clone/RAL and submit the 4,922-tile vis_lp-only bundle (OUTPUT_DIR=dr1_full, INITIAL_SEARCH_NAME=vis_lp, DATASET_NAMES_PATH=all, TAR_TO set) as a Cortex run.

## hst-gpu-residue-p4
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/303
- issued: 2026-09-24
- prompt: active/hst_gpu_residue_p4_logdet_cholesky_reuse.md
- session: Claude Code CLI (Opus 5.5), 2026-09-24
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-24
- worktree: /home/jammy/Code/PyAutoLabs-wt/hst-gpu-residue-p4
- repos:
  - autolens_profiling: feature/hst-gpu-residue-p4
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p3 (feature/point-source-cpu-p3). Disjoint file sets: this task edits scripts/imaging/likelihood_breakdown/fixed_light_trace.py and scripts/misc/likelihood_breakdown/xla_attribution.py, adds scripts/misc/likelihood_breakdown/logdet_reuse_injection.py, hpc/batch_gpu/submit_breakdown_imaging_fixed_light_logdet_reuse_a100_hst_fp64, tests under scripts/misc/test/ and results/notes/hst_gpu_residue_phase4_logdet_2026_09.md; that task touches point-source scripts/results. Recorded 2026-09-24 per the residue-p1/#267 precedent."
- next: "implement steps 0-5 (stage-map re-anchor, logdet_reuse_injection, --logdet-candidate, gate, tests, RTX screen), then submit the 6-task A100 array; harvest is the human resume point"
- summary: Phase 4 of hst-gpu-non-solver-residue: harness-only reuse of the library certified solve's masked Cholesky + a bounded Schur complement over the fixed set for log det(F+λH) (0.89 ms ceiling, 2.8 %), pinned at 1e-9 vs the library; PyAutoArray prompt only if >= 0.5 ms whole-call.
