# Numpy (CPU) deflection angles: speed up the nine mass profiles the numba likelihood route evaluates

Type: feature
Epic: numpy-deflections-cpu
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @PyAutoArray
- @PyAutoLens
- @autolens_profiling
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-09-02
Issued: 2026-09-02

> The numba CPU likelihood route (`use_jax=False`, `apply_sparse_operator_cpu()`) is now
> 0.33 s per HST rectangular evaluation (21.3 s at the start of the epic). Its mass-profile
> deflections run on the plain-numpy `xp=np` branch, which was never tuned for CPU. This task
> tunes it, keeping the shared `xp` API wherever the JAX and numpy code can stay one body.

## Where the time goes now (2026-09-02 probe, HST grid from `pixelization_numba.py --instrument hst`: 15,361-point `Grid2D`, `OMP_NUM_THREADS=1`, median of 5)

| profile | s/call | what dominates |
|---|---|---|
| Isothermal | 0.0014 | near-optimal; `axis_ratio` re-derived ~8×/call, `transform_grid_2d_to_reference_frame` ~1 ms floor |
| NFW | 0.0024 | HK24 closed form; both `where` branches evaluated in full |
| Gaussian | 0.0064 | hand-rolled `wofz` (`stellar/gaussian.py:189`), all 3 branches evaluated then `where`-selected |
| PowerLaw | 0.0074 | `scipy.special.hyp2f1` on complex z (~35 %); `axis_ratio` re-derived 11×/call |
| gNFW | 0.202 | MGE-30: `MGEDecomposer.wofz` on `(30, N)` complex128, 3 branches × 2 calls, decomposition rebuilt per call |
| **PowerLawSph** | **0.483** | decorator bug (below); physics ≈ 1 ms |
| **IsothermalSph** | **0.490** | same |
| **NFWSph** | **0.527** | same (+ complex-valued `coord_func_f_from` for a real result) |
| **gNFWSph** | **0.830** | same + elliptical MGE at `q=0.9999` for a spherical profile |

`GaussianSph` is not a mass profile (only a light profile); the spherical case is
`Gaussian(ell_comps=(0, 0))`, which takes the elliptical path unchanged. Nine profiles, not ten.

The `*Sph` cost is `EllProfile.transformed_to_reference_frame_grid_from` (`geometry_profiles.py:416`,
`@to_grid`) delegating to `SphProfile.transformed_to_reference_frame_grid_from` (`:158`, also
`@to_grid`), after which `GridMaker.via_grid_2d` (`PyAutoArray/.../decorators/to_grid.py:17`) does
`getattr(result, "over_sampled", None)` on a fresh `Grid2D` — firing the `Grid2D.over_sampled`
property and its per-pixel Python loop (`over_sample_util.py:377`) on **every** deflection call.

Tracer overhead: `Tracer.traced_grid_2d_list_from` (`autolens/lens/tracer.py:490-505`) traces a
`Grid2D` twice (grid + `grid.over_sampled`) even when the over-sampler is uniform size 1 and the
points are identical. Isothermal raw 1.4 ms → 3.5 ms through the tracer; PowerLaw 7.4 → 15.5 ms.
A full evaluation pays deflections on `grids.pixelization`, `grids.lp`, `grids.lp.over_sampled`
and the blurring grid.

## Goal

Every one of the nine profiles' numpy `deflections_yx_2d_from` at least 2× faster on the HST grid
(the `*Sph` four ≥ 100×, gNFW/gNFWSph ≥ 5×), with deflections unchanged to rtol 1e-6 against a
pinned reference — or, where the old routine is the less accurate one (hand-rolled `wofz` is
~6 significant digits: 2.7e-6 abs vs `scipy.special.wofz`), re-pinned against a high-precision
(`mpmath`) reference recorded in the note. Existing numba likelihood pins unchanged (hst rectangular
27661.910133664103, rtol 1e-6).

Constraints from the request:
- **No new public functions.** Fast paths are branches inside the existing methods; `*Sph` profiles
  that inherit the elliptical parent get their speed from the parent.
- **Keep the `xp` API single-bodied** wherever the numpy and JAX code can share one path. Split only
  where an `xp is np` branch buys a clear win (the `wofz` swap, `hyp2f1` → series, `lstsq`).
- Profiling for this work lives in a new `autolens_profiling/scripts/lens/` package, in the same
  style as the rest of the repo (versioned JSON + PNG under `results/lens/`, README auto-table via
  `build_readme.py`, `AUTOLENS_PROFILING_SMOKE` import smoke, pin checks).

## Phases & state

The Brain (`pyauto-brain feature`) scored the whole body of work *too-large* and returned
**split-into-phases**: four repos × eight levers. One Mind prompt per phase, one issue per phase,
library-first ship inside each phase.

