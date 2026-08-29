## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510 (closed 2026-08-28)
- completed: 2026-08-28
- workspace-pr: autolens_workspace#511 (merged 7c0d9efb -> main; branch head e77f25ec)
- origin: Paul Schechter's request (email 2026-08) to project Euclid PyAutoLens models onto Witt–Wynne space so the LSST-broker code `isit4or2or1` (Schechter, Lu & Hernández 2026, arXiv:2605.11090; Zenodo DOI 10.5281/zenodo.20086659, CC-BY-4.0) can corroborate whether a transient near a known quad is 4/2/1-imaged. Note the email's arXiv link (2510.11356) is the cluster-centre Witt-hyperbola paper, not this one.
- what shipped: `scripts/guides/misc/witt_wynne.py` + notebook, new `guides/misc/` folder (README/__init__), `smoke_tests.txt` entry, catalogue regen (`llms-full.txt`, `workspace_index.json`). Workspace-only; no library source touched. All four prompt deliverables shipped.
- solver port: pure numpy, mirrors `SIEP_CLI.v1.0.cpp` (quartic from Witt hyperbola ∩ unit circle, Falor & Schechter 2022; real-root count = verdict; magnification; time lags in days). Regression vs both shipped `2025wny_*.out` files: max |Δ| 3.4e-4 (their printed precision). The C++ was compiled and run on our exported `.in` → identical positions/mags, so the writer round-trips.
- projection: `witt_wynne_from_tracer` matches the model's tangential caustic (b from `LensCalc.einstein_radius_from`, PA from caustic long axis, e by bounded least-squares fit of both SIEP astroid semi-axes — single-axis closed forms disagree, e.g. 0.0995/0.1102/0.1932 at q=0.70); `witt_wynne_vector_sum` implements Schechter's literal ellipticity+shear sum for comparison.
- validation (5 simulated SIE+shear systems vs `PointSolver` + `time_delays_from`, incl. source 2% outside the caustic): verdict agreement 5/5 for both projections; positions 0.07–0.16"; lags 5–13% of span; caustic-matching only clearly better at γ=0.1 (1.8 vs 3.6 d). Runtime 5.8 s.
- conventions worth remembering (documented in the guide's `__Conventions__`): (1) `PA_isit = θ_ccw_from_+x + 90` mod 180 — Keeton's registered x-axis points West; the `90 − θ` form mirrors every image and was only caught because validation compares positions, not counts. (2) Shear enters the vector sum with a minus sign: mass ellipticity at θ elongates the caustic along θ, shear at θ_γ elongates it at θ_γ+90. (3) The C++ hardcodes h=0.7 in `TIMECONSTANT` while taking h⁻¹ Mpc distances; the port exposes `h` and passes the tracer's own so lag comparisons are like-for-like. (4) The Zenodo v1.0 code is pure SIEP — no shear parameter; the SIEP+parallel-shear version (Schechter 2026, arXiv:2604.11908) is not in the release. (5) Source exactly on the potential major axis is a quartic double root (indeterminate y) in the C++ and the port alike — documented, not guarded.
- smoke trap: `PYAUTO_SMALL_DATASETS=1` short-circuits `PointSolver.solve` to a fixed pair of positions (agreement drops to 2/5); the guide asserts the 5/5 verdict with an error naming `ENV: full_datasets`, so a runner ignoring the ENV declaration fails loudly instead of passing vacuously.
- CI at merge: 3 `pull_request` runs for e77f25ec (Smoke Tests 3.12+3.13, Navigator Check ×3, Script Size Guard) all success; `mergeStateStatus CLEAN`.
- heart-ack: shipped under human authorisation ("i authorise do a prm") with Heart RED for unrelated reasons, verbatim: "release validation FAILED (stage integrate)"; "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)"; "manifest drift: session-start hooks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml".
- follow-up: `draft/test/autolens_workspace/witt_wynne_tests_and_review.md` — broader validation grid (slopes, q, γ, misalignment, fold/cusp, Euclid redshifts), the on-axis degeneracy, per-case C++ round-trip, and a human review of the design conventions + example prose before offering the exporter to Schechter.

## Original prompt

# Witt–Wynne projection of PyAutoLens models for lensed-SN corroboration

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- point-source
- euclid
- guides
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Filed: 2026-08-28
Issued: 2026-08-28

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
