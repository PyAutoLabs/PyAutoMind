# Sparse interferometer terms: NUFFT ignores the mask origin and provenance cannot see mask-shape-compatible but pixel-incompatible masks

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- interferometer
- sparse-operator
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-10-01
Difficulty: medium
Consequence: judge
Witness: (1) on an all-false (11, 11) mask with pixel_scales 0.5 and origin (0.5, -0.5), the dirty image of a point source at (1.0, -1.5) via `TransformerNUFFT` peaks at the same native pixel as via `TransformerDFT` (today DFT → (6, 6) whose coordinate is (0, 0) after a `phase_centre=(1.0, -1.5)` re-centring, NUFFT → (5, 5) labelled (0.5, -0.5)); `transformer.visibilities_from` NUFFT vs DFT agree at 1e-10 on that offset-origin mask. (2) `SparseTerms.__add__` (or `Interferometer.from_sparse_terms`) refuses two terms built on masks with identical `shape_native` / `pixel_scales` / `origin` but different masked pixels (e.g. the centre pixel masked in one), or the provenance records a mask hash / masked-pixel count that catches it.
Review-minutes: 6
Unattended: ready
Source: Codex gpt-6-astra review of the streaming P5 branch (PyAutoLabs/PyAutoArray#600), 2026-10-01 — findings 3 and 5, both PRE-EXISTING on main; exposed because phase-centre shifts make the origin matter.

## What

1. `autoarray/operators/transformer.py` ~L331-343 (`TransformerNUFFT`): the internal `_shift` applies the even-size half-pixel
   offset but never `real_space_mask.origin`; the DFT uses the actual grid coordinates. Dirty images and dirty beams from the
   NUFFT are therefore displaced on offset-origin masks (the difference-based W̃ kernel is origin-invariant). Also
   `SparseTerms.__add__` did not check `transformer_class_name` (being added in P5), so DFT and NUFFT terms from such a mask
   could be mixed.
2. `SparseTerms` provenance (`shape_native`, `pixel_scales`, `origin`, `eps`, `phase_centre`, `transformer_class_name`)
   cannot distinguish two masks with the same geometry but different masked pixels: summing channel terms built on them
   passes every check, the dirty image at a pixel masked in one channel holds only the other channel's contribution while
   the kernel and scalars include both, and `from_sparse_terms` accepts the result on either mask.

## Plan

1. Reproduce (1) with the witness mask; fix `_shift` to include the origin offset (in radians, with the (y, x) sign
   convention the DFT uses); extend the NUFFT-vs-DFT parity tests to a nonzero-origin mask.
2. For (2) record a cheap mask fingerprint in `SparseTerms` provenance (e.g. `n_masked_pixels` + a hash of the mask
   array, or the mask itself) and check it in `__add__` and `from_sparse_terms`; persist it in the FITS round trip.
