Linear-solver programme phase 4a (research): why `pdip_jacobi` — the library `"jacobi"` preconditioning, the Mapper default — follows different trajectories batched (`jit(vmap)`) and unbatched on the A100 only.

**Shipped:** autolens_profiling#398 (merged 2026-10-08), issue autolens_profiling#397. New dataset-free probe `scripts/lens/solver/batched_divergence.py` (determinism, vmap lowering vs lane count, tiled lanes, first-difference trajectory via the library's `max_iter=k`, cond(Q) join), lint smoke line, `hpc/batch_gpu/submit_lens_solver_batched_divergence_a100_fp64`; artefacts `results/lens/solver/batched_divergence_summary_all{,_gpu,_gpu_det}_v2026.10.7.1.*` (laptop CPU from tag worktrees; A100 job 399050 on euclid-ral-gpu-2, 2:30, default and `--xla_gpu_deterministic_ops=true`); wiki research page `wiki/research/jacobi_a100_batched_divergence.md` with a decision table; ledger section "Phase 4a (2026-10-08)"; campaign page row and Next line.

**Result:** the difference is deterministic (batched reruns, fresh jit and the deterministic-ops run are bit-identical: 0/50 lanes differ) and not a `vmap` defect (B=1 through `jit(vmap)` equals plain `jit`; tiled lanes agree with each other). The batched A100 `cho_factor`/`cho_solve` differ from the single solve on 50/50 lanes from jaxnnls `initialize` (k=0) at ‖Δy‖/‖y‖ = 1.1–2.1e-15; the matrix-vector product and Jacobi scaling are identical; CPU never differs. 26 quiet lanes stay ≤ 8.2e-13 for 50 iterations with identical flags; 24 sensitive lanes reach order one within 1–2 iterations and contain all 20 members of the phase-3a Jacobi divergence set plus 4 always-convergent lanes. Controls `pdip_raw` ≤ 1.3e-13 and `certified` ≤ 3.4e-12 with identical iterations and flags. cond(Q) does not predict sensitivity (AUC 0.61 / 0.56). Explanation supported: batch-shape-dependent Cholesky rounding on the A100, amplified by Jacobi's unstable systems — on them, whether a run converges follows the rounding. Decision table: B (deterministic flag) ruled out; C (tolerance/cap) not expected to help; A (keep and document) or D (move the Mapper GPU default to raw+polish or certified) need a Mapper corpus; E (one lowering) gives bit-parity, not stability. No default, pin or tolerance changed.

**Not established:** which GPU kernels the two Cholesky paths select; whether the phase-3a CPU-vs-A100 divergence sets differ for the same reason; whether Mapper systems fall in the sensitive group; why 4 convergent lanes are sensitive.

**Caveats:** per-element `max_ulp_*` fields in the committed A100 JSONs are rounded to ~512–1024 ulp by a probe bug fixed post-run (663a7d8; one A100 job authorised, no rerun) — relative norms and bitwise comparisons are exact and every quoted number is one of those. RAL sibling worktree `/mnt/ral/jnightin/autolens_profiling_wt/linear-solver-p4a` created (p3b blocked by untracked artefacts) and left with the job logs. Shared mirror untouched.

**Remainder:** phase 5 (Mapper corpus — human option 2, 2026-10-08) filed as `draft/research/autolens_profiling/linear_solver_phase5_mapper_corpus.md`. 4b (kernel-selection probe) deferred, only if bit-parity becomes a requirement. Pulse task: mge_nnls_fix_pyautoarray_571_slam_60.

## Original prompt

# Linear-solver programme phase 4: why Jacobi PDIP trajectories diverge between batched and unbatched solves on the A100 only

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
Filed: 2026-10-08
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/397
Depends-on: complete/2026/10/linear-solver-p3b-gpu-timing.md (phase 3b rows and the finding)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md

## Original request (chat 2026-10-08)

"I think the phase 4 makes sense to do the research and have it in the wiki for future decision making."

## The finding (phase 3b, autolens_profiling#396)

On the A100 at tag 2026.10.7.1, `pdip_jacobi` (the library `"jacobi"` preconditioning mode — the
default with a Mapper, i.e. every pixelized inversion) solved inside `jit(vmap)` over 50 distinct
SLaM systems follows a different trajectory from the same systems solved one at a time: 19/50 lanes
differ in iteration count and 13/50 in the convergence flag (4/50 unconverged batched vs 13/50
unbatched). On CPU the batched and unbatched trajectories are bit-identical. The released raw PDIP
(`pdip_raw`) is identical on both devices in both modes (|Δ flux_inactive_rel| ≤ 1.4e-14). Phase 3a
had already shown that *which* systems Jacobi diverges on is device-dependent (29 CPU vs 19 A100)
while *that* it diverges is not.

## Why it matters for a future decision

Jacobi is not the MGE default any more (PyAutoArray#571/#595), but it is the preconditioning every
pixelized (Mapper) inversion uses. If GPU batched and unbatched solves follow different paths, a
Nautilus `vmap` batch on the A100 and a single-evaluation re-fit of the same parameters are not the
same computation — reproducibility, convergence-flag semantics and any CPU-vs-GPU parity test for
pixelized fits inherit this. The decision this research prepares (not takes): whether the Mapper
default should move off Jacobi on GPU, whether a determinism flag or a tolerance change is needed,
or whether the effect is confined to already-diverging (ill-conditioned) systems and can be
documented and left.

## Scope — research only, no library change

1. **Reproduce and localise** on the corpus with the phase-3b cell and a small probe script
   (`scripts/lens/solver/batched_divergence.py`, dataset-free, `_driver` pattern):
   - determinism: run the batched A100 solve twice (and with `--xla_gpu_deterministic_ops=true`);
     bit-identical or not?
   - B=1 through `jit(vmap)` vs plain `jit`: does the vmap lowering alone change the result, or does
     it need B>1 (batched cuBLAS/cuSOLVER kernels)?
   - tiled batch (one system × B): are the lanes identical to each other and to the unbatched solve?
   - `pdip_raw` and `certified` under the same probes as controls (well-conditioned paths).
2. **Per-iteration trajectory** of a few differing lanes (dump the iterate, step length and
   complementarity per PDIP iteration via the library's status primitives, no transcribed
   internals): at which iteration do batched and unbatched first differ, how large is that first
   difference (ulp-level rounding vs an algorithmic branch), and how does it grow?
3. **Condition dependence**: correlate the lanes that differ with cond(Q), the Jacobi-scaled
   condition number and the phase-3a divergence set.
4. **Write-up** as a wiki research page in autolens_profiling (`wiki/research/` or beside the
   campaign page), linked from `wiki/campaigns/linear_solver_accuracy.md`: question, method,
   evidence table, the explanation the evidence supports (or that it does not yet), and a decision
   table (options × consequences) for the human. Rows appended to the ledger
   `results/notes/linear_solver_accuracy_2026_09.md`. No defaults, pins or tolerances change here.

## Witness

The probe's JSON on CPU (identical lanes expected) and A100, plus the wiki page; `ruff`,
`build_readme.py --check`, lint smoke entry for the probe.

## Compute

One A100 job (minutes) from the private base `/mnt/ral/jnightin/PyAuto_wt/linear-solver-p3`
(RAL profiling worktree `autolens_profiling_wt/linear-solver-p3b`); CPU rows on the laptop from
tag worktrees. Needs separate compute authorization.
