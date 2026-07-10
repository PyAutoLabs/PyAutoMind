# Chunk the kernel-CDF forward transform (remove the O(M×N) memory wall)

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Original request (verbatim): "do these two: kernel-forward chunking, the
branch-flip investigation" (2026-07-10, follow-up to
PyAutoArray#373 / PR#374, human-directed after merge).

## Background

The kernel-CDF meshes (`RectangularKernelAdaptDensity/Image`, merged 2026-07-10)
evaluate the forward transform exactly: `F(q) = Σᵢ wᵢ·Φ((q−xᵢ)/h)` broadcasts
queries × points into an (M, N, 2) array. At certification scale this is fine;
at production imaging scale it is a wall: 15,380 masked pixels at pixelization
over-sampling 4 → M≈246k, N≈15.4k → ~60 GB allocation (observed OOM in
`plotting_alignment/kernel_cdf_alignment.py` before its mask was shrunk).
The interferometer sparse path (M = N) is unaffected at current scales.

## Task

1. Chunk the query dimension of the kernel forward in
   `autoarray/inversion/mesh/interpolator/rectangular_kernel.py`:
   - jax path: `lax.map` (or `scan`) over fixed-size query blocks — static
     shapes, no per-call retrace, AD flows through blocks; pad M to a block
     multiple and slice back.
   - numpy path: plain block loop.
   - Block size an internal constant tuned so peak block memory is ~O(100 MB)
     at production scale (e.g. 1024–4096 queries); document the choice.
2. **Behaviour-identical numerics** — this is a refactor: same results to
   float precision. Validate:
   - unit test: chunked vs unchunked forward equality on random inputs
     (numpy path; both paths exercised via the block-size seam);
   - re-run both jax_grad certification scripts — all variants must pass
     unchanged (strict FD, eager-vs-JIT, parity values identical);
   - demonstrate the previously-OOM config runs: `kernel_cdf_alignment.py`
     with mask radius 3.5 / os_pix=4-scale kernel evaluation (or a direct
     probe at M≈246k, N≈15.4k) within laptop memory.
3. Update the O(M×N) caveat rows in
   `autolens_workspace_developer/jax_profiling/gradient/README.md` (added
   2026-07-10) once the wall is gone.

## Constraints

- No API change (block size is not a mesh kwarg unless measurement forces it).
- Library unit tests numpy-only; JAX validation via the jax_grad scripts.
- The inverse-table build (K×N) is small — leave it unchunked.

<!-- formalised 2026-07-10 from #373 follow-up list, human-directed -->
