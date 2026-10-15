# Interferometer sparse inversion: compute data vector without the dense mapping matrix

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: safe
Priority: normal
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: glance
Witness: on the Aris 512x512 setup (91,507 masked pixels, 5,746 Delaunay vertices, use_jax=False) peak RSS of one likelihood call drops from 7.2 GB to <= ~3.5 GB with log likelihood unchanged to 1e-8
Review-minutes: 3
Unattended: ready

`autoarray/inversion/inversion/interferometer/sparse.py:104` computes
`data_vector = xp.dot(self.mapping_matrix.T, dirty_image)`, which materialises the dense
(masked pixels x source pixels) mapping matrix via hstack — 4.2 GB at 91,507 x 5,746. The step only
needs the sparse mapping operator (the same triplets the curvature routes already use). A memory
trace on the 512x512 mask attributes all RSS growth from ~3 GB to 7.2 GB to this line, on both the
numba direct_conv and NumPy FFT routes. It probably also explains most of the ~9 GB XLA temp
memory of the JAX path at that size.

Do: compute the data vector from the sparse triplets (scatter/segment-sum: D_j = sum over nonzeros
in column j of val * dirty_image[row]) on both the NumPy and JAX paths, so no dense mapping matrix
is built in the likelihood. Check other places in the interferometer sparse inversion (and
the numba subclass) that touch `mapping_matrix` per call. Keep outputs identical; add a test.
Measure peak RSS and time before/after on the 512x512 cache (and JAX compile memory).

Evidence: /tmp/claude-1000/-home-jammy-Code-PyAutoLabs/50c8c6cd-6ac2-47c2-9290-7ee73f9c4315/scratchpad/aris/PROGRESS4.md and step8/ (dataset_sparse_512.pkl cache, bench.py). PyAutoArray ccddfba6.

<!-- formalised by the Intake (Conception) Agent on 2026-10-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aaade95e-3f22-4661-b77d-365d91380803/scratchpad/intake3/interferometer_sparse_data_vector_dense.md -->
