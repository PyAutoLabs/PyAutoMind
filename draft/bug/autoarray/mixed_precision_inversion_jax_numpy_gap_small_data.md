# Mixed-precision inversion: the JAX-vs-NumPy log-likelihood gap grows on low-pixel-count data

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-06

Found during the phase-5 rebuild of the ci-timing-fast-tests epic
(autogalaxy_workspace_test#117). `scripts/imaging/jax_likelihood/rectangular.py` —
an adapt-image `RectangularBilinearAdaptImage` inversion run with
`use_mixed_precision=True` — asserts `jax.jit(analysis.fit_from)` against the
float64 NumPy path at `rtol=2e-2`. On the coarsened shared imaging dataset
(100x100 @ 0.3", 316 masked pixels) the absolute gap between the two paths is
~15 nats, against 5.8 nats on the previous dataset (180x180 @ 0.2", 716 masked
pixels; `-3150.83` vs `-3145.04` there). Measured at eight mesh sizes on the new
data the gap is essentially mesh-independent (14.99 / 26.73 / 21.32 / 15.47 /
17.64 / 19.06 / 16.80 / 14.98 nats at meshes 12, 14, 16, 17, 19, 20, 24, 28), so
it is a property of the mixed-precision inversion on lower-pixel-count data, not
of the mesh. The rebuild kept the script green by sizing the mesh to the data
(17x17, source pixels <= image pixels — the under-determined 28x28 inversion was
the actual failure) and did not touch the tolerance.

Ask: characterise where the fp32 part of the mixed-precision inversion loses the
precision as the pixel count falls (the data-vector / curvature-matrix products,
the regularization term, the log-det), decide whether the smoke script's 2 %
relative tolerance is the right contract or whether an absolute-nats bound is,
and fix the source if a genuine precision loss is found. Reproducer: the
`jax_test` imaging dataset of autogalaxy_workspace_test after #117 plus that
script; `test-results/` numbers above.

## Original observation (verbatim, from the #117 rebuild report)

> the JAX-vs-NumPy absolute discrepancy is ~15 nats on the new data against
> 5.8 nats on `main`'s (`-3150.83` vs `-3145.04` there), and it is essentially
> independent of mesh size … So the mesh fix restores the *relative* margin
> (1.23% against the script's 2%) by increasing `|log_L|`, not by shrinking the
> gap. The growth of that mixed-precision discrepancy on lower-pixel-count data
> is a finding for the source repos, not something this change fixes.
