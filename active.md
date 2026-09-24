# Active Tasks

## mge-pdip-nnls-convergence
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/571
- issued: 2026-09-24
- prompt: active/jax_positive_only_pdip_nnls_solve_does.md
- session: Claude Code CLI (Fable 5.1), 2026-09-24
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-24 (Plan Mode); mid-task checkpoint with the human after the diagnosis step, before the fix is chosen
- worktree: /home/jammy/Code/PyAutoLabs-wt/mge-pdip-nnls-convergence
- repos:
  - PyAutoArray: feature/mge-pdip-nnls-convergence
  - autolens_profiling: feature/mge-pdip-nnls-convergence
- parallel-claim: "autolens_profiling is also claimed by certified-solver-phase-c1-lane-rate, hst-gpu-residue-p4 and point-source-cpu-p3. Disjoint file set: this task adds only scripts/imaging/hazards/mge_nnls_capture.py and results/hazards/component/mge/nnls_capture_slam_hst_*.{json,npz}; the library work is in PyAutoArray. Recorded 2026-09-24 per the residue-p1/#267 precedent, plan approved by the human in-session."
- summary: JAX PDIP positive-only solve (max_iter 50) returns unconverged garbage logL on 14/48 near-truth vectors of the SLaM source_lp[1] 60-column MGE model; capture (Q,q) fixture, red regression test vs fnnls_cholesky, diagnose plateau-vs-blow-up + certified-solver certification, then fix so non-convergence is never silent (PyAutoArray#571).

## ep-factor-search-overhead
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1642
- issued: 2026-09-24
- prompt: active/ep_factor_search_wrapper_overhead.md
- session: Claude Code CLI (Fable 5.1), session id unavailable
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/ep-factor-search-overhead
- repos:
  - PyAutoFit: feature/ep-factor-search-overhead
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1643
- library-pr-2: https://github.com/PyAutoLabs/PyAutoFit/pull/1644 (stacked on #1643, base feature/ep-factor-search-overhead; retarget to main after #1643 merges)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1643
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1644
- heart-red-override:
  - authorization: Live human 2026-09-24 (Claude Code CLI) selected "Yes, override and open PR 1" for the development-only Heart RED override on PR 1 of #1642; commit/push/pending-release PR only, no merge or release.
  - red-reasons: "release validation FAILED (stage integrate)"; "workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more)"; "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml" (readiness red, score 45, ts 2026-09-24T15:11:12Z)
  - passed: full serial test_autofit 2881 passed / 2 skipped at 16789050a; autofit workspace smoke 8/8 scripts + 2/2 notebooks; PyAutoFit main CI green; downstream impact (iii) none. Heart remains RED for release purposes.
- heart-red-override-pr-2:
  - authorization: Live human 2026-09-24 (Claude Code CLI), asked whether the override extends to opening PR 2 as a stacked PR (base = PR 1 branch, retargeted to main after PR 1 merges) and PR 3 the same way once green, selected "Yes, same override for PR 2 and PR 3"; commit/push/stacked pending-release PR only, no merge or release.
  - red-reasons: same three as PR 1 (readiness red, score 45, ts 2026-09-24T15:11:12Z).
  - passed: full serial test_autofit 2885 passed / 2 skipped at 1cd4a5b85; new EP-visuals tests red on PR 1 source; EP harness moments bit-identical to PR 1; downstream impact (iii) none. Heart remains RED for release purposes.
- resume: PR 1 (#1643) open awaiting human /prm; PR 2 (#1644, EP visuals) open stacked on #1643, retarget to main after #1643 merges then /prm; PR 3 (mapper fast path) in progress on feature/ep-factor-search-overhead-p3.

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
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/euclid-dr1-positions-gate
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-dr1-positions-gate
- summary: Pre-submit positions gate: 0.15" central cut, quick SIE+shear fit with one-image leave-one-out drop, per-tile threshold T=min(max(2 s_min,0.3),0.5) in a positions_meta.json sidecar read by load_vis_dataset. Phase 1/3; runs in its own worktree alongside #102 (disjoint files).
- resume: Worktree created; implementation (scripts/tools/positions_gate.py, util.py sidecar read, tests, submitter) delegated to Opus in-session; then /ship_workspace.

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
- status: awaiting-merge
- autonomy: supervised (header); plan approved in-session 2026-09-24
- worktree: /home/jammy/Code/PyAutoLabs-wt/hst-gpu-residue-p4
- repos:
  - autolens_profiling: feature/hst-gpu-residue-p4
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p3 (feature/point-source-cpu-p3). Disjoint file sets: this task edits scripts/imaging/likelihood_breakdown/fixed_light_trace.py and scripts/misc/likelihood_breakdown/xla_attribution.py, adds scripts/misc/likelihood_breakdown/logdet_reuse_injection.py, hpc/batch_gpu/submit_breakdown_imaging_fixed_light_logdet_reuse_a100_hst_fp64, tests under scripts/misc/test/ and results/notes/hst_gpu_residue_phase4_logdet_2026_09.md; that task touches point-source scripts/results. Recorded 2026-09-24 per the residue-p1/#267 precedent."
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/306
- commit: autolens_profiling 83e27e1 (feature/hst-gpu-residue-p4, pushed) — PR https://github.com/PyAutoLabs/autolens_profiling/pull/306 (pending-release, lint green); 71e3f21 cell+injection+gate, 5f6f8c7 schur_k256 amendment, a621160 RTX screen, 83e27e1 A100 harvest + verdict note
- hpc: RAL A100 array 350651 (8 tasks) harvested 2026-09-24, 8/8 rc 0, gate PASS 8/8; RAL autolens_profiling checkout back on main 9ad12ab
- heart-red-override: "2026-09-24 live human \"yes i authorize\" to the named #303 development-only override (push + open PR + four-sink record + campaign-map update; merge excluded). RED reasons at push: `release validation FAILED (stage integrate)`; `workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more)`; `manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml`. Branch gates passed on 83e27e1: pre-registered gate 8/8 rows (72/72 pins, worst 3.7e-10), recon -0.43..-0.60 %, unjoined 0; ruff check+format, build_readme --check, check_submits clean; pytest scripts/misc/test 886 passed / 5 skipped. Recorded on #303 (issuecomment-5817533377) and PR #306."
- next: "human /prm 306 (merge + close #303). Verdict NO LEVER: the Schur path's triangular solve vs the 1500x1500 factor costs 0.97-1.05 ms at every k >= 32, more than the 0.90 ms dense Cholesky; campaign fp64 levers exhausted."
- summary: Phase 4 of hst-gpu-non-solver-residue: harness-only reuse of the library certified solve's masked Cholesky + a bounded Schur complement over the fixed set for log det(F+λH) (0.89 ms ceiling, 2.8 %), pinned at 1e-9 vs the library; PyAutoArray prompt only if >= 0.5 ms whole-call.
