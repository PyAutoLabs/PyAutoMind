# Weak-lensing `simple` example: rescale to a genuine cluster-scale lens

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Improve the `scripts/weak/` `simple` example so it depicts a *genuine* weak-lensing
system rather than one whose signal is really strong/intermediate lensing.

## Problem

The current `simple` example uses a galaxy-scale Isothermal lens (`einstein_radius=1.6"`)
and draws 200 background galaxies uniformly in a 3.0"-half-width square. Because that box
reaches inward to `r ~ 0.14"`, many galaxies sit at or inside the Einstein radius, where the
Isothermal shear `|gamma| = theta_E / (2r)` is order 0.2-1. The example's clean "31-sigma
detection" therefore comes from near-Einstein-radius galaxies in the strong/intermediate
regime, not from genuinely weak shear. Measured empirically: median per-galaxy `|gamma|/sigma`
~ 1.1; restricting to a true weak annulus (5-20") at the same `theta_E` collapses the same
200-galaxy catalogue to ~3 sigma. The example does not *look* like the weak lensing it is
teaching.

## Change

Rescale the `simple` scenario to the mass scale where weak lensing is actually the tool of
choice — a cluster — and place the background galaxies where weak measurements are actually
made (outside the strong-lensing core):

- **Lens:** cluster-scale Isothermal, `einstein_radius=25.0"` (very massive cluster,
  sigma_v ~ 1200-1400 km/s), `axis_ratio=0.8`, `angle=45`, `centre=(0,0)`, `z_l=0.5`,
  `z_s=1.0`. Keep Isothermal (the analytic `gamma = theta_E/2r` keeps the tutorial's
  `chi^2 ~ 2N` reasoning clean; NFW is the real-data example's job).
- **Sources:** 1500 background galaxies drawn uniformly-in-area in a **50"-200" annulus**
  (inner radius ~2 theta_E, safely into the weak regime; ~45 gal/arcmin^2 deep-survey
  density). Build an explicit `al.Grid2DIrregular` and use `simulator.via_tracer_from`
  (the docstring already recommends this for core exclusion).
- **Noise:** `noise_sigma=0.25` (typical shape noise).
- **Priors (`modeling.py`):** the default Isothermal priors are galaxy-scale (Einstein
  radius Uniform 0-8", centre Gaussian sigma=0.1") and would exclude a 25" lens, so widen
  them (Einstein radius Uniform 0-60", centre Gaussian sigma=20") with prose explaining that
  priors track the system's scale.
- Sync the hand-picked truth in `fit.py` and `likelihood_function.py` (`einstein_radius=25.0`,
  `axis_ratio=0.8`), the `2N` sanity number (400 -> 3000), and all dataset-description prose
  (200 -> 1500, 3.0" square -> 50-200" annulus, 0.3 -> 0.25, "galaxy-scale" -> "cluster-scale").

Leave `scripts/features/strong_lensing/` unchanged — that joint strong+weak example is
deliberately galaxy-scale.

## Files

- `scripts/weak/simulator.py`
- `scripts/weak/modeling.py`
- `scripts/weak/fit.py`
- `scripts/weak/likelihood_function.py`

(`notebooks/weak/*.ipynb` and `markdown/weak/*.md` are generated from the scripts by
PyAutoBuild at build/release time.)

## Acceptance

The new scenario is genuinely weak (every galaxy outside the core; median `|gamma|` below the
per-galaxy shape noise) yet still recovers its inputs and runs in minutes. Verified against
autolens 2026.7.15.1 in a clean venv:

- `simulator.py` -> 1500-galaxy 50-200" annulus catalogue, detection S/N ~ 16 sigma,
  median `|gamma|=0.085`, max `0.27`.
- `fit.py` / `likelihood_function.py` -> `chi^2 = 2974` for 3000 dof; by-hand ==
  `FitWeak` == `AnalysisWeak` log-likelihood.
- `modeling.py` (Nautilus, ~2 min) -> `einstein_radius` recovered `24.3"` (1-sigma
  22.9-25.8; truth 25.0 within 0.5 sigma); ellipticity and centre within ~1 sigma.

<!-- filed 2026-07-15 as a follow-up to the completed weak series (weak-modeling,
weak-real-data, weak-dataset-from-json); design values verified end-to-end before filing. -->
