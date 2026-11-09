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
