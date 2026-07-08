# k×s coupling — design note (phase 1)

Deliverable of `kxs_phase_1_design.md` (PyAutoLabs/PyAutoArray#362).
Companion ground truth: `kxs_ground_truth.py` (same directory). Grounded
against the refactored helpers on the `feature/psf-oversample-refactor`
branch (PyAutoArray#361 / PyAutoGalaxy#484 — phase 2 requires them merged).

## 1. Mechanism (confirmed numerically)

Per image pixel: evaluate on the adaptive k_i·s sub-grid → partial-bin by
the mean of each (k_i)² group to a uniform s×s block → the resulting
uniform s-resolution fine image is PSF-convolved at s (unchanged series
machinery) → bin s→1. Adaptive sampling does integration accuracy; the
uniform intermediate does convolution. Ground truth (`kxs_ground_truth.py`):
k=1 reduces exactly to the parent s=2 reference; the adaptive
k∈{2,1}-radial reference numbers are pinned for phases 2–3:

| quantity | adaptive k∈{2,1}, s=2 |
|---|---|
| sum over mask | 2.785595827470031e+00 |
| blurred[slim 0] | 3.725339878416663e-02 |
| blurred[slim 17] | 2.011409122749033e-01 |
| blurred[slim 36] | 1.090992099132513e-02 |

## 2. The fork: where does the partial pre-bin live?

**Decision: (b) caller-side util, with the segment map cached on
`OverSampler`.** Not (a) Convolver-internal.

Rationale, grounded:

- The refactored Convolver engines (`_convolved_over_sampled_{np,jax}_from`)
  take values **already at uniform s in per-pixel sub-block order** and
  validate length against the cached permutation
  (`_check_over_sampled_length`). Option (a) would require `state_from` /
  `_fine_state_from` to receive the evaluation `over_sample_size` array
  (mask alone cannot derive it), growing the state contract and forcing
  dual-length input detection — implicit magic where the series has
  deliberately used loud, single-contract inputs.
- Option (b) keeps the 2a contract intact ("the Convolver takes uniform-s
  sub-block values") and puts the new logic in one place with one test
  surface.

## 3. The util (phase 2 spec)

`over_sample_util.binned_to_convolve_size_from(values, sub_size, convolve_over_sample_size, xp=np)`

- Input: values of length Σ(k_i·s)² in per-pixel sub-block order (row-major
  within each block, exactly what `grid.over_sampled` evaluation yields);
  `sub_size` the per-pixel evaluation sizes (k_i·s, int or Array2D);
  trailing dims allowed (mapping-matrix rows).
- Index map: within pixel p's (k_i·s)-row-major block, sample (row, col)
  belongs to fine cell (row // k_i)·s + (col // k_i); global segment id =
  p·s² + local cell. Vectorizable from the sub_size array; **cached on
  `OverSampler`** (mirroring the existing `segment_ids` used by
  `binned_array_2d_from`) as e.g. `convolve_segment_ids_from(s)`.
- Mean per segment: `np.bincount` weights / counts on the numpy path,
  `jax.ops.segment_sum` on the JAX path — both already precedented in
  `OverSampler.binned_array_2d_from`.
- No-op fast path when all k_i == 1 (`sub_is_uniform` and equal to s):
  return values unchanged — preserves the existing equal-sizes behaviour
  byte-identically.

## 4. Validation + call sites (phase 2 scope)

- `_validate_convolve_over_sample_size`: the equality rule relaxes to
  divisibility — every `over_sample_size` entry (int or adaptive Array2D)
  must satisfy `entry % s == 0`, else `DatasetException` (loud; e.g. size 8
  with s=3 rejected). Adaptive Array2D becomes *allowed* when divisible.
- Call sites applying the util after evaluation (all already funnel through
  a small number of seams thanks to the series refactor):
  `OperateImage._psf_evaluation_grids_from` consumers (the three blurred
  variants), the linear-lp override, `convolved_padded_image_2d_from`, the
  simulators' fine path, and `Mapper.mapping_matrix_over_sampled` (rows
  pre-binned with the same util; the mapper's over_sampler carries the
  pixelization sizes).
- `GridsDataset.blurring` at k×s: the blurring grid keeps
  `over_sample_size = s` (k_i on the blurring region buys nothing — its
  flux is smooth wings) — one line, documented.

## 5. Risks carried forward

- The mapper row pre-bin multiplies the sub-resolution matrix build cost by
  k_i² before reduction — profile at phase 2 exactly as the parent series
  profiled the ×s² cube.
- Simulator adoption (phase 4) changes simulated datasets — the
  re-baselining survey in the parent prompt's Risks section governs.

## 6. Phase-2 execution sketch

1. `OverSampler.convolve_segment_ids_from(s)` + `binned_to_convolve_size_from`
   util (+ exactness tests vs manual reshape-mean, uniform and adaptive).
2. Divisibility validation swap in `Imaging` (+ guard tests).
3. Call-site application (+ ground-truth-pinned tests: the §1 table through
   the public API; k=1 parity strict).
4. Mapper rows + inversion leg (+ delta-kernel identity at k×s).
5. PyAutoLens/PyAutoGalaxy suites + workspace leg per the parent prompt.
