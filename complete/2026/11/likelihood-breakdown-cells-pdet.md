## Outcome

Remainder of #523. PR #526 merged 2026-11-10 (a8ac3103) under the live human's Heart-RED development override ("Override + RAL validation") and `/prm`.

- Shared helpers `reconstruction_steps.grounding_from` / `log_det_regularization_from` give the PyAutoArray#682 pseudo-determinant `ln det H`. They are used by the inline evidence and timed log-det rows of `imaging/{rectangular,delaunay,delaunay_nn}` and `datacube/delaunay`, by `sparse_steps.log_evidence` (via `SparseContext.reg_grounding`), by `matrix_free` (exact, scorer, and SLQ on the grounded subspace), and by #524's `FixedLightSystem` / `log_evidence_terms_np`. The JAX-free builder keeps a pinned NumPy copy.
- RAL 414743 (`ral`, CPU fp64, private library mains incl. #682): 10/10 COMPLETED, and the cell evidence equals the library's on every run.
- Pins re-measured:

  | Pin | Value |
  |---|---|
  | delaunay constant_split / adapt_split | 29120.1328 / 29164.2105 |
  | delaunay_nn constant_split / adapt_split | 29153.7935 / 29358.1182 |
  | rectangular bilinear / rtu | 28631.6052 / 28515.5316 |
  | matrix_free `PINNED_LOG_DETS` | all three meshes |
  | datacube sma per channel | −3160.43901 (new) |

  Most shifts exceed #682's +9.21 because the old pins also missed earlier library changes.
- New test: `scripts/misc/likelihood_breakdown/test/test_pdet_grounding.py`. `pytest scripts/misc/*/test` gives 1907 passed, 6 skipped.

## Original prompt

# Per-cell likelihood_breakdown evidence still uses the pre-#682 ln det H

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Filed: 2026-11-09
Issued: 2026-11-09
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/525

Remainder of autolens_profiling#523 (record `complete/2026/11/likelihood-breakdown-pdet-drift.md`). PR #524 taught `reconstruction_steps.log_evidence_terms` the PyAutoArray#682 pseudo-determinant via an optional `grounding` argument, and wired it through `FixedLightSystem` and `log_evidence_terms_np`. These cells still call the scorer without grounding, so their recorded evidence terms sit +9.21 nats per regularized mapper from the library's `FitImaging.log_evidence`:

- `scripts/imaging/rectangular/likelihood_breakdown.py`
- `scripts/imaging/delaunay/likelihood_breakdown.py`
- `scripts/imaging/delaunay_nn/likelihood_breakdown.py`
- `scripts/imaging/pixelized/matrix_free.py` (and `test_matrix_free_steps.py`)

Pass `grounding=inversion._intrinsic_regularization_blocks` (empty on older libraries) at each call. Check whether any committed result JSON or witness compares cell evidence to the library. Run each changed cell once to confirm its evidence equals `FitImaging.log_evidence`.
