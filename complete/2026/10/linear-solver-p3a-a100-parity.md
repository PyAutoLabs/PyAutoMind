Linear-solver programme phase 3a: A100 parity of the 81-system solver corpus from a private RAL checkout at tag 2026.10.7.1 (human rule 2026-10-07: the shared mirror `/mnt/ral/jnightin/PyAuto` is never synced while euclid_dr1 depends on it).

**Shipped:** autolens_profiling#394 (merged 2026-10-07T21:18Z, `a55dcacb`), issue autolens_profiling#393. New `hpc/batch_gpu/submit_lens_solver_accuracy_a100_fp64`; artefacts `results/lens/solver/accuracy_summary_all_v2026.10.7.1.*` (laptop CPU) and `accuracy_summary_all_gpu_v2026.10.7.1.*` (A100 job 397475, euclid-ral-gpu-1, 1:04); ledger section in `results/notes/linear_solver_accuracy_2026_09.md`; campaign page row 3 and Next → phase 3b.

**Result:** parity holds for the released raw PDIP solver — CPU vs A100 max |Δ flux_inactive_rel| 5.4e-14, max |Δ amp_rel_max_sig| 4.0e-10, iterations identical on 81/81. It remains inadmissible under the pre-registered rule on both devices for the phase-2 reasons. Device disagreements reported (not explained): `pdip_jacobi` diverges on 29 (CPU) vs 19 (A100) systems; `pdip_raw_tol_jaxnnls` flips one convergence flag at the cap. No baseline pin moved. Private library checkouts: Nerves c5ade605, Fit 710f4b34, Array ccddfba6, Galaxy b4946b8a, Lens b6bf543c; jax/jaxlib 0.10.2 (Nerves install metadata excludes 0.10.*; no CPU batched solve in the job).

**Hazard:** a tag source checkout stamps `al.__version__ = 2026.8.17.1`, so a re-run overwrites the committed `_v2026.8.17.1` artefact; write to `--output-dir` and copy to the release name.

**Remainder:** phase 3b (GPU/vmap timing cell) filed as `draft/research/autolens_profiling/linear_solver_phase3b_gpu_timing_cell.md`; the private RAL base and worktree `/mnt/ral/jnightin/autolens_profiling_wt/linear-solver-p3` are left for it. Pulse task: mge_nnls_fix_pyautoarray_571_slam_60.

## Original prompt

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
