## interferometer-sparse-data-vector
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/626
- completed: 2026-10-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/630
- merge: 7cc71238bcb31300ee183902ebfeb52452f40712 (head 8676b6a0)
- summary: The sparse-operator interferometer inversion now builds its data vector directly from the mapper's COO triplets, so the likelihood path no longer materialises the dense mapping matrix. New private helpers `_sparse_triplets_slim_from` and `_data_vector_mapper_from`; tests check the sparse data vector against the dense product. Scope merged = scope filed (no partial).
- witness: numba 5,746-vertex peak RSS 7.17 → 3.14 GB; JAX jit 1,459 vtx 3.65 → 2.60 GB; XLA compile temp at 5,746 vtx 8.95 → 1.86 GB, and JAX at 5,746 vtx now runs at 3.24 GB. Timings not claimed (machine load 2–14).
- decision-taken: the witness wording "logL unchanged to 1e-8" was read as fp64 precision; measured agreement ≤2.5e-11 relative. Revert: `git revert 8676b6a0`.
- behaviour-note: JAX mixed precision now computes this as a float64 block, so results are not bit-identical to the previous mixed-precision path.
- gate: tests 2033 pass/4 xfail · smoke 92/92 scripts + 4/4 notebooks · review CLEAN (independent Opus) · Heart RED under the recorded live-human development override (session 3e3dea38; reasons on #626; permitted commit/push/PR-open, merge separate — merged by human /prm 2026-10-15).
- campaign: PyAutoPulse#62, task `interferometer_large_mask_aris`.
- where-to-pick-up: #627 (adaptsplit-logdet-backend-parity; patch on the issue) is next on the PyAutoArray claim, then #628 (interferometer-numba-route-gate) by the human's ordering.

## Original prompt

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
Issued: 2026-10-15
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
