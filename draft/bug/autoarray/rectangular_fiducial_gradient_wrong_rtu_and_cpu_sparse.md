# Wrong JAX gradient through the rectangular source mesh: RTU (all backends) and Bilinear on the CPU sparse path

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on imaging/rectangular/hst fiducial (39x39, no --standard-size) value_and_grad agrees with the central-difference plateau (steps 1e-4..1e-7, 3 seeded directions) to <= 1e-3 relative for RectangularRTU on CPU sparse and A100 dense and for Bilinear on CPU sparse, and CPU/A100 gradients agree
Review-minutes: 10
Unattended: never
Filed: 2026-11-02

Found during likelihood-lifecycle phase 6c (autolens_profiling#509), RTU vs Bilinear side run. Libraries at tag 2026.10.25.1. Human: "yes" (file it), 2026-11-02.

## Symptom

Cell imaging/rectangular/hst, fiducial 39x39 (no `--standard-size`), campaign leg-11 flags, `gradient_breakdown.py --gradient`, mesh via `--rect-mesh`.

- **RTU (kernel-CDF)**: the likelihood is smooth. Along the 3 seeded unit directions the central difference plateaus at about -2895 / 1237 / 2530 over steps 1e-4..1e-7. Autodiff gives 5.6e7 / -1.6e8 / 5.6e7 on A100 dense (RAL 413870) and -1.8e8 / 5.9e7 / 7.1e7 on CPU sparse (RAL 413868), with |g| ≈ 2e9. The two backends differ in sign, while log L agrees to 1e-10.
- **Bilinear (rank-CDF)**: A100 dense gives |g| 3.3e4, consistent with the FD at h=1e-3 (413869). CPU sparse gives |g| 6.5e10 and an analytic directional derivative of -2.4e9 against an FD of -4386 (413867).
- Control: on the 74 standard-size v2 campaign legs (RAL 413791-413830), CPU and A100 |g| are identical on every cell, including imaging/rectangular at all 4 instruments.

The value is right and only the gradient is wrong, so the bug is in the derivative path: a near-singular term (sqrt / division / `where` guard at a degenerate point) in the RTU kernel CDF, or in the sparse mapping-matrix construction that the CPU path uses. Which one is open.

## Evidence

- `~/Science/Science/scratch/delaunay_hilbert_2026-11-01/rtu_vs_bilinear/{rtu,bilinear}/results/imaging/rectangular/hst/{jax_cpu_sparse_fp64/hpc_ral_cpu,jax_gpu_dense_fp64/hpc_a100}/gradient.json`
- `~/Science/Science/scratch/delaunay_hilbert_2026-11-01/results/rectangular_hst_rtu_fiducial/probe.json` (13-step FD sweep + log L slices, A100); write-up in that folder's README.md.
- RAL: /mnt/ral/jnightin/profiling/autolens_profiling_p2dg/output/p6_gradient_rtu/.

## Suggested first step

Reduce to a CPU-reproducible unit test: per-parameter gradient vs FD on the fiducial cell to find which parameters carry the huge components (mesh weights, lens mass, or lens light), then bisect the RTU / sparse mapper path with `jax.debug` / `jax.grad` on intermediate quantities.
