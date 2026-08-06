## pointmass-smbh-jax
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/553
- completed: 2026-08-06
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/554 (merged b68df8b0)
- summary: `al.mp.PointMass` and `al.mp.SMBH` failed every JAX-mode fit (user report on 2026.8.4.1). Two independent bugs in `autogalaxy/profiles/mass/point/`: (1) `PointMass.deflections_yx_2d_from` routed through the legacy `radial_grid_from` → `_cartesian_grid_via_radial_from` helpers, which return an `ArrayIrregular` wrapper under `xp=jnp` on the irregular PSF-evaluation grids — `jnp.multiply` rejects it; (2) `SMBH.__init__` used `np.sqrt` on the traced `mass` → `TracerArrayConversionError`. Fixed with raw `xp` ops (mirroring `IsothermalSph`), tracer-safe `** 0.5`, and hardened `potential_2d_from`/`convergence_2d_from` (whose dead central-pixel `argmin` code was deleted).
- validation: `test_autogalaxy/` 1017 passed; PyAutoLens `test_autolens/point/` 115 passed against the branch; jitted `AnalysisImaging.log_likelihood_function` with stock `PointMass` (θ_E free) and `SMBH` (mass free) finite — both reproduced the user errors on unfixed main as controls; deflections parity vs analytic formula 8.7e-19; `jax.grad` finite for all point-mass params.
- traps: (a) `PowerLawSph(slope=3.0)` is NOT a point-mass substitute — the `(3 - slope)` normalisation is NaN at exactly 3. (b) A non-finite `Isothermal.ell_comps` gradient at exactly `(0.0, 0.0)` exists independent of the point mass — pre-existing, not this task. (c) Heart was RED at ship (release-validation integrate stage, unrelated in-flight release arc) — PR-open and merge both explicitly human-authorized; merge also pre-empted PR CI (pending, not failing) and the six-workspace smoke run (only parallel-race false failures observed, none serially confirmed) on human instruction "feels like overkill for a small feature".
- follow-up (unrouted): no CI covers the JAX path for point-mass profiles — consider adding `PointMass`/`SMBH` to an `autogalaxy_workspace_test` JAX parity script so this regression class is caught automatically.

## Original prompt

# al.mp.PointMass and al.mp.SMBH break every JAX fit

Type: bug
Target: PyAutoGalaxy
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

## Original request (verbatim)

> ok do the work on the source code, the user can wait until we do a new release
> so I wont send them the code above

(In response to a user support report: modelling a central black hole in a lens
galaxy with JAX on version 2026.8.4.1 — `al.mp.PointMass` raises
`TypeError: multiply requires ndarray or scalar arguments, got ArrayIrregular`,
and `al.mp.SMBH` raises `jax.errors.TracerArrayConversionError`.)

## Diagnosis (complete — reproduced locally at 2026.8.4.1-8-g9776421a)

Two independent bugs in `PyAutoGalaxy/autogalaxy/profiles/mass/point/`:

1. **`PointMass.deflections_yx_2d_from`** (`point.py:70`) routes through the
   legacy `radial_grid_from` → `_cartesian_grid_via_radial_from` helpers. Under
   `xp=jnp` on the irregular PSF-evaluation grids every imaging fit uses,
   `radial_grid_from` returns an `ArrayIrregular` wrapper which `jnp.multiply`
   rejects. Contrast `IsothermalSph` (`total/isothermal.py:270`), which passes a
   raw `xp.full(...)` radius through the same helper and works. Fix: compute
   deflections with raw `xp` ops on `grid.array`
   (`alpha = einstein_radius**2 / (y**2 + x**2 + 1e-20)`;
   `xp.stack((alpha*y, alpha*x), axis=-1)`), keeping the
   `@aa.decorators.to_vector_yx` + `@aa.decorators.transform` decorators.
2. **`SMBH.__init__`** (`smbh.py:63`) computes
   `einstein_radius = np.sqrt(mass_angular / np.pi)`. With `mass` a free
   parameter the instance is built inside the jit trace, so `np.sqrt` receives a
   tracer → `TracerArrayConversionError`. Fix: `(mass_angular / np.pi) ** 0.5`
   (Python pow is tracer-safe). The astropy critical-surface-density call is
   fine because redshifts stay floats.

Also latent: **`PointMass.convergence_2d_from`** (`point.py:52`) is np-only
(`np.square`/`np.argmin`, hardcoded `np.zeros`, ignores `xp`) — the source of
the non-fatal "Visualization warm-up failed" warning in the user's log. It
returns zeros by design (Dirac-delta convergence); modernise to `xp.zeros` and
tracer-safe ops.

Both fixes were validated end-to-end in the diagnosis session: a jitted
`AnalysisImaging.log_likelihood_function` with subclassed fixed profiles returns
a finite likelihood (stock profiles reproduce both user errors as controls), and
fixed deflections match stock numpy deflections to ~1e-18.

Note: `PowerLawSph(slope=3.0)` is NOT a substitute — the `(3 - slope)`
normalisation makes it NaN at exactly 3.
