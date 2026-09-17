# PointSolver image-plane chi-squared CPU speed-up: is the JAX CPU path sub-optimal enough for a sparse/numba lever?

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoLens
- PyAutoArray
Themes:
- point-source
- profiling
- cluster
- jax
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: cluster-strong-lensing
Filed: 2026-09-17

# PointSolver image-plane chi-squared CPU speed-up: is the JAX CPU path sub-optimal enough for a sparse/numba lever?

User request (verbatim):

In autolens_profiling, we have done lots of work speeding up imaging and interferometer on CCD. Now, I want us to speed up the point_source image plane chi-squared, with this issue focusing on CPU. This will likely use the JAX implementation, for other LH functions we had existing numba code to build on and there was lots of sparsity to exploit. Im not sure doing a whole numba CPU implementation is worth it. However, its worth some research, and asking if the JAX CPU implementation is sufficiently sub optimal that there are obvious low hangign fruit improvements with a clever CPU sparse approach, noting that cluster modeling will rely heavily on the PointSolver.

We may not have a likelihood_breakdown of this likelihood function yet, in which case we should make one before trying any kind of CPU or JAX code. I have another claude chat looking into that so bare that in mind and we wont do any real dev work until that is made

## Gate

Gated on the point_source likelihood_breakdown cell (scripts/point_source/likelihood_breakdown/) being built by a concurrent session; no CPU or JAX implementation work starts until that breakdown exists. This session's deliverable is the research note + ranked candidate levers. Research phase COMPLETE 2026-09-17 (see Findings); the implementation phase (lever 1 first, library-first in PyAutoArray/PyAutoLens) still waits on the breakdown cell.

## Baseline

Committed CPU runtime for image_plane_solved (v2026.7.23.1): eager 274 ms/call, single-JIT full pipeline 38.6 ms/call, vmap(3) 28 ms/call — results/runtime/point_source/image_plane_solved/.

## Where the code lives

- `autolens_profiling` — profiling cells and committed runtime results.
- `PyAutoLens` — solver source, `autolens/point/solver/`.
- `PyAutoArray` — triangle machinery, `autoarray/structures/triangles/`.

## Related

Sibling (not parent): `draft/research/autolens_profiling/point_solver_profiling_cells.md` — the PointSolver profiling-cells research prompt in the same cluster-strong-lensing epic.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/a4c1ddc1-40ff-4f6b-9048-5c5e0b329332/scratchpad/intake_input.md; Target/Epic/title hand-restored after the conductor resolved Target: PyAutoArray and dropped Epic: -->

## Findings (2026-09-17 research run, CPU, read-only — no repo edited)

Full note + reproducible scratch scripts/JSONs: session scratchpad `pointsolver/pointsolver_cpu_research_note.md` (to be landed in `autolens_profiling/results/notes/` with the fix PR). Machine: WSL2 laptop, 8 cores, NPROC=8, fp64, jax 0.10.2, autolens 2026.8.17.1; speed-ups are within-run interleaved ratios.

**Answer:** the JAX CPU path is sub-optimal, but not from sparsity or padding — ~84% of the call is a `jnp.unique` sort that is a no-op under jit.

- **Mechanism.** `CoordinateArrayTriangles._vertices_and_indices` (PyAutoArray `autoarray/structures/triangles/coordinate_array.py`) calls `jnp.unique(flat_vertices, size=3*N, fill_value=nan)`. Under jit the static `size=3N` means the "deduplicated" table has exactly as many rows as the input (69 849 for the 100×100 `simple` grid, 59% NaN fill), so it saves zero deflection evaluations and costs one lexicographic sort of 69 849 fp64 rows. The `ArrayTriangles` it builds is used only for `containing_indices` and thrown away every step. JAX-path-only defect: the NumPy sibling's `np.unique` genuinely shrinks 69 849 → 28 665.
- **Proof (monkeypatched in scratch, library untouched).** Full `AnalysisPoint.log_likelihood_function` on the `image_plane_solved` config: 40.0 → 8.1 ms/call (4.9× median, 5.4× p10), log-likelihood bit-identical (7.743201200876812), HLO sorts 15 → 7, FLOPs 15.58M → 6.50M. Real cluster solver config (200×200 @ 0.7″, 92 169 triangles, 13 mass components, 3 planes, 2 sources): 117 → 48 ms per source (2.4×), solved positions identical; a 2-source cluster likelihood 237 → 98 ms.
- **Lower bound.** Bare deflections for one solve ≈ 6 ms (69 849 + 7×720 points) inside a 26–42 ms call → 77–86% bookkeeping. Post-fix the simple solve is ~1.4× its deflection bound; the cluster solve is at its (extrapolated) bound, so at cluster scale the remaining lever is the dPIE/NFW deflection code, not the solver.
- **Sensitivity.** n_steps: all 7 refinement steps cost ~3 ms total (~0.45 ms each) — not a lever, and LL degrades below 4 steps. Grid extent: 30×30 = 6.4 ms vs 100×100 = 39.8 ms vs 140×140 = 72 ms with bit-identical LL — the cell tiles ±9.9″ to find images at ~1.6″. Fit/χ² + β* centre + magnification filter = 0.34% of the call. The solve is invoked twice per likelihood (`model_data` property) but XLA CSEs it — no lever.
- **NumPy path (the existing unpadded sparse implementation).** 96 ms/solve doing 2.5× fewer deflection evaluations — 12× slower than the fixed JAX path.
- **Numba verdict: not worth it.** No existing kernel, no exploitable sparsity beyond what the NumPy path already has, headroom gone after a ~20-line fix, and a callback loop would forfeit the `custom_jvp` implicit gradient, `vmap` and the GPU path.

**Ranked levers:** (1) drop the throwaway `jnp.unique` on the JAX trace path (PyAutoArray + PyAutoLens `_plane_triangles`; red-control bit-identical LL + cluster positions) — 4.9× simple / 2.4× cluster; (2) precompute the initial lattice's unique vertices + index map once at solver construction in NumPy (the step-0 tiling is static), cutting step-0 deflection count ~2.4–6× with no runtime sort — matters most at cluster scale where deflections dominate post-fix (not measured); (3) solver grid extent guidance / defaults (6.2×, zero code); (4) coarser initial `scale` + more steps (~4× on step 0, completeness risk, not measured); (5) `MAX_CONTAINING_SIZE` / 240-triangle fan-out (≲1.5 ms, correctness knob); (6) mass-profile deflection code at cluster scale. Recommend against warm-starting across sampler calls (breaks the pure-function contract `vmap`/`custom_jvp` rely on).

**Not measured:** vmap batch 1/4/16 post-fix, `MAX_CONTAINING_SIZE` sweep, post-fix grid/n_steps sweep, `--xla_disable_hlo_passes=constant_folding` A/B, bare deflections at 276 507 points. Trap: jax caches jaxprs on function identity — a monkeypatch A/B needs a distinct function object and `jax.clear_caches()` before each compile.
