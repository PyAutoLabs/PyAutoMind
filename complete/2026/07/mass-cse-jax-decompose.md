## mass-cse-jax-decompose
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/499 (closed)
- completed: 2026-07-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/500 (merged b8bc0a3e, squash)
- repos: PyAutoGalaxy
- summary: incomplete Sérsic-stellar-mass CSE→JAX port (chaining.py FAIL) — thread xp through Sersic CSE deflection path, branch-free cse_settings_from, jnp.linalg.lstsq on JAX path. NOT jax-0.10.2. Release-tail item F. Corrective validation GREEN on v2026.7.14.1.dev66001 (integrate:pass); Heart YELLOW. See project_cse_mass_jax_trace_bug.

## Original prompt

# group/mass_stellar_dark chaining fails with a JAX exception on release wheels

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoGalaxy
- PyAutoArray
Difficulty: hard
Autonomy: supervised
Priority: normal
Status: diagnosed
Fix-locus: PyAutoGalaxy (autogalaxy/profiles/mass — CSE decomposition path)
Workflow: library
Strategy: full jnp trace of the CSE decomposition; freeze total_cses/sample_points
  to a conservative static max (~50/80) on both paths (static shapes under jit);
  phased — P1 unblock chaining, P2 Sersic-range + NFW parity harden.

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the
release wheels under the release profile:

```
scripts/group/features/advanced/mass_stellar_dark/chaining.py ... FAIL (26.6s)
  For simplicity, JAX has removed its internal frames from the traceback of the following
  exception. Set JAX_TRACEBACK_FILTERING=off to include these.
```

The run-runner captured only the filtered banner, not the actual exception — it is a **real
JAX error** during a group-scale mass_stellar_dark **chaining** pipeline (real sampler,
`PYAUTO_TEST_MODE=1` for user workspaces), and fails fast (26.6 s), so it is NOT a timeout
(distinct from the other `group/`/`chaining` scripts that TIMEOUT and are handled by the
release timeout bump PyAutoHeart#c19c948).

Reproduce from the `autolens_workspace` checkout on current main under the release profile,
with `JAX_TRACEBACK_FILTERING=off` to get the real traceback:

```
cd autolens_workspace
JAX_TRACEBACK_FILTERING=off PYAUTO_TEST_MODE=1 PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1 \
  python scripts/group/features/advanced/mass_stellar_dark/chaining.py
```

The dev venv is now jax 0.10.2 (matches the release stack — see
[[reference_laptop_gpu_jax_setup]]), so this should reproduce locally. Candidate causes given
the release-validation context: a jax-0.10.2 numerical/behaviour change in the chained
group-scale fit (cf. the jax-drift and LinAlg-not-PD siblings), a NaN/inf in a chained-prior
pass, or a real group/mass_stellar_dark modelling issue. Classify (jax regression vs real
bug) and fix at the right layer. Release run: PyAutoHeart workspace-validation `29279095224`,
TestPyPI `2026.7.13.1.dev65601`. See [[project_release_2026_07_13_blocked_3bugs]] and
PyAutoHeart#72.

## Diagnosis (2026-07-14, reproduced locally on jax 0.10.2)

**Classification: real library bug (incomplete JAX port of the CSE mass-profile
decomposition), NOT a jax-0.10.2 regression.** jax 0.10.2 is incidental — the
release stack simply jits the likelihood; the same code fails on any jax version.

Reproduced on `autolens_workspace` main with `JAX_TRACEBACK_FILTERING=off`.
search[1] (lens light) is cached; **search[2]__mass_stellar_dark** crashes on the
first jitted likelihood eval. The lens mass is a Sersic (stellar) + NFW (dark)
model; the Sersic *mass* profile deflections go through the CSE decomposition
path, which is only partially JAX-threaded:

1. **`PyAutoArray` `.../decorators/abstract.py`** (`AbstractMaker._xp`) resolves the
   backend from the `xp` passed *into* the decorated call. So a dropped `xp` at a
   call site silently becomes `xp=np`.
2. **First crash — `PyAutoGalaxy/autogalaxy/profiles/mass/abstract/cse.py:197`**:
   `self.radial_grid_from(grid=grid, **kwargs)` drops `xp` (it is a *named* param
   of `_deflections_2d_via_cse_from`, not in `**kwargs`), so `radial_grid_from`
   (`geometry_profiles.py:113` `xp.sqrt(...)`) runs with `xp=np` on a JAX tracer →
   `TracerArrayConversionError` (float64[225]). Threading `xp=xp` here clears it.
3. **Second crash (after fixing #2) — the decomposition itself is not traceable.**
   With `sersic_index` free in search[2], `decompose_convergence_via_cse` runs on
   tracer params via numpy/scipy:
   - `sersic.py:58` `cse_settings_from` → `np.log10((23.0/sersic_constant)**sersic_index)`
     on a scalar tracer → `TracerArrayConversionError` (float64[]).
   - `sersic.py:280` `np.sqrt(self.axis_ratio())`; param-dependent `radii_min/max`.
   - `cse.py:122/126` `np.logspace(np.log10(radii_min), ...)` on tracer bounds.
   - `cse.py:143` `scipy.linalg.lstsq` — cannot trace at all.
   The dark **NFW** decompose (`dark/nfw.py`) has the same shape (`np.max(grid_radii)`,
   `scipy.lstsq`) and would fail identically once reached.

Isothermal traces fine because it deflects **analytically** (`xp.arctan/arctanh`),
never touching CSE — so the CSE JAX port (commit `35e6812a`, 2026-05-26 "port CSE
module to support JAX via xp parameter") was never actually exercised under jit
until this chaining script. This is the first release script to jit a CSE mass
profile with free params.

**Fix locus: PyAutoGalaxy** (`profiles/mass/abstract/cse.py`, `stellar/sersic.py`
incl. `cse_settings_from`, `dark/nfw.py`). Real fix ≈ thread `xp` through
`cse_settings_from` + both `decompose_convergence_via_cse` + `_decompose_convergence_via_cse_from`,
and replace `scipy.linalg.lstsq`/`np.logspace` with `jnp.linalg.lstsq`/`xp.logspace`
so the decomposition is jit-traceable. Validate via the JAX parity scripts in
`autogalaxy_workspace_test` (jit round-trip + `fitness._vmap`), never `test_autogalaxy/`.
Difficulty raised medium → **hard** (numerical path + lstsq-in-trace, affects all
CSE mass profiles under JAX).
