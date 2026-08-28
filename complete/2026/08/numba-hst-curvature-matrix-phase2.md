# Phase 2: 1.86x more on the HST numba evaluation — a two-stage source-space accumulator for F, and one eccentric-radius grid shared across an MGE basis

- **Issue:** PyAutoArray#507 (closed) · **PRs:** PyAutoArray#508 (`f4b8e758`, head `d8bc3bac`), PyAutoGalaxy#590 (`90317122`, head `6031aa0a`), autolens_profiling#190 (`ed1e265a`, head `7cc4bbd7`) — merged 2026-08-28 in that order (library-first gate)
- **Repos:** PyAutoArray (`inversion/inversion/imaging_numba/inversion_imaging_numba_util.py`, `operators/over_sampling/over_sampler.py`, test modules), PyAutoGalaxy (`profiles/light/linear/abstract.py` + tests), autolens_profiling (`scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`)
- **Epic:** none — **phase 2 of 2**, successor to `complete/2026/08/numba-hst-curvature-matrix-speedup.md` (PyAutoArray#505/#506)
- **Status: SHIPPED.** The goal (HST rectangular ~0.60 s -> ~0.35 s, likelihood unchanged to pinned tolerance) is met with margin.

## The headline

Phase 1 left F no longer dominant and named two residuals: the mapper x mapper block of `F` (46% of a 0.62 s HST rectangular numba evaluation) and the MGE operated mapping matrix (37%). Step 0 instrumented both before anything was optimised — and, as in phase 1, the split moved the lever. **78% of the MGE row was profile evaluation, not the PSF convolution** phase 1 had already batched, and the mapper x mapper kernel does exactly **1.773e8** inner accumulations at the HST fiducial (the plan's estimate was "~2e8").

Paired B/A/B/A in one session on real datasets — three arms, three rounds per cell in rotating arm order, the first round discarded because numba `cache: true` recompiles on an arm switch, mean of the last two; `OMP_NUM_THREADS=1`, `AUTOARRAY_NUMBA_OPERATED_MEMO=0`, `n_repeats=10`:

| cell | base (`1b89404b`) | after steps 1-2 | final | whole phase |
|---|---|---|---|---|
| hst rectangular, step total | 0.6214 s | 0.4324 s | **0.3334 s** | **1.86x** |
| hst rectangular, direct eval | 0.6184 s | 0.4207 s | **0.3013 s** | **2.05x** |
| euclid rectangular | 0.2226 s | 0.1870 s | **0.1417 s** | 1.57x |
| hst Delaunay-1250 | 0.6331 s | 0.6076 s | **0.4884 s** | 1.30x |
| hst: F mapper x mapper | 0.2581 s | 0.0819 s | 0.0825 s | **3.13x** |
| hst: MGE total | 0.1970 s | 0.1937 s | **0.0844 s** | 2.33x |

Rows the change does not touch hold still (`Blurred image` 0.98-1.02x, the batched MGE PSF convolution 0.96-1.00x) — the control on the paired session.

## The four changes

1. **Oracle the mapper x mapper kernel, then hoist its row gathers** (`a583f1a6`). The kernel had no direct unit test; it now has one pinned to `F = M.T W M` with a dense `W`, plus a symmetry / halved-diagonal test, with the pre-change quadruple loop retained as `curvature_matrix_via_sparse_operator_reference_from`. The hoist takes 1-D row views once per data pixel instead of re-gathering from wide-stride 2-D arrays `u0` times, leaving the accumulated expression operand-for-operand identical. Bit-identical; 1.04-1.12x.
2. **The two-stage source-space accumulator** (`88e14bc6`) — the phase's biggest single win. `w0` does not depend on `data_1`, so the sum factorises into a per-data-pixel dense accumulator over source space followed by contiguous AXPYs over whole rows of `F`: ~1.8e8 irregular read-modify-writes into a 4.9 MB matrix become ~4.4e7 L1 scatters plus vectorisable dense adds. **2.90x on the block at HST.** `CURVATURE_TWO_STAGE_MAX_PIX_PIXELS = 4096` is an explicit module-level constant carrying the measured `pix_pixels` sweep (crossover at or beyond 8192 on both production geometries, outside the range a PyAuto pixelization runs at), overridable per call — not a silent heuristic.
3. **Cache the `OverSampler`'s non-uniform binning divisor** (`d8bc3bac`). `binned_array_2d_from` recomputed `np.bincount(segment_ids)` *and* the `sub_is_uniform` check on every call — 120 calls per evaluation for a 60-Gaussian MGE, and once more for every ordinary numpy light profile. Both depend only on the constructor's `sub_size` and are now `cached_property`. On the HST over sampler (17980 sub-pixels into 15361 pixels) the divisor cost 38.8 us and the uniformity check 61.3 us per call, against 81.5 us for the whole cached call. Bit-identical; the cached divisor is read-only, because the old code guarded zero counts by mutating in place.
4. **One eccentric-radius grid per MGE group** (PyAutoGalaxy#590). An MGE is a `LightProfileLinearObjFuncList` of tens of `Gaussian`s sharing `centre` and `ell_comps` and differing only in `sigma`. Every `image_2d_from` redid the same reference-frame transform (an `arctan2`, a `sin` and a `cos` per coordinate) and the eccentric radii from it — cProfile put the transform alone at 951 us of the 1.3 ms each profile took. `_image_slim_list_from` now groups profiles by `(class, centre, ell_comps)`, computes each group's transform and radii once, and evaluates each profile's `image_2d_via_radii_from` against them. Both the data grid and the blurring grid go through it, so the numpy batched-convolution path picks it up too. 60x `image_2d_from(grid)` 0.0867 -> 0.0168 s, 60x on the blurring grid 0.0346 -> 0.0092 s.

## Verification

- `test_autoarray` **1326 passed** (1296 at the phase-1 baseline; +12 step 1, +18 step 2, +3 step 3). `test_autogalaxy` **1149 passed** (1144 before; +5).
- **Oracle tests were written against the unmodified kernel before any change**, with recorded control runs: a deliberately wrong constant and a dropped diagonal doubling each fail them; dropping the step-2 accumulator clear gives 17 failed 1 passed; a wrong dispatcher branch, 1 failed. PyAutoGalaxy's controls: dropping the transform, elliptical instead of eccentric radii, transforming the un-over-sampled grid, removing the `image_2d_from`-identity membership test — each fails the new tests.
- **All three pinned log likelihoods unchanged to every recorded digit** at explicit `rtol=1e-6`, on every arm: hst bilinear 27661.91013366411, hst RTU 27180.70471569685, hst Delaunay 29090.527210448134. euclid (unpinned) 6213.306873885871.
- `inversion.curvature_matrix`, same instance per arm: **bit-identical for step 3 alone**; max rel `1.24e-14` (hst) / `2.63e-15` (euclid) across the whole phase, `np.allclose(rtol=1e-12)` True. The MGE operated mapping matrix is **bit-identical base -> final** (`np.array_equal` on the 60 x 15361 mapping matrix and the 60 x 5960 blurring stack).
- **The pool run is again the one that mattered.** 8 cores, `PYAUTO_TEST_MODE=1`, 2828 masked pixels, 60-Gaussian linear MGE bulge: 0.2000 -> 0.1697 s per evaluation in a pool of 8, 0.4099 -> 0.3634 s serial, so the parallel speed-up ratio goes **2.05x -> 2.14x**. Flat-to-up is the pass condition — that ratio is what falls if a lever introduces hidden threads.

## Traps recorded

- **Instrument before optimising, again — and it moved the lever again.** The prompt's MGE candidate list pointed at the PSF convolution; 78% of the row was profile evaluation. Step 0's split, not the plan, chose both levers. Two of the four mapper x mapper candidates named at planning time were already dead on arrival (upper-triangle symmetry is exploited, unique-mappings compression is what the kernel already iterates over).
- **Group by shared geometry; do not test all-or-nothing.** The workspace's canonical MGE recipe (`features/multi_gaussian_expansion/modeling.py`) stacks two sets of 30 Gaussians sharing a centre but with their own `ell_comps`, and `GalaxiesToInversion` lands both in one func list. An all-or-nothing check would have fallen back to 60 independent evaluations on exactly the model users are told to write.
- **The membership token is `image_2d_from` function-object identity, not `isinstance`.** That identity is what makes "the transform and the radii are the whole of the shared work" true: subclasses that inherit it (linear, operated, spherical Gaussians) match; `GaussianMultipole`, which overrides it to perturb the radius, does not; `Sersic` and its children do not either — they already avoid the polar transform via `_eccentric_radii_grid_from_cartesian`, a branch taken only when the grid is *not* pre-transformed, so hoisting a transformed grid into them would be both slower and a different floating-point expression.
- **A profiling harness that hand-rolls the library's own path times the old code after the library changes.** `_mge_blurring_stack` used to reimplement the per-profile loop; after #590 it would have kept measuring the *old* code on the new library and mis-attributed the win to the residual row. It now calls the same path `operated_mapping_matrix_override` calls, dispatches on the attribute so both libraries stay measurable, and records the branch it took as `mge_blurring_stack_path` (`shared_geometry` on the final artifacts, `per_profile_loop` on the base arms).
- **A dispatch threshold is a constant with a sweep behind it, not a heuristic.** `CURVATURE_TWO_STAGE_MAX_PIX_PIXELS = 4096` is module-level, documented by the measured crossover, and overridable per call.
- **A branch that was never PR'd has never run the repo's lint gate.** The autolens_profiling step-0 commit left two harnesses failing `ruff format --check`; `origin/main` was clean throughout. A final `ruff format` commit fixed it — worth running the gate locally on any long-lived unopened branch.

## What this leaves

The HST rectangular numba evaluation is 0.33 s, from 1.56 s before phase 1 — **4.7x across the two phases**. No phase 3 is filed: on hst Delaunay-1250 the remaining lead is the inversion build (~0.5 s), explicitly out of scope for both phases, and the rectangular cell's residual rows are all <= ~0.05 s.

One follow-up is named but deliberately not filed here: giving `Gaussian` the same Cartesian eccentric-radius shortcut `Sersic` has would remove the polar transform for *every* Gaussian evaluation, not just an MGE basis — but it moves values, so it is a separate, wider-blast-radius task.

## Heart RED at merge — human override

Merged over the pre-existing Heart **RED score 45** (`pyauto-heart readiness --json`, ts `2026-08-28T21:34:42Z`): `red_reasons: "release validation FAILED (stage integrate)"`; `yellow_reasons: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)"` and `"manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml"`. Human authorisation 2026-08-28, verbatim: *"prm and then kick off phase 2, I authorize the heart RED thing"* — scoped to this task only; release stays human. The RED is pre-existing on `main` and unrelated: the failing workspace scripts sit on the **JAX** likelihood path, while this diff touches only the **numba** imaging-inversion path plus additive-only library changes.

CI was green on every run and every matrix leg before each merge — 4 runs, 8 legs, no push-event runs on these branches (all three repos fire on `pull_request`): PyAutoArray `Tests` (`unittest (3.12)`, `unittest (3.13)`, `unittest-nojax`); PyAutoGalaxy `Tests` (the same three) + `Docs` (`docs-build`); autolens_profiling `lint`.

## Parallel claim

autolens_profiling was claimed simultaneously by `nuts-warm-start-driver-and-a100-probe`, with a human-approved second worktree and disjoint file sets (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`). Explicit pathspecs only, never `git add -A`, in that repo. That worktree stays claimed and was not touched at close-out.

## Original prompt

# Numba CPU likelihood at HST resolution, phase 2: the mapper×mapper block and the MGE operated matrix

Type: feature
Epic: none (successor to `numba_cpu_hst_curvature_matrix_speedup`, PyAutoArray#505)
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @autolens_profiling
Themes:
- numba-cpu
- pixelization
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-08-28
Issued: 2026-08-28
Blocked-by: PyAutoArray#505

## Original request

> yeah do that phase 2

(in reply to: "What's left for a phase 2, if you want one: mapper×mapper (0.28 s) and the MGE
operated matrix (0.22 s) now lead at HST.")

## Context

PyAutoArray#505 (branch `feature/numba-hst-curvature-matrix-speedup`, shipping 2026-08-28) routed
the mapper × linear-func block of the curvature matrix F through the batched FFT `Convolver`
(`Convolver.reversed_kernel`), taking F 1.20 → 0.36 s and the HST rectangular numba evaluation
1.56 → 0.60 s (`OMP_NUM_THREADS=1`, `AUTOARRAY_NUMBA_OPERATED_MEMO=0`, paired same-session
measurements; note in `autolens_profiling/results/notes/numba_curvature_matrix_f_split.md`).

Post-#505 HST rectangular split (0.60 s/eval):

| step | s | share |
|---|---|---|
| F: mapper×mapper [numba sparse-op / w-tilde contraction] | 0.277 | 46% |
| MGE operated mapping matrix (60 funcs, per-eval convolution of varying profiles) | ~0.22 | ~37% |
| F: mapper×linear-func [FFT conv + scatter] | 0.054 | 9% |
| everything else | ≤ 0.02 each | |

Delaunay-1250: mapper×mapper 0.123 s of 0.76 s; F is no longer dominant there — the inversion build
(~0.5 s) is, which is out of scope here.

## Plan findings (2026-08-28)

Two read-through findings changed the task's shape at planning time. First, the **MGE half of the
cost lives in PyAutoGalaxy, not PyAutoArray**: the #505 `Convolver` batching is already applied in
`LightProfileLinearObjFuncList.operated_mapping_matrix_override` (the 60 Gaussians are stacked into
one convolution) and scipy already skips the length-60 axis, so the bulk of the ~0.22 s is the 120
per-profile image evaluations, all of which recompute an identical transform and eccentric-radius
grid because the MGE basis shares `centre`/`ell_comps` and varies only in `sigma` — hence
`@PyAutoGalaxy` added to Repos above. Second, **two of the four mapper×mapper candidate levers are
dead on arrival**: upper-triangle symmetry is already exploited (the sparse preload stores
`ip1 >= ip0` and the kernel folds `A + Aᵀ`) and unique-mappings compression is already what the
kernel iterates over. The live lever is a **two-stage reformulation** — a per-data-pixel dense
source-space accumulator followed by contiguous AXPYs.

## Goal

Take the HST rectangular numba evaluation from ~0.60 s to ≤ ~0.35 s with the log-likelihood
unchanged to pinned tolerance (pins: hst rectangular 27661.910133664103, hst-rtu
27180.704715696862, hst-delaunay 29090.52721044813; rtol 1e-6 where summation order changes,
bit-identical otherwise).

1. **Decompose first, as in #505.** Instrument the mapper×mapper kernel
   (`inversion_imaging_numba_util.py`, sparse-op diag + off-diag kernels) and the MGE operated
   mapping matrix step in the `autolens_profiling` breakdown harness; record the split at hst +
   euclid rectangular and hst Delaunay-1250. Checkpoint: the split picks the lever.
2. **mapper×mapper candidates**, cheapest first: unique-mappings compression (is the inner loop over
   data pixels × PSF footprint × source pixels where a per-unique-mapping formulation is smaller);
   upper-triangle-only + mirror; whether the preloaded PSF-precision products are fully exploited
   (nothing mapper-independent recomputed per evaluation); `prange` measured both at
   `OMP_NUM_THREADS=1` and under the Nautilus pool.
3. **MGE operated matrix candidates**: determine FFT- vs scatter-bound; batch the varying profiles
   through the same `Convolver` path as #505 if the per-func convolution is the cost; check whether
   any profile subset is invariant across evaluations for a given model (memo, already
   `AUTOARRAY_NUMBA_OPERATED_MEMO`).
4. Ship behind parity tests; `test_autoarray` green; smoke
   `autolens_workspace/scripts/imaging/features/pixelization/cpu_fast_modeling.py`; paired
   before/after on the four breakdown cells + one Nautilus pool run; note in `autolens_profiling`.

Out of scope: the JAX path; RTU / kernel-CDF meshes (GPU-only by decision); the Delaunay inversion
build; the NNLS solve.
