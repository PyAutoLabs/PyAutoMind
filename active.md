# Active Tasks

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
- ral-jobs: capture 350659 (array 0-3: delaunay/rectangular x pix1/pix2) → replay 350663 (array 4-37, afterok:350659), submitted 2026-09-24 from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/certified-solver-phase-c1-lane-rate @ f59f84d; libs on RAL = local mains (PyAutoArray 7fa8d271 incl. #567). lensed_source.fits seeded from RAL main (sha 5256cba0…, differs from laptop 091c9052…; phase B read the RAL copy).
- resume: pull with `hpc/sync pull` (point it at the RAL worktree), check sacct for OOM at B=50/100 (PSF cube ~389 MB/lane), write results/notes/certified_solver_phase_c1_lane_rate_2026_09.md + job provenance JSON, apply the verdict rule, then ship_workspace. Laptop witness (n_batch=4, prior/exploration lanes only): free-reg uncertified 10/60 Delaunay pix1, 9/60 pix2, 14/60 rectangular pix1 (fixed-reg round 1: 0/60) — uncertified lanes are weakly regularized, none-vs-PDIP up to 3e-4 relative.
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
## euclid-dr1-positions-gate
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/103
- issued: 2026-09-24
- prompt: active/euclid_dr1_positions_gate.md
- session: claude (Fable CLI, 2026-09-24, https://claude.ai/code/session_018LZi93FBcwjRdYx1Qe7Epy)
- worktree: /home/jammy/Code/PyAutoLabs-wt/euclid-dr1-positions-gate
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-dr1-positions-gate
- summary: Pre-submit positions gate: 0.15" central cut, quick SIE+shear fit with one-image leave-one-out drop, per-tile threshold T=min(max(2 s_min,0.3),0.5) in a positions_meta.json sidecar read by load_vis_dataset. Phase 1/3; runs in its own worktree alongside #102 (disjoint files).
- pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/104
- status: awaiting-merge
- heart-red-override: 2026-09-24 live user "I authorise you to continue" for the named #103 development override (push + PR-open only; merge excluded). "Heart RED reasons at the time: release validation FAILED (stage integrate); workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more); manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml. Branch gates: pytest 296 PASS (37 gate tests), exemplar witness verdicts reproduced, in-session review of util.py wiring."
- resume: PR #104 open (4 commits 1fb1a42..485eb9a on feature/euclid-dr1-positions-gate). Next: human /prm when CI is green (merge stays human); then runs with the gate to confirm it is OK BEFORE phase 2 (human sequencing 2026-09-24). Phase 2 started 2026-09-24 as #105 (euclid-dr1-positions-finder, stacked on this branch by human go); phase 3 (draft/research/euclid/euclid_dr1_positions_gate_remodel_run.md) still waits on the merge.

## euclid-dr1-positions-finder
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/105
- issued: 2026-09-24
- prompt: active/euclid_dr1_positions_finder.md
- session: claude (Fable CLI, 2026-09-24)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/euclid-dr1-positions-finder
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-dr1-positions-finder
- summary: Phase 2/3 of the positions work: model-guided finder (compute peaks, fixed-centre SIE+shear quick fit, numpy forward solve, reconcile, iterate) in a shared pure-numpy module used by segmentation.py, util.py and the gate. Witness: human-approved 10-lens sample in euclid_dr1 inspect/positions_sample, then the census.
- parallel-claim: "2026-09-24 human go: own worktree alongside #103 (branch stacked on feature/euclid-dr1-positions-gate, PR #104 open unmerged, deliberate dependency; retarget to main after merge) and #102 (disjoint files: catalogue/, inspection bundle). Brain sized too-large/4-phase; human approved one task, one PR."
- pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/106 (base feature/euclid-dr1-positions-gate; retarget to main after #104 merges)
- heart-red-override:
  - authorization: live user 2026-09-25 answered "Override, open the PR" to the named #105 development override (push + open PR; merge stays human via /prm)
  - red-reasons: `release validation FAILED (stage integrate)`; `workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more)`; `manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml`
  - passed: pytest 139 (not slow) incl. 9 new rewrite_positions tests at 53cc0d3; 150/150 regression vs the human-approved old-vs-new comparison
- resume: PR #106 open (3 new commits a195033/b8e8d79/53cc0d3 add rewrite_positions.py + segmentation.write_positions). Rollout plan approved 2026-09-25: human /prm #104 then #106 -> sync RAL pipeline -> rewrite_positions priority pass on the first 250 dr1_sep1_rest tiles (sorted) -> full dr1_sep1_rest + dr1_sep1_top1000 CPU array -> rsync rest positions back to local. RAL output for the 10 rest_01 lenses deleted for a fresh start (Tile102004820… left: job 350664_6 still running, human to scancel).

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
