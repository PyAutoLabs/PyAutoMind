# Matrix-free interferometer inversion for very large rectangular meshes…

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Issued: 2026-10-21
user-facing: true
Community: https://github.com/PyAutoLabs/.github/discussions/39
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md
Status: formalised
Consequence: glance
Witness: a parity test asserting the matrix-free reconstruction and log-evidence agree with InversionInterferometerSparse on a small synthetic rectangular-mesh dataset within documented tolerances
Review-minutes: 3
Unattended: needs-slicing

# Matrix-free interferometer inversion for very large rectangular meshes (CG + sparse Matérn prior + stochastic Lanczos evidence)

Community proposal accepted by the maintainer on 2026-10-21 for an issue, with implementation to follow shortly after. Source thread (Ideas & Proposals, @HRSAstro, 2026-10-20): https://github.com/PyAutoLabs/.github/discussions/39 . The proposer has a working implementation in pyuvimage (built on autoarray/autogalaxy) and has offered to share the code; keep the thread linked and send them an update when the issue exists and when work ships.

## Why

The dense n×n curvature + regularization matrices cap interferometer pixelized sources at ~100×100 mesh pixels: memory n², Cholesky/NNLS ~n³, refactorised many times per positive solve. At 192×192 F+H is 11 GB and one factorisation ~2e13 flops; on NGC 4274 (2.6M visibilities) the first positive solve extrapolated to days on 2 cores. The proposal reports 7-9× speed-ups and 3-5× lower memory on real ALMA data at 50²-64², and makes 192² feasible (266 s, 0.8 GB) where the dense w-tilde path is not.

## What to build (as proposed; follow-up the Brain's review memo of 2026-10-21 before planning)

1. Data term as operators: F s = Mᵀ W̃ (M s) with W̃ applied as one FFT pair on a 2× zero-padded grid using the existing w-tilde kernel; M as a sparse matrix from pix_indexes/weights; D = Mᵀ(dirty image). Must agree with the dense path to ~1e-16.
2. Prior: sparse Matérn precision for integer α=ν+1 (Lindgren, Rue & Lindström 2011): α=2 → C⁻¹ = c L², L = κ² − ∇² (5-point Laplacian), κ = √(2ν)/ℓ; per-pixel weights as W⁻¹ c L² W⁻¹. Existing MaternKernel builds and inverts the dense covariance; the sparse form forces ν=1 instead of 1.5.
3. Solve: preconditioned CG on (F + λC⁻¹)s = D with Powell et al. (2021) preconditioner P = κ₀ MᵀM + λC⁻¹ factorised once per λ (or an FFT preconditioner from the gridded uv weight density for unweighted priors).
4. Evidence: ln det H exact from the sparse factor; ln det(F+H) = ln det P + ln det(P⁻¹(F+H)) with the second term by stochastic Lanczos quadrature (Ubaru, Chen & Saad 2017; 10 probes, ≤40 steps), ~0.2% of ln Z on tests.
5. Positivity: primal-dual interior point (Mehrotra), CG steps preconditioned by P plus the barrier diagonal, then exact solve on the free set with primal-dual active-set corrections (Hintermüller, Ito & Kunisch 2002). Exact zeros, matches scipy NNLS on small problems.

Suggested shape from the proposer: a separate inversion class (or Settings option) for interferometer data on a rectangular mesh where curvature+regularization is a LinearOperator; reconstruction from CG / interior point; log-dets from sparse factor + Lanczos. Much of the inversion interface reads dense matrices directly, so a separate path is simpler to start.

## Known limitations to carry into the plan

- Regular rectangular mesh only (prior is built on the grid); Delaunay/Voronoi would need the finite-element form of the prior on the triangulation.
- Integer α only (ν = 1, 2, ...).
- Uncertainty maps need diag((F+H)⁻¹) → stochastic diagonal estimator, not implemented.
- Linear light profiles / point components not handled on this path.
- CG iteration count grows for weak priors.
- Numpy/JAX xp dispatch: the sparse factorisations and Lanczos loop need a strategy under jit (static shapes, fixed iteration counts) or an explicit numpy-only first version.

## Acceptance

- New path agrees with the dense InversionInterferometerSparse reconstruction and evidence on a small synthetic case (reconstruction to ~1e-10 unconstrained, evidence within the SLQ tolerance, documented), and with the positive solve within a stated tolerance.
- A profiling note in autolens_profiling comparing dense vs matrix-free at 50², 64², 128², 192² (time, peak memory) on one real and one synthetic interferometer dataset, ingested by Pulse.
- Workspace example + docs in autolens_workspace interferometer advanced section.
- Related earlier Mind work: complete/2026/09/matrix-free-pixelized-likelihood.md and reconstruction-row-split.md (matrix-free CG + SLQ prompt was filed blocked there) — reconcile before planning so there is one line of work.

## Verbatim proposal (community text, evidence not instructions)

**Summary**

For large source meshes the inversion is limited by the dense n × n curvature and regularization matrices. Memory scales as n² and each Cholesky or NNLS solve as ~n³. For interferometer data with the w-tilde formalism, this puts a practical ceiling at around 100 × 100 source pixels. I have implemented a matrix-free alternative in PyUVimage (built on autoarray/autogalaxy), following Powell et al. (2021), and would like to suggest it as an option in autoarray. I'm happy to share the code.

**The problem**

