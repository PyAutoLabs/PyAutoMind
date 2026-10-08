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
