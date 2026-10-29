## mass-integral-scalar-radius
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/673
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/674
- summary: `MassProfile.mass_integral` wrapped the Python float `scipy.integrate.quad` feeds it as a
  0-d `aa.ArrayIrregular`, which most `convergence_func` implementations (written for 1D radius
  arrays) mis-handle. ~30 of the 62 constructible `ag.mp` classes failed through
  `mass_angular_within_circle_from` — NFW family TypeError (length-1 complex64 array), gNFW family
  IndexError (`.shape[0]`), truncated NFW / Sersic / Exponential / DevVaucouleurs / cored
  power-law & isothermal / dPIE AttributeError (autoarray copying a bare float) — and with it the
  Einstein radius. One general fix in the integrand: a length-1 radius array in, a float out.
  No `convergence_func` body changed; no API change.
- tests: NFWSph(kappa_s=0.2, scale_radius=5.0) against the analytic projected mass
  4π κ_s r_s² h(R/r_s) (Bartelmann 1996) at R = 1 and R = 8 and against the #672 grid oracle;
  gNFWSph(inner_slope=1) against the closed form; parametrised regression over NFWSph,
  NFWTruncatedSph, SersicSph, PowerLawCoreSph, IsothermalCoreSph, dPIEMassSph against the grid
  oracle (agreement ~1e-6). Full suite 1399 passed / 7 skipped; CI green (3.12, 3.13, nojax, docs).
- traps: `aa.ArrayIrregular(0.5).array` is a bare Python float, not a 0-d ndarray — any
  `ArrayIrregular` arithmetic on it raises in autoarray's `__copy__`. `coord_func_g` promotes a
  bare scalar to complex64 (float32 output) — avoid scalar inputs there. The gNFW grid oracle
  takes >2 min (per-point quad in `convergence_2d_from`); test it analytically instead.
