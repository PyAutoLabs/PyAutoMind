# Linear-solver programme phase 3a: A100 parity of the solver corpus from a private tag checkout

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- linear-solver
- gpu
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Status: active
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/393
Filed: 2026-10-07
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md
Campaign: https://github.com/PyAutoLabs/autolens_profiling/blob/main/wiki/campaigns/linear_solver_accuracy.md

## Original request (verbatim, chat 2026-10-07)

> dont HPCPyAutoPull the main RAL repo though... its needed for euclid_dr1

Then, to the proposed plan ("Clone the five libraries at tag 2026.10.7.1 into a private
directory under the RAL home ... Parity cell first ... Timing cell second ... Rows and verdict
go to the solver ledger and the campaign wiki page"): "I agree".

## Scope (phase 3a — parity only; the timing cell is phase 3b, `linear_solver_phase3b_gpu_timing_cell.md`)

1. **Private RAL base.** Clone PyAutoNerves/Fit/Array/Galaxy/Lens at tag `2026.10.7.1`
   (contains PyAutoArray#595) under `/mnt/ral/jnightin/PyAuto_wt/linear-solver-p3/` and a
   worktree of autolens_profiling beside it. Never touch `/mnt/ral/jnightin/PyAuto`. Reuse the
   shared venv (jax 0.10.2) via `activate.sh`, then prepend the private checkouts to
   `PYTHONPATH`; export `PYAUTO_HPC_BASE` to the private base so the in-job import guard
   proves provenance. Hazard: Nerves' `!=0.10.*` jax exclusion is install-time metadata for a
   CPU batched-LAPACK deadlock; the GPU leg uses stored CPU fnnls references, so no CPU batched
   solve runs in the job. Record jax/jaxlib versions in the SLURM log.
2. **Parity cell (existing code).** `scripts/lens/solver/accuracy.py --device gpu` over the
   81-system corpus on one A100 (fp64); a new `hpc/batch_gpu/submit_lens_solver_accuracy_a100_fp64`
   following the package's submit pattern. Score with `flux_inactive_rel`, amplitude agreement
   and iterations per lane against the stored CPU fnnls references; report max |logL_gpu − logL_cpu|
   as context only.
3. **Records.** Append rows and a verdict to `results/notes/linear_solver_accuracy_2026_09.md`
   and `wiki/campaigns/linear_solver_accuracy.md`; regenerate README dashboards
   (`build_readme.py --check`). Any regression routes to /intake as a bug. Pulse task flips on
   that evidence; no baseline pin moves.

## Authorization

The human authorized (chat 2026-10-07) the development task and the A100 parity job from the
private checkout. CPU arrays, if any, use `--partition=ral` only. The timing cell (phase 3b) is a separate start_dev.
