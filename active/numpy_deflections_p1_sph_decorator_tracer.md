# Numpy deflections phase 1: measure (scripts/lens), fix the *Sph over-sampled re-materialisation, drop the tracer double trace

Type: feature
Epic: numpy-deflections-cpu
Phase: 1
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-09-02
Issued: 2026-09-02

> Phase 1 of the `numpy-deflections-cpu` epic — ledger
> `draft/feature/autogalaxy/numpy_deflections_cpu_speedup.md`, which holds the measured before-table,
> the goal (every one of the nine numpy `deflections_yx_2d_from` at least 2× faster on the HST grid,
> the four `*Sph` ≥ 100×, gNFW/gNFWSph ≥ 5×), the request's constraints (no new public functions,
> keep the `xp` API single-bodied) and the approved decisions 1–5. This phase lands the measurement
> package the whole epic reports through, then takes the two levers that change no numerics at all:
> the `*Sph` over-sampled re-materialisation (~500× on four profiles) and the tracer's double trace
> (~2× at tracer level on every profile). Issue on **PyAutoArray** (the load-bearing code change),
> cross-referenced from the other PRs.

## Goal

`scripts/lens/deflections/` measuring all nine profiles on hst + euclid with committed baseline
artifacts, then two zero-numerics fixes: `*Sph` ≥ 300×, tracer-level cost ≈ 2× cheaper for every
profile on sub-size-1 grids. Deflections and likelihoods bit-for-bit unchanged (rtol 1e-6 pins).

Branch `feature/numpy-deflections-p1`, worktree `~/Code/PyAutoLabs-wt/numpy-deflections-p1/`.

## Step 0 — `autolens_profiling/scripts/lens/deflections/` (baseline committed BEFORE any library edit)

```
scripts/lens/README.md                      axis narrative, links down
scripts/lens/deflections/README.md          <!-- BEGIN auto-table:deflections -->
scripts/lens/deflections/_driver.py         grid construction (as pixelization_numba.py: Mask2D.circular r=3.5",
                                            radial over-sampling [4,2,1]@[0.3,0.6], pixelization sub-size 1),
                                            timing loop, separate cProfile pass, pin check, JSON+PNG write
scripts/lens/deflections/_profiles.py       registry: name -> (ctor, fiducial params, family)
scripts/lens/deflections/total.py           Isothermal, IsothermalSph, PowerLaw, PowerLawSph
scripts/lens/deflections/dark.py            NFW, NFWSph, gNFW, gNFWSph
scripts/lens/deflections/stellar.py         Gaussian (ell + ell_comps=(0,0))
results/lens/deflections/<cell>_summary_<instrument>_v<version>.{json,png}
results/notes/numpy_deflections_cpu.md      before table + epic ledger
```