| phase | prompt path | repos | levers | status |
|---|---|---|---|---|
| 1 | `draft/feature/autoarray/numpy_deflections_p1_sph_decorator_tracer.md` | @PyAutoArray, @PyAutoGalaxy, @PyAutoLens, @autolens_profiling | measure (`scripts/lens/deflections/`), `*Sph` over-sampled re-materialisation, sub-size-1 short-circuit, tracer double trace | draft — starting 2026-09-02 |
| 2 | `draft/feature/autogalaxy/numpy_deflections_p2_mge_wofz.md` | @PyAutoGalaxy, @autolens_profiling | `scipy.special.wofz` on numpy, spherical MGE branch, cached decomposition | draft |
| 3 | `draft/feature/autogalaxy/numpy_deflections_p3_closed_form_geometry.md` | @PyAutoGalaxy, @PyAutoArray, @autolens_profiling | PowerLaw series with factor-driven term count, NFW/NFWSph masks, Isothermal hoists, rotation-matrix grid transform | draft |

Phase 1 carries the measurement package: every later phase's before/after numbers come from the
cells it lands, so it is a hard predecessor of phases 2 and 3. Phases 2 and 3 touch disjoint files
and could run in either order.

## Ledger

Append-only. Dated entries; newest at the bottom.

**2026-09-02 — born.** Probe on the HST grid (`pixelization_numba.py --instrument hst`, 15,361
points, `OMP_NUM_THREADS=1`, median of 5) produced the table above: `*Sph` 0.48–0.83 s/call against
~1 ms of physics, gNFW 0.202 s, PowerLaw 0.0074 s, Gaussian 0.0064 s, NFW 0.0024 s, Isothermal
0.0014 s. Brain classification: feature / autogalaxy; repos autoarray + autogalaxy + autolens +
autolens_profiling; difficulty large (derived *too-large*); workflow combined; **split-into-phases**.
Vitals at birth: library + workspace CI green; worktree drift = another task's dirty worktree plus
this prompt in canonical Mind; release validation "no rehearsal evidence" (not a dev blocker).

Decisions 1–5 below were put to the human and **approved 2026-09-02**:

1. **Phasing.** Epic `numpy-deflections-cpu`, three phases, one Mind prompt each; this session
   starts phase 1. Today's prompt becomes this ledger (+ an `epics.md` entry). Rejected
   alternative: one task / one worktree / four PRs — legal, but it is exactly the shape the Brain
   scored too-large.
