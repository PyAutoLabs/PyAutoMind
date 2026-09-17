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

Gated on the point_source likelihood_breakdown cell (scripts/point_source/likelihood_breakdown/) being built by a concurrent session; no CPU or JAX implementation work starts until that breakdown exists. This session's deliverable is the research note + ranked candidate levers.

## Baseline

Committed CPU runtime for image_plane_solved (v2026.7.23.1): eager 274 ms/call, single-JIT full pipeline 38.6 ms/call, vmap(3) 28 ms/call — results/runtime/point_source/image_plane_solved/.

## Where the code lives

- `autolens_profiling` — profiling cells and committed runtime results.
- `PyAutoLens` — solver source, `autolens/point/solver/`.
- `PyAutoArray` — triangle machinery, `autoarray/structures/triangles/`.

## Related

Sibling (not parent): `draft/research/autolens_profiling/point_solver_profiling_cells.md` — the PointSolver profiling-cells research prompt in the same cluster-strong-lensing epic.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/a4c1ddc1-40ff-4f6b-9048-5c5e0b329332/scratchpad/intake_input.md; Target/Epic/title hand-restored after the conductor resolved Target: PyAutoArray and dropped Epic: -->
