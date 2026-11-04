## rectangular-gradient-rtu-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/671
- completed: 2026-11-02
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/672
- summary: the filed symptom (|g| ~2e9 on the imaging/rectangular/hst fiducial, RTU all backends, Bilinear CPU sparse) split into two causes. (1) Not a library bug: on the 141x141 (odd) HST grid at os_pix=1 a source-grid point sits exactly on the Isothermal centre at prior medians, and the `psi` softening (+1e-16, a 1e-8 core) gives d(deflection)/d(centre) ~1.5e8, which is exact for the softened function but beyond what FD can resolve. Nudging the centre 1e-5 dropped |g| to 2.4e5. The evaluation-point fix was handed to autolens_profiling#509 (p6c). (2) Library bug, fixed: `ellipse_params_via_border_pca_from` took `b = max(|y'|)`. A lens on the mask's symmetry centre gives exact +/- border-pair ties, and JAX's equality-based `max` tie gradient is unstable under `jit` reverse mode (2x / 0.5x; eager correct). The new `max_at_argmax_from` gathers the element at the argmax: values unchanged, one-hot gradient. On the jitted MGE-medians repro einstein_radius went from 25.46 to 24.183 (FD 24.183).
- scope change (human, 2026-11-02): re-scoped from "RTU kernel-CDF / sparse mapper" to the few-% error once (1) was diagnosed; autolens_profiling not claimed (held by p6c), used read-only.
- traps: MGE looked like the trigger but only the jitted Fitness path shows the bug; stage bisection needs reverse mode (NNLS is custom_vjp, so jvp fails), and per-slot weight FD comparisons are invalid for points exactly on a mesh line (corner relabelling). Kernel-CDF lo/hi and std().min() were tested under exact ties with no jit divergence, so they were left unchanged. Small standalone graphs do NOT reproduce the jit tie bug (it needs XLA fusion of the tracer graph), so the regression test asserts the one-hot property instead. The real HST cell needs XLA_FLAGS=--xla_disable_hlo_passes=constant_folding locally (compile OOM otherwise).
- follow-ups filed: draft/research/autolens_profiling/gradient_campaign_impact_of_border_tie_and_centre_singularity.md (human request: campaign impact), draft/bug/autoarray/sparse_vs_dense_log_likelihood_mismatch_nonlinear_lens_light.md.
- witness: the prompt Witness (HST fiducial FD agreement) is not reachable until #509 moves the fiducial evaluation point off the grid; fix proven on jax_test (jitted) + autolens_workspace_test jax_grad/pixelization.py passed.
- heart: shipped on STALE ("release validation incomplete: no rehearsal for current source"), human-acknowledged.
- repro: Science/scratch/rectangular_gradient_rtu_sparse_2026-11-02/

## Original prompt

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
Issued: 2026-11-02

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
