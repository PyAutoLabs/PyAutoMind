Linear-solver programme phase 3b: the `jit(vmap)` timing cell for the solver corpus, CPU and A100, from the private RAL checkout at tag 2026.10.7.1 (shared mirror `/mnt/ral/jnightin/PyAuto` untouched; euclid_dr1 arrays were running on it).

**Shipped:** autolens_profiling#396 (merged 2026-10-08T08:26Z, `86cb1460`), issue autolens_profiling#395. New `scripts/lens/solver/timing.py` and `_solvers.batched_kernel` (existing `fn`/`kernel` untouched), lint smoke line, `solver-timing` README auto-table, `hpc/batch_gpu/submit_lens_solver_timing_a100_fp64`; artefacts `results/lens/solver/timing_summary_all_v2026.10.7.1.*` (laptop CPU, tag worktrees) and `timing_summary_all_gpu_v2026.10.7.1.*` (A100 job 398249, euclid-ral-gpu-2, 0:38); ledger section "Phase 3b (2026-10-08)" in `results/notes/linear_solver_accuracy_2026_09.md`; campaign wiki row and Next line.

**Result** (per-evaluation minimum ms over 7 interleaved rounds of batched wall ÷ B, fp64; SLaM batches are distinct fixture+slam48 systems, euclid lanes are tiled copies of one system): `pdip_raw` CPU 1.353 / 0.881 / 0.682 and A100 3.948 / 0.581 / 0.190 at B = 1 / 16 / 50; `pdip_jacobi` CPU 2.488 / 1.630 / 1.396 and A100 6.715 / 1.149 / 0.369. Compile walls 0.3–1.2 s recorded separately (first call per config). Batched `pdip_raw` reproduces the unbatched phase-3a rows on every lane (|Δ flux_inactive_rel| ≤ 1.4e-14, identical iterations and flags). Slowest-lane mechanism confirmed: a vmapped `while_loop` costs its slowest lane, and one diverging Jacobi lane pins the batch at the 50-iteration cap (A100 B=16/50), so Jacobi costs 1.94x the released solver at A100 B=50. **New, unexplained:** `pdip_jacobi` batched vs unbatched trajectories differ on the A100 (19/50 lanes in iterations, 13/50 in the convergence flag) and are identical on CPU — reported in the ledger without explanation. A timing is not admissibility; no baseline pin moved.

**Caveats:** euclid lanes measure throughput only; the A100 used the warm shared JAX compile cache (`cache_fresh: false`); laptop under background load (loadavg ~1.9); the CPU batched run used jax 0.10.2 (Nerves-excluded for the batched-LAPACK deadlock, Heart#274; none occurred); source checkouts stamp 2026.8.17.1, so both runs wrote to scratch and were copied to the `_v2026.10.7.1` names. Job logs not committed (scratchpad only). RAL sibling worktree `/mnt/ral/jnightin/autolens_profiling_wt/linear-solver-p3b` created because the p3 one held untracked (byte-identical) 3a artefacts.

**Remainder:** phase 3 was the last filed phase of the programme. Phase 4 (research: why Jacobi batched and unbatched trajectories diverge on the A100 only, written up for a future decision) is filed as `draft/research/autolens_profiling/linear_solver_phase4_jacobi_a100_batched_divergence.md`. Pulse task: mge_nnls_fix_pyautoarray_571_slam_60.

## Original prompt

# Linear-solver programme phase 3b: GPU/vmap timing cell for the solver corpus (A100, private tag checkout)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- linear-solver
- gpu
Difficulty: moderate
Autonomy: supervised
Priority: medium
Consequence: judge
Status: active
Filed: 2026-10-07
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/395
Depends-on: complete/2026/10/linear-solver-p3a-a100-parity.md (private base + parity rows; shipped autolens_profiling#394)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md

## Original request (chat 2026-10-07)

The human agreed to the phase-3 plan: "Timing cell second: the task asks for a new timing cell
(single, vmap16, vmap50 per evaluation, jacobi versus raw preconditioning, interleaved minima) on
the SLaM 60-column system and the euclid capture."

## Scope

- `scripts/lens/solver/timing.py` on the `_driver` pattern: single, vmap16 and vmap50
  per-evaluation cost on the SLaM source_lp[1] 60-column system (`slam_fixture_571`) and the
  euclid capture (`euclid_vis_lp`), fp64, candidates `pdip_jacobi` and the released raw PDIP
  (`pdip_raw_polish`), interleaved minima; compile time reported separately from steady
  per-call cost; NNLS share via `stats["iterations"]`.
- CPU smoke locally (lint.yml smoke list), then one A100 submit script from the phase-3a private
  base. The RTX 2060 leg is optional laptop compute.
- Rows and verdict appended to `results/notes/linear_solver_accuracy_2026_09.md` and the campaign
  wiki; `build_readme.py --check`.