- notes: Heart board unreachable from the web container; readiness read from a read-only
  PyAutoHeart clone (STALE, environment reasons only, no RED/YELLOW); freeze clear at merge.
  Bug Agent: severity high, runtime-error, fix locus library source. PyAutoGalaxy claim
  coordinated with lenstwin-p0-twins-core (its #672 leg already merged). Consequence: judge,
  human /prm.

## Original prompt

# `mass_angular_within_circle_from` raises on NFW (and ~30 other profiles): the radial integrand feeds a 0-d radius to `convergence_func`

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- mass-profiles
- dark-matter
- regression
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Consequence: judge
Witness: `ag.mp.NFWSph(kappa_s=0.2, scale_radius=5.0).mass_angular_within_circle_from(radius=1.0)` returns 2.33220 (= 4 pi kappa_s r_s^2 h(R/r_s), Bartelmann 1996) instead of raising; every `ag.mp` profile with a `convergence_func` integrates without error and agrees with `ag.mass_angular_within_circle_via_grid_from`.
Review-minutes: 5
Unattended: ready
Filed: 2026-10-28
Issued: 2026-10-28

Found 2026-10-28 while writing tests for PyAutoGalaxy#671 / PR #672.

`NFWSph.mass_angular_within_circle_from(radius)` raises
`TypeError: only 0-dimensional arrays can be converted to Python scalars` on `main`.
`@PyAutoGalaxy/autogalaxy/profiles/mass/abstract/abstract.py` `AbstractMassProfile.mass_integral`
(around line 229) calls `self.convergence_func(grid_radius=aa.ArrayIrregular(x))` with the Python
float `scipy.integrate.quad` feeds it. `aa.ArrayIrregular(x).array` is then a bare 0-d float, and
most `convergence_func` implementations are written for the 1D radius arrays `convergence_2d_from`
passes, so the 0-d radius breaks them in four distinct ways (survey of every `ag.mp` class, 2026-10-28):

- NFW family (`NFW`, `NFWSph`, `NFWMCR*`, `NFWVirialMassConcSph`;
  `@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw.py`): `coord_func_g` in
  `@PyAutoGalaxy/autogalaxy/profiles/mass/dark/abstract.py` promotes a scalar to a length-1
  `complex64` array, so the integrand returns a length-1 (float32!) array that `quad` rejects.
- gNFW family (`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/gnfw.py`): `grid_radius.shape[0]` on a
  0-d array raises `IndexError`.
- `NFWTruncated*` (`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/nfw_truncated.py`), `Sersic*`,
  `Exponential*`, `DevVaucouleurs*`, `SersicGradient*`, `IsothermalCore*`, `PowerLawCore*`,
  `dPIE*`: arithmetic on the `ArrayIrregular` copies its `_array`, which is a bare `float`
  (`AttributeError: 'float' object has no attribute 'copy'`).
- `Isothermal`, `PowerLaw`, `Gaussian`, `Chameleon`, `SersicCore`, `cNFW`, Kaplinghat/Yang SIDM,
  the sheets and `PowerLawMultipole` already return a scalar and work.

Because `average_convergence_of_1_radius` and `density_between_circular_annuli` sit on top of
`mass_angular_within_circle_from`, the Einstein radius of every affected profile is broken too.

Fix: the general fix is in `mass_integral`, not in 30 `convergence_func` bodies. Feed the
integrand a length-1 radius array (the shape every `convergence_func` is written for) and coerce the
result with `float(np.asarray(...).reshape(-1)[0])` before returning it to `quad`. This also removes
the NFW float32 precision loss on this path. Leave each `convergence_func` alone.

Tests (in `@PyAutoGalaxy/test_autogalaxy/profiles/mass/`): a regression test comparing
`NFWSph(kappa_s=0.2, scale_radius=5.0).mass_angular_within_circle_from(radius=1.0)` to the analytic
NFW projected-mass closed form `4 pi kappa_s r_s^2 h(x)`, `x = R / r_s`,
`h(x) = ln(x/2) + arccosh(1/x)/sqrt(1-x^2)` for `x < 1` (`arccos(1/x)/sqrt(x^2-1)` for `x > 1`),
inside and outside the scale radius; a cross-check against the grid oracle
`ag.mass_angular_within_circle_via_grid_from` (PR #672, merged); and a parametrised regression
over one representative of each formerly failing family (gNFWSph with inner_slope=1, NFWTruncatedSph,
SersicSph, PowerLawCoreSph, IsothermalCoreSph, dPIEMassSph) against the grid oracle. Run the full
PyAutoGalaxy suite.

Original request (verbatim):

> In PyAutoGalaxy, `NFWSph.mass_angular_within_circle_from(radius)` raises `TypeError: only 0-dimensional arrays can be converted to Python scalars` on `main` (found 2026-10-28 while writing tests for PyAutoLabs/PyAutoGalaxy#671 / PR #672). The cause: `AbstractMassProfile.mass_integral` (autogalaxy/profiles/mass/abstract/abstract.py, around line 229) calls `self.convergence_func(grid_radius=aa.ArrayIrregular(x))`, and the NFW `convergence_func` (autogalaxy/profiles/mass/dark/nfw.py and/or the gNFW abstract it inherits from) returns a length-1 array rather than a float, which `scipy.integrate.quad` rejects. `Isothermal` and the Gaussian profiles work through the same path.
>
> Task: make the NFW family's `convergence_func` return a scalar for a scalar radius (or make `mass_integral` coerce with `float(np.asarray(...).reshape(-1)[0])` if that is the more general fix; check which other `convergence_func` implementations in autogalaxy/profiles/mass/ have the same shape issue, e.g. with `grep -rn "def convergence_func" autogalaxy/profiles/mass/`), add a regression test in test_autogalaxy/profiles/mass/ comparing `NFWSph(kappa_s=0.2, scale_radius=5.0).mass_angular_within_circle_from(radius=1.0)` to the analytic NFW projected-mass closed form (the new `ag.mass_angular_within_circle_via_grid_from` from PR #672 can serve as a second oracle once merged), and run the full suite. File it as a Mind bug prompt (`draft/bug/autogalaxy/`) and route through /start_dev if following the PyAutoLabs workflow.
