# Point-source A100 campaign — phase 0+1 (lean): baseline + bottleneck map on current main

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-28
Issued: 2026-09-28
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/350
Parent-record: draft/research/autolens_profiling/point_source_image_plane_gpu_breakdown.md (campaign contract; stays as campaign intent)

## Original request (verbatim, 2026-09-28)

continue cut-triangle-gather-jax noting autgolens profiling updates

point solver c[u stuff but may be on gpu now?

ok go and follow the recommendation

(The recommendation: one lean A100 phase on current main — device trace, vmap 1/4/16/64/256 throughput + memory, mixed-precision row, forward-mode gradient — skipping the preserved-unoptimized-revision reproduction because the CPU campaign's A100 rows 350587/350637/357322/359102 already cover it; then a human go/no-go on phase 2 against the likelihood-share-of-a-fit admission bar from the 2026-09-27 profiling review.)

## Plan

## Context

The single-source PointSolver CPU campaign is complete (IP-2/3/4b/4c shipped; #580/#584/PyAutoLens#753 merged, unreleased). Its A100 no-regression rows show the GPU call is **launch-bound**: 0.83 ms scalar, 0.23 / 0.07 ms/L under vmap-4 / 16, flat under FLOP-halving levers (jobs 350587, 350637, 357322, 359102). The GPU sibling campaign (`draft/research/autolens_profiling/point_source_image_plane_gpu_breakdown.md`, wiki `point_source_gpu_breakdown.md`) is unstarted.

Human decision 2026-09-28: skip the contract's phase-0 reproduction of the preserved unoptimized revisions (the CPU-campaign A100 rows already cover it); run **one** A100 job on current main measuring what is still unknown, write the upper bound for the phase-2 levers, and stop at a **human go/no-go** judged against the 09-27 review's admission bar (likelihood share of a fit). autolens_profiling only — no library edits.

## Mind / issue

- Phase prompt `draft/research/autolens_profiling/point_source_gpu_p01.md` (request verbatim + this plan; parent = the campaign draft, which stays as campaign intent). `/create_issue` on autolens_profiling, title `research: point-source A100 phase 0+1 — launch-bound bottleneck map on current main`.
- Task `point-source-gpu-p01`, branch `feature/point-source-gpu-p01`, worktree `~/Code/PyAutoLabs-wt/point-source-gpu-p01/autolens_profiling`. Conflict guard clean (other autolens_profiling worktrees — mass-field-profiling-live, Codex abell-1201-data — touch other folders).
- Register `workspace-dev` in active.md; route `/start_workspace`.

## Implementation (delegated to one Opus subagent, progress file + Monitor)

New cell `scripts/point_source_image/likelihood_breakdown/gpu_bottleneck_map.py`, reusing (import, not copy) the solver_config_sweep.py builders: `_solved_model`, `make_solver` (control cfg), `loglike_factory`, `_vector_stream(seed=314)`, `register_model_pytrees`, `compile_route`, `_median_ratio`, `FIDUCIAL_SOLVED_LOG_L_BY_BACKEND`; helpers `_profile_cli.py`, `provenance.py`, `timing.block`. If importing the sweep script is awkward, lift the shared builders into a small `_point_source_image_common.py` with the sweep re-importing them (behaviour-preserving; sweep output unchanged).

Legs (all on the default `structured`, MCS 20 current-main solver, fp64 unless stated):

1. **Baseline** — lower / compile / first-call / warm (20 rounds × 20 calls, varying stream inputs, `block_until_ready`), with command buffers (CUDA graphs) ON (default) and OFF. Fiducial bit-exact gate (GPU `…806`).
2. **vmap scaling** — batches 1/4/16/64/256 (stop early on OOM): ms/L, throughput, compile s, XLA temp bytes, device `memory_stats()` peak; `max_abs_delta_vs_scalar` gate.
3. **Device trace** — `jax.profiler.trace` on the command-buffers-OFF executable (fixed_light_trace.py precedent) parsed with `scripts/misc/likelihood_breakdown/xla_attribution.py` (`device_events`, `split_calls`, `idle_gaps`, `hlo_census`). Report per call: **kernel count**, device-busy ms vs wall ms (→ launch/host fraction), idle-gap distribution, and per-stage attribution via a **new point-solver `STAGE_MAP`** (step-0 containment, per-step deflections / containment / neighbourhood / up_sample / dedup-sort, magnification filter, χ², other) keyed on source frames in PyAutoArray `structures/triangles/` and PyAutoLens `point/solver/`. Unit test for the stage map in `scripts/misc/test/`. Scalar and vmap-16.
4. **fp32 what-if row** — the PointSolver has no mixed-precision switch, so this is labelled explicitly as a whole-program `JAX_ENABLE_X64=0` run (separate process in the same job): timing + |Δ log L|, image count and max position Δ vs fp64 over the stream. Evidence of headroom only, not a supported mode.
5. **Gradient** — reverse `jax.value_and_grad` and forward `jax.jacfwd` of the image-plane likelihood (5 params, through the `custom_jvp` implicit path): scalar + vmap-16 timing and compile. Quote throughput only after a central finite-difference agreement check at smooth stream points (report rel. error per param; flag topology-transition points rather than failing on them).

Output: `results/breakdown/point_source_image/gpu_bottleneck_map_hpc_ral_a100_fp64.json` + `.png` (vmap curve, stage attribution bar, busy-vs-wall); schema = sweep style (`summary` via `_scrub`, `device.provenance`, `source_revisions`). No `autolens_version` key (like the sweep, it stays out of README tables and the dashboard).

Submit `hpc/batch_gpu/submit_breakdown_point_source_image_gpu_bottleneck_map_a100_fp64` copied from the mcs A100 template (preflight, env, revision assert), plus the fp32 second invocation; `# WALL-BASIS:` block `source: unmeasured` with headroom, updated to measured after the run.

Local laptop CPU smoke run with tiny counts (trace leg + stage map exercised on CPU) before RAL. On RAL: `HPCPullPyAuto` so the mirror carries current mains (#580/#584/#753), git-pull the profiling checkout to the branch, `hpc/sync submit --gpu …`, `hpc/sync pull`, copy JSON/PNG (+ log if it adds anything, `results/logs/point_source_image/…_ral_job_<id>_gpu_bottleneck_map.out`).

## Write-up

- Ledger `results/notes/point_source_gpu_breakdown_2026_09.md`: setup/provenance, the five tables, and a **phase-2 upper-bound section**: for each contract lever (kernel fusion / fewer launches, loop form for compile, vmap break-even, implicit-gradient Jacobian, deflections) the maximum gain the trace allows (e.g. launch-bound fraction bounds any launch-count lever; stage share bounds a stage-specific lever), vs the run-to-run MDI.
- Go/no-go memo in the same note: states the upper bounds and that no image-plane fit has been timed; the admission bar needs one autolens_inference measurement (likelihood share of an image-plane fit + eval count, batched vs serial) — recommended as the prerequisite if any lever clears MDI. Decision is the human's.
- Wiki: fill `wiki/campaigns/point_source_gpu_breakdown.md` header (Status open, Verdict, Headline with job id, Profiling PRs, Ledger, Next = go/no-go), phases table row "0+1 combined (lean)", journal entry noting the human's skip of the preserved-revision reproduction; refresh `wiki/index.md` row.

## Verification

- `ruff check` / `ruff format --check`, `pytest scripts/misc/test/`, `build_readme.py --check`, `check_wiki.py --check`, `check_results_layout.py --check`, `check_submits.py --check`, `build_dashboard.py --check` — all green locally before PR.
- JSON `all_gates_pass: true` on the A100 (fiducial bit-exact, vmap deltas, FD gradient agreement), `source_revisions` equal the mirror HEADs, backend `gpu` asserted.
- Ship via `/ship_workspace` → PR into autolens_profiling main (supervised; merge stays human). Then report the go/no-go to the human and stop.
