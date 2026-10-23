DelaunayNN wide-row imaging overhead (PyAutoArray#629), DelaunayNN imaging arm of the
PyAutoPulse campaign `delaunay-nn-cpu`. Merged 2026-10-17 as
https://github.com/PyAutoLabs/PyAutoArray/pull/637 (MERGED):

- `adaptive_pixel_signals_from` (NumPy path) now sums only the live `pix_sizes[i]` entries of
  the 32-wide Sibson tables via a numba kernel (`adaptive_pixel_signal_sums_from`, bincount
  fallback), bit-identical to the padded scatter; JAX branch unchanged.
- `data_slim_to_pixelization_unique_from` resets only the touched `pix_check` entries and the
  mapper no longer copies the wide tables; outputs bit-identical.
- Sibson failed rows (overflow/degenerate) keep size ≥ 1 with a NaN weight (reference, numba,
  JAX), so a failed row now yields NaN evidence instead of a finite, wrong one.

RAL A/B (job 412525, `ral` exclusive, 1 thread): DelaunayNN sub 4 0.569 → 0.392 s
(2.20× Delaunay, was 3.00×), sub 2 0.235 → 0.189 s (1.75×, was 2.10×); adaptive signals
158 → 6.5 ms; logL bit-identical on every case. The prompt's ~1.5× acceptance line is **not
met**: the remainder is the Sibson interpolation itself (~41% of the call) and curvature over
wider unique-mapping rows, outside this scope. Human decision 2026-10-17: further DelaunayNN
speed-up is filed as research, not continued here.


## Original prompt

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
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/629
Pulse: campaign delaunay-nn-cpu (to be created; PyAutoPulse free since 2026-10-15)

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
