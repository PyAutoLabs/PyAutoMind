# Oversampled PSF: k×s evaluation/convolution coupling + simulator adoption

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Follow-on to the oversampled-PSF series (design PyAutoArray#353, recorded as
future work in `oversampling_design.md` §3: "generalising to
`over_sample_size = k * convolve_over_sample_size` … is a pure extension of
the bin step, not a redesign"). Filed 2026-07-08 at user request.

## Why

Oversampled convolution currently requires `over_sample_size_*` to be a
uniform int **equal** to `convolve_over_sample_size`. But the workspace
simulators (and many fits) use **adaptive radial** evaluation grids — e.g.
the start-here simulator's `sub_size_list=[32, 8, 2]` — which the
uniform-equal rule rejects. The k×s coupling removes the conflict: evaluate
at any per-pixel size that is a **multiple of s**, partially bin the
evaluated values from k_i·s down to the uniform s the convolution needs,
convolve at s, bin to image resolution. Adaptive evaluation accuracy and
oversampled convolution then compose instead of excluding each other.

## Scope — library first (PyAutoArray + PyAutoGalaxy), workspace follows

1. **Relax the coupling rule.** `_validate_convolve_over_sample_size`
   accepts any `over_sample_size` (int or adaptive Array2D) whose every
   entry is divisible by `convolve_over_sample_size`; anything else still
   raises `DatasetException` loudly (e.g. sub size 8 with s=3).
2. **Partial pre-bin.** New machinery to bin per-pixel evaluation blocks
   (k_i·s × k_i·s, sub-block order, possibly adaptive k_i) down to uniform
   s×s blocks by the mean of each (k_i)² group — the existing segment-mean /
   `slim_for_sub_slim` machinery generalises. **Design paragraph required
   before code** (series lesson: hypotheses get corrected at survey): decide
   whether the pre-bin lives (a) inside the Convolver entry points, which
   would take values at the grid's evaluation resolution plus the sizes
   array (state caches the pre-bin index map alongside the permutations), or
   (b) as a standalone util the callers apply (operate/image.py evaluation
   sites, the linear-lp override, `convolved_padded_image_2d_from`, the
   inversion's `mapping_matrix_over_sampled`). Option (a) keeps callers
   unchanged; option (b) keeps the Convolver contract simple. Pick one and
   record why.
3. **Callers** (PyAutoGalaxy): whichever option lands, the evaluation grids
   no longer need forcing to s — `_psf_evaluation_grids_from` and friends
   pass the natural grids through.
4. **Tests** (numpy-only): exactness — the k×s path must equal manually
   pre-binning the evaluated values and feeding the existing s-path
   (identity, ≤1e-14, uniform k and adaptive k_i); divisibility guards;
   s=1 and k=1 regression parity; extend
   `autolens_workspace_test/scripts/imaging/convolution_over_sampled.py`
   with an adaptive-evaluation + s=2 FitImaging leg.
5. **Simulator adoption** (autolens_workspace, after the library merge):
   update the simulator scripts to simulate with `convolve_over_sample_size=2`
   (fine `from_gaussian` PSFs) while keeping their adaptive radial evaluation
   grids. Start with `scripts/imaging/simulator.py` and the feature
   simulators that copy its pattern; update the `simulator.py` and
   `over_sampling.py` guide prose to reflect that adaptive evaluation now
   composes with oversampled convolution.

## Risks (survey before the simulator leg)

- **Changing the simulators changes the simulated datasets** (more accurate
  blurring ⇒ different pixel values). Every workspace/workspace_test script
  that auto-simulates its dataset and pins numbers against it — and the
  curated smoke subsets — must be surveyed for re-baselining before the
  workspace PR ships. If the ripple is large, adopt in the start-here
  simulator only and stage the feature simulators separately.
- Interferometer/datacube simulators are out of scope (no 2D PSF
  convolution / different operators) — state so in the PR.
- Fits-loaded PSFs (real instrument kernels) stay at s=1 unless a fine
  kernel exists; only the Gaussian `from_gaussian` simulators adopt s=2.

## Sequencing

After the two currently-parked series items ship (docs PR
autolens_workspace#235; refactor #360) — the k×s work builds on the
refactored helpers. Library-first merge gate as usual.

Parent series: `issued/oversampling.md` (design `oversampling_design.md` §3).
