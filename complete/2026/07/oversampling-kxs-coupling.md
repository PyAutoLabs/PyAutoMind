# oversampling-kxs-coupling

- shipped: 2026-07-09 (series closed; the prompt never left `draft/`)
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/362 (CLOSED — "series complete")
- prs: PyAutoArray#363, #364, #365 · PyAutoGalaxy#486, #489 · autolens_workspace#236 · autolens_workspace_test#154 (all merged)
- repos:
  - PyAutoArray, PyAutoGalaxy
  - autolens_workspace, autolens_workspace_test
- phase-records: [[kxs-design]] [[kxs-core]] [[kxs-cache]] [[kxs-workspace-tests]] [[kxs-refactor]] [[kxs-surface-refactor]]

## Summary

This is the **source prompt** for the k×s coupling series — the five-phase plan
it lays out was executed in full over 2026-07-08/09 and the series tracker
PyAutoArray#362 was closed as "series complete". Six dated completion records
already existed for the individual phases; only the prompt they all came from
was never advanced out of `draft/feature/autoarray/`.

Recorded 2026-08-09 by the draft/ sweep. No work is owed.

## Verified against PyAutoArray main (`efaf3041`), 2026-08-09

Graded against the prompt's own § Scope, not inferred from the phase records:

1. **§1 relax the coupling rule — SHIPPED.**
   `_validate_convolve_over_sample_size` (`autoarray/dataset/imaging/dataset.py:23`)
   accepts any `over_sample_size` (int or adaptive `Array2D`) whose every entry
   is divisible by `convolve_over_sample_size`, and raises `DatasetException`
   naming the rule otherwise. Its docstring states the mechanism in the prompt's
   own words — "the k x s coupling, whereby values evaluated at per-pixel sizes
   k_i * s are partially binned to the uniform s the convolution requires".
   The pre-change equality rule is gone.

2. **§2 partial pre-bin — SHIPPED**, as
   `over_sample_util.binned_to_convolve_size_from`
   (`autoarray/operators/over_sampling/over_sample_util.py:205`). The placement
   fork the prompt required a design paragraph for was settled and is recorded in
   [[kxs-design]]. Covered by `test_over_sample_util.py` on both legs the prompt
   asked for — `binned_to_convolve_size_from__uniform_k__equals_manual_reshape_mean`
   and `__adaptive_k__and_identity_fast_path`.

3. **§3 PyAutoGalaxy callers — SHIPPED** via PyAutoGalaxy#486 ([[kxs-core]]).

4. **§4 tests — SHIPPED.** Library numpy-only tests as above; the
   `convolution_over_sampled.py` adaptive + s=2 `FitImaging` leg the prompt
   specifies landed as autolens_workspace_test#154 ([[kxs-workspace-tests]]:
   lp round trip chi2=0, adaptive pixelized 6.6e-5, divisibility guard,
   adaptive simulate→fit 1.1e-29).

5. **§5 simulator adoption — DELIBERATELY RE-SCOPED, not skipped.**
   [[kxs-core]] records the fork resolved as option (c): executed simulators stay
   at `s=1`, and option (a) was split out as
   `draft/feature/autolens_workspace/oversampled_psf_dataset_adoption.md`. That
   prompt is correctly still a live draft — it is the residue of this §5, and is
   NOT covered by this record.

6. **Phase-5 refactor exercise — SHIPPED** as PyAutoGalaxy#489
   ([[kxs-surface-refactor]]), plus the extra [[kxs-cache]] and [[kxs-refactor]]
   legs the series added on top of the original plan.

## Why it was missed

Nothing upstream drifted — the trackers were right the whole time, exactly as in
the 2026-08-08 `planned.md` prune. The prompt is stale purely because `draft/` is
graded by no check, and slug-similarity is too weak to catch it: this file's stem
against `kxs-core` scores a Jaccard of 0.25, well under any workable threshold.
What found it was reading the prompt's acceptance criteria against the tree — and
it was provable from PyAutoMind alone, since the six phase records were already
sitting in `complete/2026/07/`.

## Original prompt
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

## Workflow — mirror the oversampling series (user instruction, 2026-07-08)

Phase like the parent series, each phase its own issue/PR behind the
library-first gate:

1. **Design + ground truth** (no source edits): settle the pre-bin placement
   fork (§ Scope 2) with file/line grounding; extend the brute-force ground
   truth with the adaptive-k_i partial-bin reference (evaluate at
   [k_i·s], partial-bin to s, convolve, bin — pinned numbers the later
   phases assert against). Mechanism: adaptive evaluation → partial bin to a
   uniform s-resolution fine image → PSF convolve at s → bin s→1.
2. **Core library** (PyAutoArray + PyAutoGalaxy callers): the divisibility
   rule, the partial pre-bin, wiring; unit tests pinned to phase-1 numbers;
   s=1 and k=1 strict parity.
3. **Workspace tests** (autolens_workspace_test): extend
   `convolution_over_sampled.py` with an adaptive-evaluation + s=2
   FitImaging leg and a simulate→fit round trip on an adaptive grid.
4. **Simulator adoption + docs** (autolens_workspace): simulator scripts to
   s=2 (re-baselining survey first, per Risks); update the simulator and
   over_sampling guide prose to say adaptive evaluation now composes with
   oversampled convolution.
5. **Refactor exercise** (Refactor Agent, behaviour-preserving, last): sweep
   everything the k×s work touched — in particular whatever the pre-bin
   decision adds to `convolver.py`/`over_sample_util.py` — against the full
   test surface built by phases 1–4.

## Sequencing

Phase 1 (design) can start immediately. Phases 2+ require the parent
series' refactor PRs merged (PyAutoArray#361, PyAutoGalaxy#484) — the k×s
work builds on the consolidated helpers. Library-first merge gate as usual.

Parent series: `issued/oversampling.md` (design `oversampling_design.md` §3).