2. **PyAutoArray claim conflict.** `worktree_check_conflict` fires: PyAutoArray is claimed by
   `numba-vs-jax-sparse`, which is a **read-only research verdict on `main` — no branch, no
   worktree**. File sets are trivially disjoint. Approved: own worktree, `parallel-claim:` recorded
   on the `active.md` entry (the 2026-08-26 #176/#177 precedent).
3. **`autolens_profiling` canonical checkout is on `feature/refs-v1-redo-ruling`** (another task's
   clean branch). The task worktree branches from `origin/main`; the canonical checkout is left
   untouched.
4. **`scripts/lens/` is a second top-level axis** in autolens_profiling — library-component
   profiling, dataset-free — beside the dataset-first families; `README.md:142-144` amended to say
   so. Rejected alternative `scripts/misc/deflections/`: the family will grow (convergence,
   potential, shear) and is different in kind from `misc`.
5. **Accuracy re-pins.** Where the old routine is the *less* accurate one (hand-rolled `wofz` ≈ 6
   significant digits, 2.7e-6 abs vs `scipy.special.wofz`), deflections may move up to ~3e-6
   relative and are re-pinned against an `mpmath` reference recorded in the note, via an explicit
   `--repin --repin-reason` flow. Everything else holds rtol 1e-6 against pinned before-values.

**2026-09-02 — phase 1 step 0 landed (autolens_profiling 6b652dc + 4fd5a09 on
`feature/numpy-deflections-p1`, PyAutoArray#514).** `scripts/lens/deflections/{total,dark,stellar}.py`
+ `_driver.py`/`_profiles.py`, six baseline artifacts (hst + euclid) under `results/lens/deflections/`,
note `results/notes/numpy_deflections_cpu.md`, README auto-table `deflections`, lint smoke row.
Three findings that correct the premise:
- **The `*Sph` ~500 ms penalty is on the direct `Grid2D` entry only.** `tracer_util.traced_grid_2d_list_from`
  wraps each plane in `Grid2DIrregular` before calling the profiles, so production ray-tracing never pays it
  (hst IsothermalSph: 699 ms direct vs 3.6 ms through the tracer). The fix stays (zero-numerics, removes a
  real trap for direct calls, `Galaxy.traced_grid_2d_from`, plotting), but the likelihood-side phase-1 win
  is the double-trace removal, not this.
- **`PowerLawSph` returns 2 non-finite deflections on both grids** (closed form divides by the radius at
  the exact centre). Pins are nan-aware and pin `n_non_finite` separately; a centre guard is a library
  follow-up, out of scope here.
- **Laptop timing variance is ~30 % between passes** (gNFWSph hst 0.88 / 1.04 / 1.20 s). An "after" must
  clear that band; ratios are the reproducible result.
Baseline hst (Grid2D / Irregular / Tracer): Isothermal 2.0 / 2.2 / 6.1 ms; PowerLaw 11.2 / 12.7 / 25.1 ms;
NFW 5.8 / 5.9 / 7.1 ms; Gaussian 11.0 / 12.4 / 23.7 ms; gNFW 358 / 446 / 721 ms; IsothermalSph 699 / 1.3 /
3.6 ms; PowerLawSph 701 / 1.5 / 3.7 ms; NFWSph 591 / 9.9 / 14.2 ms; gNFWSph 1205 / 384 / 674 ms.

**2026-09-02 — phase 1 SHIPPED to PR-open (PyAutoArray#514).** PRs, merge order: PyAutoArray#516
(`to_grid` reads `_over_sampled`/`_over_sampler`; `Grid2D.over_sampled` + `over_sampler` short-circuit at
sub-size 1) → PyAutoGalaxy#595 (`Galaxy.traced_grid_2d_from` no second deflection call at sub-size 1) →
PyAutoLens#718 (`Tracer.traced_grid_2d_list_from` same) → autolens_profiling#210 (`scripts/lens/` axis,
before/after, note). Suites: test_autoarray 1362, test_autogalaxy 1158, test_autolens 576, all green;
every deflection pin held at rtol 1e-6 with no `--repin`; numba likelihood pins bit-identical on both
A/B arms; workspace smoke `cpu_fast_modeling.py` exit 0. Heart YELLOW acknowledged (PyAutoArray PR 10d
old; no release rehearsal) — recorded on `active.md`.
After (hst, Grid2D direct → / Tracer →): IsothermalSph 699 ms → 0.99 ms (710×) / 3.6 → 1.4 ms;
PowerLawSph 701 → 1.2 ms (570×); NFWSph 591 → 4.2 ms (142×); gNFWSph 1.21 s → 301 ms (4.0×, MGE remains);
Tracer 1.7–3.9× on every profile (Isothermal 6.1 → 2.7 ms, PowerLaw 25.1 → 9.0 ms, gNFW 721 → 281 ms).
Negative result, reported as such: the numba breakdown `Inversion build` row moves 1–2 ms on an
Isothermal lens — inside host noise — because Isothermal deflections were already ~2 ms; the tracer
saving scales with the profile (PowerLaw/gNFW models gain 16–440 ms per evaluation at tracer level).
`jax_compile` warm compile 321 → 268 ms under unequal load: inconclusive, not re-pinned. Tracked breakdown
artifacts left untouched (load-contaminated re-runs are not a valid after). Phases 2 and 3 unblocked
once #516/#595/#718 merge (their cells and pins are on the #210 branch).

## Gates

Every phase must clear all four before it ships:

- **Per-profile deflection pins, rtol 1e-6** against the values pinned by the phase-1 cells
  (`{abs_sum, abs_max, sample}` on a 16-point `Grid2DIrregular`). Re-pinning is allowed only through
  `--repin --repin-reason`, refuses shifts > `--repin-max-shift` (1e-3) without `--repin-force`, and
  embeds `pin_provenance` in the JSON. The documented exceptions are decision 5 above: the
  hand-rolled-`wofz` replacements in phase 2, re-pinned against an `mpmath` reference recorded in
  `results/notes/numpy_deflections_cpu.md`.
- **Likelihood pins, rtol 1e-6**: `pixelization_numba.py` and `delaunay_numba.py`, hst + euclid —
  hst rectangular **27661.910133664103**.
- **Before/after artifacts** committed under `autolens_profiling/results/lens/deflections/` as
  versioned `<cell>_summary_<instrument>_v<version>.{json,png}`, with the README auto-table
  regenerated (`build_readme.py --check` is a lint gate).
- **Suites green**: `test_autoarray`, `test_autogalaxy`, `test_autolens`; `ruff check` +
  `ruff format --check`; lint smoke.

Out of scope: the JAX path's speed; CSE (not on any of the nine default deflection paths — NFW's CSE is
opt-in); `convergence_2d_from` / `potential_2d_from`; new mass profiles or public methods.

## Original request (verbatim)

We recently made CPU run times with the numba route amazingly fast, well done! Look up the history of this work we
did a few days ago.

I now want to speed up the deflection angle part oft his likelihood function, noting that because it does not use
JAX It uses the pure numpy route which has no necessarily been optimized for CPU and is not necessarily the fastest
implementation.

In particular, I want all of the follow numpy caclulations of deflection angles to be sped up:

- PowerLaw
- PowerLawSph
- Isothermal
- IsothermalSph
- NFW
- NFWSph
- gNFW
- gNFWSph
- Gaussian
- GaussianSph

Dont add new functions, so if any of these Sph methods use the elliptical parent just speed up that.

Where possible, aim to just keep the numpy route and .xp API, so we dont split the numpy code from the JAX Code
and thus make everything twice as long. However, if there are situations where different code paths for numpy and JAX
lead to obvious performance improvements, then it is acceptable to split the code.

Some of these use MGE / CSE decompositions and therefore this task will probably turn into also optimizing up both those
calculations.

I think autolens_profilng suits having deflection angle profilng and othr such computations being coded out, tracked
and whatnot in the same style as everything there. So in scripts make a "lens" package which contains all this information
and the work done for this task.
