# Precompute fixed-geometry Gaussian deflection angles and rescale by the free mass-to-light ratio (numpy + JAX)

Type: feature
Epic: gaussian-deflections-precompute
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @PyAutoLens
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- jax
- profiling
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: with every Gaussian's centre/ell_comps/sigma fixed and only mass_to_light_ratio free, the second and later likelihood evaluations call no Faddeeva/`wofz` kernel (asserted by a call-count probe) and the deflections equal the per-evaluation path to rtol 1e-12 on the `scripts/lens/deflections/` pins.
Review-minutes: 25
Unattended: needs-slicing
Parent: complete/archive/epics/numpy_deflections_cpu_speedup.md
Filed: 2026-09-02

> Successor to the `numpy-deflections-cpu` epic (ledger at the Parent path; phase 1 = autoarray issue #514,
> PRs autoarray #516 / autogalaxy #595 / autolens #718 / autolens_profiling #210). **Start only after
> that epic's three phases are complete** — it is a separate follow-up, not an epic member, because it
> changes how a model's fixed vs free parameters reach the profile code and is likely to be complex.

## Idea (user, 2026-09-02, verbatim)

"we should intake a follow up issue which exploits the fact that if all of the Gaussian light profile
values are fixed and thus only their mass to light ratio is free in a model, we can precompute the
deflection angles and scale them up and down by a constant factor. This could be quite complex and
thus should be a separate follow up issue after this deflection speed up stuff is complete. Also likely
that JAX doesn't use this so would help there."

## Context

The Gaussian mass profile (`autogalaxy/profiles/mass/stellar/gaussian.py`, Faddeeva closed form via
`wofz`) and every MGE-decomposed mass profile (`autogalaxy/profiles/mass/abstract/mge.py`) evaluate the
full per-Gaussian deflection field on every likelihood call, even when the Gaussians' centres,
`ell_comps` and `sigma`s are fixed — the common SLaM case where an MGE lens light was fitted in an
earlier stage and the mass follows the light with a single free `mass_to_light_ratio`. The deflection
field is linear in the Gaussian amplitude, so a fixed-geometry Gaussian's deflections are a constant
vector (per grid) times the free scalar; a stack of N fixed Gaussians sharing one ratio collapses to one
precomputed summed field times the ratio.

Baseline (autolens_profiling `scripts/lens/deflections/`, hst grid 15,361 points, numpy,
`OMP_NUM_THREADS=1`, after phase 1): Gaussian 11 ms / call; gNFW via MGE-30 293 ms / call. Pins and the
`--repin` policy live there (PR #210).

## Levers to scope

1. Detect fixed geometry from the model: prior vs constant (the model's own parameter kinds) on each Gaussian's centre,
   `ell_comps`, `sigma` (and, for MGE-decomposed profiles, the parent's geometry); the free scalar is
   `mass_to_light_ratio` (or the MGE amplitude prefactor).
2. Cache the unit-amplitude deflection field per (grid identity, Gaussian geometry) across likelihood
   evaluations — same cross-evaluation memo shape as `nnls_memo.py` / the operated-matrix memo; key on
   the grid's shape/mask fingerprint and the fixed parameters, kill-switch env var.
3. Rescale by the free ratio per evaluation; N fixed Gaussians with one shared ratio sum once.
4. JAX: a cached unit field becomes a constant folded into the trace (the deflection subgraph
   disappears), so the win is likely larger there than on numpy — measure both.
5. Where the geometry is *not* fixed, nothing changes.

## Gates

Deflections bit-identical (the rescale is one multiply; pins rtol 1e-6 in `scripts/lens/deflections/`);
likelihood pins on the numba cells unchanged; measure numpy and JAX before/after; `test_autogalaxy` /
`test_autolens` green; no new public API beyond what the cache needs.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/d3971bba-0e8d-4c4f-bc59-7808e6bfa6cd/scratchpad/intake_gaussian_precompute.md -->

## Epic log

**2026-09-03 — epic born; phases filed.** Design settled after a code survey: two exact levers behind one
memo, both keyed on **values**, never on model metadata. **L1** — whole-field memo for a fully-fixed mass
profile of any class, keyed on (class name, constructor-argument values, grid fingerprint). **L2** —
Gaussian geometry/amplitude split: store the unit-ratio field, return `m2l x field`; `GaussianGradient` is
not linear in one scalar and takes L1 only. **Grid fingerprint** = `sha256` of `grid.array` bytes + shape +
`pixel_scales`, because `FitDataset.grids` rebuilds the grid every call, so `id(grid)` would never hit.
Lives in one private module `autogalaxy/profiles/mass/abstract/deflections_memo.py` (byte cap 256 MB FIFO,
kill switch `AUTOGALAXY_DEFLECTIONS_MEMO=0`, `memo_stats()` counters), hooked in
`MassProfile.deflections_yx_2d_from` *above* `@transform` so the stored field is the rotated-back field for
the untransformed grid. Numpy path first; under JAX the fixed geometry is concrete and only `m2l` is a
tracer, so the unit field is computed at trace time with scipy and embedded as a constant, removing the
Faddeeva subgraph from the jaxpr. Memo precedent: `PyAutoArray .../imaging_numba/sparse.py:20-51`.

Three phase prompts:
- ~~`draft/feature/autogalaxy/gaussian_precompute_p1_numpy_memo.md`~~ — numpy memo + `_wofz` call-count
  witness. **SHIPPED 2026-09-03** — record `complete/2026/09/gaussian-precompute-p1.md`
  (PyAutoGalaxy#602 + autolens_profiling#214; Basis-30 hst 21.5x, SLaM-shaped likelihood 3.0x
  bit-identical, witness `[60, 0, 0]` vs the `[60, 60, 60]` controls).
- ~~`draft/feature/autogalaxy/gaussian_precompute_p2_jax_trace_time_constant.md`~~ — JAX trace-time
  constant. **SHIPPED 2026-09-03** — record `complete/2026/09/gaussian-precompute-p2.md`
  (PyAutoArray#520 + PyAutoGalaxy#605 + autolens_profiling#216; jaxpr 53,369 → 13,289 equations
  (-75%), `vmap_first_call` 10.8 → 5.4 s, steady-state `vmap` unchanged — inversion-dominated).
- `draft/feature/autogalaxy/gaussian_precompute_p3_downstream_sweep.md` — SLaM / test_autolens / workspace sweep.

**2026-09-03 — phase 3 SHIPPED to PR-open (autolens_workspace#530).** Downstream sweep on the merged
library mains (PyAutoGalaxy `65af1122`, PyAutoArray `e36a5af4`); the phase adds no mechanism, it verifies
the memo on the driver it was built for and documents the kill switch. `test_autolens` **610 passed**
(1 xfailed). SLaM `imaging/features/advanced/mass_stellar_dark/slam.py` in test mode, 3 repeats per leg:
every stage's max-log-likelihood **bit-identical** memo on vs off; `mass_light_dark[1]` **0.370 s on vs
0.515 s off** (0.72x), every stage at or below memo-off; `memo_stats` **119 hits / 20 misses / 0 evictions
/ 119 kB / 20 entries**; the kill-switch leg reads all zeros. **Store-churn finding NEGATIVE** — the
linear-Sersic light with a free ratio (an L1 profile whose key changes every call) showed no churn
penalty at this scale, so no library change is proposed. autolens_workspace_test: **4 scripts** run
(`imaging/jax_likelihood/mge.py`, `imaging/jax_grad/mge.py`, `imaging/visualization/modeling_visualization_jit.py`
pass; `interferometer/visualization/modeling_visualization_jit.py` OOM-killed in its live-Nautilus Part 2,
which is exactly its **pre-existing `no_run.yaml` SLOW/OOM entry**), **pins unchanged**. Numba likelihood
pins held: `pixelization_numba` hst **27661.9102** (rel **2.65e-9**, within 1e-6) and
`pixelization_numba_mge_mass` **exact** (bit-identical), memo **2.61x** per call at hst resolution — the
production-scale number for this shape, since test mode calls the likelihood once per stage. Doc: one
paragraph in the `mass_light_dark` pipeline docstring plus the regenerated notebook. The epic closes at
`/prm` on autolens_workspace#530.