- Each cell: the standard prologue (`ruff.toml` root-finder, `sys.path`, `AUTOLENS_PROFILING_SMOKE`
  early exit as `pixelization_numba.py:82-93`), `parse_profile_cli` + `--instrument {hst,euclid}`,
  `resolve_output_paths`, `device_info_dict`. Per profile: median-of-N s/call on `Grid2D`, on
  `Grid2DIrregular` (`grids.lp.over_sampled`), and through a two-plane `Tracer`; n_points; cProfile
  top-12 (`cprofile_top`, per-call, attribution only, separate pass); pin block
  `{abs_sum, abs_max, sample}` with 16 fixed `(y, x)` arcsec coordinates (8 @ r=1.0", 4 @ 0.15",
  4 @ 2.8") on a dedicated `Grid2DIrregular`, checked rtol 1e-6 via `check_pinned` + a small
  `check_pinned_vector` helper added beside `_profile_cli.py:313`; drift recorded, never adjudicated.
  `--repin` requires `--repin-reason`, refuses shifts > `--repin-max-shift` (1e-3) without
  `--repin-force`, embeds `pin_provenance` in the JSON.
- `build_readme.py`: no scan-root or regex change (artifacts use the `summary` purpose token; the
  `rglob` already walks `results/lens/`); add `_render_deflections_table` beside `:444-479`,
  register `"deflections"` in `_build_renderers` (`:762-771`), add the new README to
  `TARGET_READMES` (`:779-788`, via `REPO_ROOT`), fix the comment at `:192` and docstring `:20-42`.
- `lint.yml:131-146` smoke gains `python scripts/lens/deflections/total.py`; workflows README row.
- `README.md:142-144` amended: `scripts/lens/` is a second top-level axis (library-component
  profiling, dataset-free) beside the dataset-first families (epic decision 4).
- Ruff clean; `build_readme.py --check` clean.

## Step 1 — PyAutoArray: the `*Sph` bug + the sub-size-1 short-circuit

The `*Sph` ~500 ms is a decorator bug, not physics. `EllProfile.transformed_to_reference_frame_grid_from`
(`geometry_profiles.py:402-417`, `@to_grid`) delegates to the also-`@to_grid` `SphProfile` method
(`:158`); the outer `GridMaker.via_grid_2d` (`autoarray/structures/decorators/to_grid.py:17-18`)
then does `getattr(result, "over_sampled", None)` on the wrapped `Grid2D`, firing the property and
its per-pixel Python loop (`over_sample_util.py:417-429`) on every call. The materialised value is
also semantically wrong (mask-derived, so not translated by the profile centre) — nothing reads it.

- `autoarray/structures/decorators/to_grid.py:17-18` (and `:26-27`): read `_over_sampled` /
  `_over_sampler` instead of the properties. Identity for the two load-bearing callers
  (`galaxy.py:381`, `tracer.py:513` set them explicitly); lazy recompute elsewhere gives the same
  answer (same mask/sub-size inputs). Verified: 0.644 s → 0.0016 s, max abs diff 0.0.
- `autoarray/structures/grids/uniform_2d.py:211-224` `Grid2D.over_sampled`: return
  `Grid2DIrregular(self.array)` when all sub-sizes are 1 (verified bit-identical — same points, same
  order). Kills the ~1.5 s Python loop for every sub-size-1 grid.
- Tests in `test_autoarray/structures/decorators/test_to_grid.py`: (i) negative pin —
  monkeypatch `Grid2D.over_sampled` to fail, `IsothermalSph.deflections_yx_2d_from` must return;
  (ii) positive pin — an explicit `over_sampled=` sentinel survives `via_grid_2d`; (iii) sub-size-1
  `over_sampled` equals the slim grid; sub-size-4 still differs.

## Step 2 — the double trace

`Tracer.traced_grid_2d_list_from` traces every `Grid2D` twice (`autolens/lens/tracer.py:490-505`:
`grid`, then `grid.over_sampled`); `Galaxy.traced_grid_2d_from` (`galaxy.py:376-383`) does the same.
With a uniform size-1 over-sampler (the pixelization grid in every numba cell) the second trace is
100 % redundant: Isothermal 1.4 → 3.5 ms, PowerLaw 7.4 → 15.5 ms through the tracer.

- `PyAutoLens/autolens/lens/tracer.py:498-501`: when `np.all(grid.over_sample_size.array == 1)`
  (host-side static bool, safe under `jit`), wrap the already-traced `grid_2d_list` as the
  over-sampled list instead of tracing again. Same in `PyAutoGalaxy/autogalaxy/galaxy/galaxy.py:376-383`.
- Test in `test_autolens/lens/test_tracer.py`: traced `.over_sampled` equals `traced(g.over_sampled)`
  and differs from `g.over_sampled` (pins that the tracer's explicit value still survives), for
  sub-size 1 and 4.

## Ship (library-first)

PyAutoArray PR → PyAutoGalaxy PR → PyAutoLens PR → autolens_profiling PR with the after-numbers:
re-run `total.py`/`dark.py`/`stellar.py` hst + euclid; re-run `pixelization_numba.py` +
`delaunay_numba.py` hst + euclid (likelihood pins rtol 1e-6 — hst rectangular 27661.910133664103;
the "Inversion build (trace+mesh+mapper)" row should drop); re-run the `jax_compile` warm-compile
pins (one fewer duplicate subgraph).

## Verification

- `test_autoarray`, `test_autogalaxy`, `test_autolens` green; smoke
  `autolens_workspace/scripts/imaging/features/pixelization/cpu_fast_modeling.py`.
- Baseline artifacts committed before any library edit; after-artifacts in the profiling PR;
  README auto-table regenerated (`build_readme.py --check` is a lint gate).
- `ruff check` + `ruff format --check`; lint smoke green.
- Expected: `*Sph` ≥ 300×, tracer-level cost ≈ 2× for every profile on sub-size-1 grids.

## Out of scope

Numerics of any profile (phases 2 and 3); the JAX path's speed; CSE; `convergence_2d_from` /
`potential_2d_from`; new mass profiles or public methods.
