# Active Tasks

## autolens-visualization-birth
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/436
- issued: 2026-09-25
- prompt: active/birth_autolens_visualization_repo.md
- session: Claude Code CLI (Fable 5.1 architect, Opus execution), 2026-09-25
- status: workspace-dev
- autonomy: human-required (header); plan approved in-session 2026-09-25; `gh repo create` and the org-profile README row denied to the agent (public-surface guard) — human creates PyAutoLabs/autolens_visualization and pushes
- worktree: /home/jammy/Code/PyAutoLabs-wt/autolens-visualization-birth
- repos:
  - autolens_visualization: feature/autolens-visualization-birth (new local repo at lens/autolens_visualization, no remote yet)
  - PyAutoMind: feature/autolens-visualization-birth
  - PyAutoBrain: feature/autolens-visualization-birth
  - PyAutoHeart: feature/autolens-visualization-birth

## mge-nnls-grad-nan
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/573
- issued: 2026-09-25
- prompt: active/mge_nnls_grad_nan.md
- session: Claude Code CLI (Opus 5.5), 2026-09-25
- status: library-dev
- autonomy: human-required (header); plan approved in-session 2026-09-25 (choose polish vs effective-kappa on evidence; runtime vs autolens_profiling from a detached scratch worktree, no profiling claim)
- worktree: /home/jammy/Code/PyAutoLabs-wt/mge-nnls-grad-nan
- repos:
  - PyAutoArray: feature/mge-nnls-grad-nan

## certified-solver-phase-c1-lane-rate
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/304
- issued: 2026-09-24
- prompt: active/certified_solver_phase_c1_lane_rate.md
- session: Claude Code CLI (Opus 5.5), 2026-09-24
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-24 (measurement only; release block overridden by the human, runs against library mains incl. unreleased PyAutoArray#567)
- worktree: /home/jammy/Code/PyAutoLabs-wt/certified-solver-phase-c1-lane-rate
- repos:
  - autolens_profiling: feature/certified-solver-phase-c1-lane-rate
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p3 (feature/point-source-cpu-p3). Disjoint file sets: that task adds scripts/point_source/likelihood_breakdown/static_lattice_ab.py, point-source RAL submits, results/breakdown/point_source/static_lattice_ab_* and results/notes/point_source_cpu_campaign.md; this task adds scripts/imaging/likelihood_breakdown/nautilus_batch_capture.py, a --lanes captured mode in scripts/imaging/likelihood_breakdown/fixed_light_trace.py, hpc/batch_gpu/submit_breakdown_imaging_fixed_light_certified_lane_rate_a100_hst_fp64 (+ static test), results/breakdown/imaging/nautilus_batches_* and results/notes/certified_solver_phase_c1_lane_rate_2026_09.md. Recorded 2026-09-24 per the residue-p1/#267 precedent."
- ral-jobs: 2026-09-25 RESUBMIT @ be01a52 (rect pix1+pix2 now free al.reg.Adapt as production; #572 `preconditioning` forwarded by the harness wrappers) — capture 350766 (array 1,3: rectangular pix1/pix2) → replay 350768 (array 4-37, afterok:350766). Delaunay captures from 350659_0/_2 reused (AdaptSplit, fingerprint unchanged). Old run: 350659_3 failed (rect pix2 had 1 free param → Nautilus needs ≥2), 350663 cancelled (DependencyNeverSatisfied); stale Constant rect captures moved to results/breakdown/imaging/stale_constant_350659/ on RAL. OUTCOME (checked 2026-09-25): 350766_1/_3 COMPLETED (16m/6m, no OOM); 350768_4-7 rate COMPLETED; 350768 time B=16/20/50 (24 tasks) exit 1 BY DESIGN — pre-registered per-lane gate (arm vs own-composition library-PDIP ref, 1e-9) FAILED on 2-40 lanes/task incl. pdip/on rows, JSONs written first (28 captured JSONs on RAL); B=100 (17-19, 29-31) OOM ~74 GiB = the pre-registered memory-limit row, no JSON. Nothing to resubmit; gate not loosened.
- ral-jobs-prev: capture 350659 (array 0-3: delaunay/rectangular x pix1/pix2) → replay 350663 (array 4-37, afterok:350659), submitted 2026-09-24 from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/certified-solver-phase-c1-lane-rate @ f59f84d; libs on RAL = local mains (PyAutoArray 7fa8d271 incl. #567). lensed_source.fits seeded from RAL main (sha 5256cba0…, differs from laptop 091c9052…; phase B read the RAL copy).
- resume: per-lane gate-failure analysis in progress 2026-09-25 (lane-driven vs composition-driven; free regularization suspected); pull the 28 JSONs, write results/notes/certified_solver_phase_c1_lane_rate_2026_09.md + job provenance JSON, apply the verdict rule, then ship_workspace. Laptop witness (n_batch=4, prior/exploration lanes only): free-reg uncertified 10/60 Delaunay pix1, 9/60 pix2, 14/60 rectangular pix1 (fixed-reg round 1: 0/60) — uncertified lanes are weakly regularized, none-vs-PDIP up to 3e-4 relative.
- summary: Certified-positive-solver phase C1: capture real Nautilus proposal batches at production n_batch=20 (HST fixed-light, Delaunay N=1500 + rectangular), replay on A100 fp64 under certified+fallback none jit(vmap) for the uncertified-lane rate, matched timing at B=16/20/50/100, verdict gates C2 (draft/feature/autofit/certified_solver_batched_guard_c2.md).

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
- summary: Interferometer likelihood campaign 1/3: interferometer MGE breakdown cell on the shared harness (+ exploratory W~ func-list arm), JAX CPU + RAL A100 fp64 (mp on A100) across sma/alma/alma_high(/jvla), VRAM block re-test, ranked lever note + follow-up prompts.
