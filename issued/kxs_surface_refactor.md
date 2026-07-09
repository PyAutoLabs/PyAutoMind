# Refactor the k×s coupling surface (proper Refactor Agent run)

Type: refactor
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

The k×s series' phase-5 refactor exercise, re-run properly through the
Refactor Agent (the 2026-07-09 leg vectorized one function without an agent
invocation — recorded miss). Behaviour-preserving; witnesses are the full
PyAutoArray + PyAutoGalaxy suites plus the ground-truth-pinned k×s tests and
the workspace script `autolens_workspace_test/scripts/imaging/convolution_over_sampled.py`.

## Surface (everything k×s touched)

- `@PyAutoArray/autoarray/operators/over_sampling/over_sample_util.py` —
  `convolve_bin_segment_ids_from` (+ lru cache) and
  `binned_to_convolve_size_from`; the segment-mean pattern duplicates
  `OverSampler.binned_array_2d_from`'s bincount/segment_sum split.
- `@PyAutoArray/autoarray/inversion/mappers/abstract.py` —
  `mapping_matrix_over_sampled` property + `mapping_matrix_over_sampled_for`.
- `@PyAutoArray/autoarray/dataset/imaging/dataset.py` —
  `_validate_convolve_over_sample_size` (divisibility form).
- `@PyAutoGalaxy/autogalaxy/operate/image.py` — the prime candidate:
  `_psf_evaluation_grids_from` + `_binned_for_convolution` are two halves of
  one concern, and the three blurred-image variants each re-implement the
  evaluate -> maybe-pre-bin -> convolve-or-delegate sequence; the list/dict
  variants could route through one scalar core.
- `@PyAutoGalaxy/autogalaxy/profiles/light/linear/abstract.py` — the
  override borrows `OperateImage._binned_for_convolution` via a local
  import; assess whether the shared core removes the borrow.

## Constraints

- Zero behaviour change; no test edits; all witnesses green unmodified.
- Public API unchanged; JAX paths stay static-shape pure.
- The `convolver/` package split remains out of scope (parent decision
  stands, recorded on PyAutoArray#360).