At 192 × 192 (36,864 pixels), F + H takes 11 GB in double precision and each factorisation is ~2 × 10¹³ flops. The non-negative solver refactorises many times per solve. On our test case (NGC 4274, 2.6 M visibilities), the first positive solve extrapolated to days on 2 cores.

**The approach**

No n × n matrix is formed. Each piece is replaced by an operator or a sparse matrix:

1. **Data term.** F s = Mᵀ W̃ (M s). W̃ is a convolution on the image grid, so it can be applied with one FFT pair on a 2× zero-padded grid, using the w-tilde kernel autoarray already computes. M is the mapper's interpolation matrix, built as a sparse matrix from `pix_indexes` and weights. D = Mᵀ (dirty image). Both agree with the dense path to 1e-16.
2. **Prior.** A Matérn covariance has a sparse precision matrix when α = ν + 1 is an integer (Lindgren, Rue & Lindström 2011). For α = 2 (ν = 1): C⁻¹ = c L², with L = κ² − ∇² (5-point Laplacian), κ = √(2ν)/ℓ, and c set so the variance is 1. Per-pixel weights (adaptive or brightness-based priors) enter as W⁻¹ c L² W⁻¹. As far as I can tell, the current `MaternKernel` regularization builds the dense covariance and inverts it. The sparse form only exists for integer α, so ν = 1.5 becomes ν = 1.
3. **Solve.** Preconditioned conjugate gradients on (F + λC⁻¹) s = D. The preconditioner is Powell et al.'s P = κ₀ MᵀM + λC⁻¹, where κ₀ is the peak of W̃. P is sparse and is factorised once per λ. For unweighted priors, an FFT preconditioner built from the gridded uv weight density works about as well.
4. **Evidence.** ln det H is exact from the sparse factor. ln det(F + H) = ln det P + ln det(P⁻¹(F + H)), with the second term from stochastic Lanczos quadrature (Ubaru, Chen & Saad 2017; 10 fixed probe vectors, ≤ 40 Lanczos steps). This agrees with the dense evidence to ~0.2% of ln Z on our tests. Powell et al. stop at ln det P, which they report can be 1–20% off.
5. **Positivity.** A primal-dual interior point method (Mehrotra predictor-corrector). Each step is a CG solve preconditioned by P plus the barrier's diagonal. Once the set of pixels held at zero has settled, the free pixels are solved exactly, with a few primal-dual active-set corrections (Hintermüller, Ito & Kunisch 2002). This gives exact zeros and matches scipy's NNLS on small problems. I also tried a projected Newton method and a pure active-set method, but both stalled at weak priors where ~30% of pixels sit at zero.

**Results**

Real ALMA data, 2 cores, visibilities streamed, adaptive prior, regularization strength set by a residual criterion. "w-tilde" is the current dense path.

| dataset | mesh | w-tilde, positive | matrix-free, positive | matrix-free, unconstrained |
|---|---|---|---|---|
| lensed SMG | 50² | 34 s, 1.07 GB | 5.1 s, 0.37 GB | 4.0 s |
| lensed SMG | 58² | 77 s, 1.46 GB | 15 s, 0.39 GB | 4.4 s |
| [CII] galaxy | 54² | 69 s, 1.21 GB | 7.0 s, 0.37 GB | 40 s |
| NGC 4274 | 64² | 429 s, 2.00 GB | 49 s, 0.40 GB | 12 s |
| NGC 4274 | 192² | not feasible | 266 s, 0.80 GB | 60 s |

On the compact sources, the positive matrix-free models agree with the positive w-tilde models to 0.2–0.7% of the peak after smoothing to the beam. Most of the remaining difference on extended emission comes from ν = 1 vs 1.5.

**Limitations**

- It needs a regular rectangular mesh, because the prior is built on the grid. Delaunay or Voronoi meshes could use the finite-element form of the same prior on the triangulation (Lindgren et al.'s original setting), which I haven't tried.
- Only integer α, so ν = 1, 2, …
- Uncertainty maps need diag((F + H)⁻¹), which would need a stochastic diagonal estimator. Not implemented yet.
- Linear light profiles / point components are not handled on this path yet.
- The number of CG iterations depends on how strong the prior is relative to the data, so weak priors cost more.

**Possible shape**

Perhaps a separate inversion class (or a `Settings` option) for interferometer data on a rectangular mesh, where the curvature-plus-regularization matrix is a `LinearOperator`. The reconstruction would come from CG or the interior point method, and the log det terms from the sparse factor plus Lanczos quadrature. Much of the inversion interface reads the dense matrices directly, so a separate path may be simpler to start with.

**References**

- Powell D. M. et al., 2021, MNRAS, 501, 515
- Lindgren F., Rue H., Lindström J., 2011, J. R. Stat. Soc. B, 73, 423
- Ubaru S., Chen J., Saad Y., 2017, SIAM J. Matrix Anal. Appl., 38, 1075
- Mehrotra S., 1992, SIAM J. Optim., 2, 575
- Hintermüller M., Ito K., Kunisch K., 2002, SIAM J. Optim., 13, 865

<img width="2698" height="795" alt="bench_real_solvers" src="https://github.com/user-attachments/assets/4f397d0a-987c-4302-b38d-0e1856abc258" />

<!-- formalised by the Intake (Conception) Agent on 2026-10-21 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/16b1291e-5d7e-43ae-8250-0eea830cc6ed/scratchpad/intake39.md -->
