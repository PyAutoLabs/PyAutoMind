# Witt–Wynne projection of PyAutoLens models for lensed-SN corroboration

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoLens
Themes:
- point-source
- euclid
- guides
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-08-28

## Original request (verbatim)

> Can we implement this in PyAutoLens, can you find the zenodo with example code to
> make this easy?
>
> [Email from Paul Schechter] Please incorporate Witt-Wynne into your Euclid lens
> modeling. I think it would suffice to project your models onto Witt-Wynne space
> without consulting the pixels. Throw out source shape -- centroid suffices. Throw
> out non-isothermality. Throw out the components of shear and ellipticity
> perpendicular to the direction of their sum. Throw out secondary perturbers. It's
> good enough for corroborating quadruply lensed SNae. [...] If you choose, I would
> do the projecting of your models onto Witt-Wynne space. Zero out the coordinate
> system so that you won't be divulging Euclid sources.
>
> ok do it, put it in guides on autolens_workspace for now and do the optional
> thing ourselves if it simplifies source code distribution

## Context

- Paper: Schechter, Lu & Hernández 2026, arXiv:2605.11090 (SN 2025wny / LSST
  alert protocol). NOT arXiv:2510.11356 (that is the cluster-centre paper).
- Code: `isit4or2or1` v1.0, Zenodo DOI 10.5281/zenodo.20086659, CC-BY-4.0,
  single-file C++17 (`SIEP_CLI.v1.0.cpp`, 374 lines). Pure SIEP, **no shear**.
  Input `.in` file (gravlens conventions, PA deg E of N):
  `x_lens y_lens / x_src y_src / e / b / phi / D_ol D_ls (h^-1 Mpc) / z_l z_s`.
  Output: `num_images` then per-image `xpos ypos mag angle lags`.
- Method: Falor & Schechter 2022 (arXiv:2205.06269) asymptotically circular
  quartic; number of real roots = 4/2/1 verdict. Witt 1996 hyperbola, Wynne &
  Schechter 2018 (arXiv:1808.06151), Schechter & Wynne 2019 (arXiv:1901.08517),
  Schechter 2026 Galaxies 14, 20 (arXiv:2604.11908, SIEP + parallel shear).

## Deliverables

1. **Guide** `autolens_workspace/scripts/guides/.../witt_wynne.py` (+ generated
   notebook per the workspace regen convention): load a PyAutoLens result
   (Isothermal/PowerLaw + ExternalShear, any source), project onto Witt–Wynne
   space — mass centre (zeroed / offset-only), Einstein radius (for PowerLaw use
   the Einstein-radius-from-profile, not the normalisation), ellipticity and PA
   from the *sum* of the (e1,e2) and (γ1,γ2) vectors with the perpendicular
   component discarded, converting our e=(1-q)/(1+q) and CCW-from-+x PA to the
   gravlens e=1-q, PA E-of-N conventions; source light centroid; D_ol, D_ls
   from redshifts + cosmology. Write the `.in` file and a CSV row.
2. **Pure-Python/JAX port** of the quartic 4/2/1 solver (positions, mags, lags)
   so no C++ build is needed. Place it in the guide for now (user chose
   "guides on autolens_workspace for now"); note in the plan whether a small
   PyAutoLens utility is the better home for distribution and leave that to
   the plan-approval step.
3. **Validation** in the same guide: on simulated quads (and a Euclid-like
   example) compare the projected SIEP verdict/positions against the full
   PyAutoLens `Tracer` multiple images from the point solver; report the
   agreement level of the shear-folding approximation.
4. Cite the Zenodo DOI and papers; CC-BY-4.0 attribution for any ported code.
