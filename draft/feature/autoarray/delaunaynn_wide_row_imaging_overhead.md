# Speed up unique_mappings and adaptive_pixel_signals for wide DelaunayNN rows (imaging)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- numba-cpu
- imaging
- delaunay-nn
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft

Follow-up from PyAutoArray#623 phase 2 (measured 2026-10-15, laptop, threads=1, load 3-5).
After the numba Sibson kernel (#624), DelaunayNN on HST-scale imaging is still ~2.7x
Delaunay at sub_size 4 (0.78 s vs 0.29 s per `log_likelihood_function`, 1030 vertices,
15,380 pixels; sub 2: 0.32-0.48 s vs 0.31-0.38 s). Profile of the DelaunayNN extra cost:

- Sibson interpolation of 245k queries: 0.21 s
- `mapper.unique_mappings` (`mapper_numba_util.data_slim_to_pixelization_unique_from`): 0.30 s vs 0.10 s Delaunay
- `adaptive_pixel_signals_from`: 0.16 s vs 0.01 s — an `np.add.at` over the 32-wide (`SIBSON_MAX_NEIGHBORS`) rows, most slots empty (13-15 non-zeros max)

Fix ideas: iterate only `pix_sizes[i]` entries per row (skip padding) in both, numba or
compacted-CSR `np.bincount` for adaptive_pixel_signals. Acceptance: imaging DelaunayNN
within ~1.5x Delaunay at sub 4 with bit-/1e-12 parity; Delaunay unchanged.
Timing scripts: session scratchpad `0b91c774.../scratchpad/phase2/imaging_timing.py` (temporary).

Also (from the #625 independent review, pre-existing): `sibson.py` ~L518-555 can in principle emit a failed
row with `size == 0` whose NaN weights sit only in padding; every route reads the first `size` entries, so
the evidence comes out finite (and wrong) instead of NaN. Decide whether failed rows should keep `size >= 1`
so NaN propagates; add cavity-overflow and degenerate cases to the NaN-route tests.
