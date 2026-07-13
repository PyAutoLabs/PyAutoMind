# Shared-state likelihood API for multi-dataset examples (shifted shared Delaunay mesh)

Extend the datacube shared-state / `shared_preloads` machinery (PyAutoFit
`shared_state_from` + `shared=` kwarg; PyAutoArray `Preloads*`; PyAutoLens
consumer) to the **imaging multi-dataset** examples in
`autolens_workspace/scripts/multi/`, adding docstring'd sections to the existing
examples showing the API.

**Scope reality check (audited 2026-07-10):** only the interferometer consumer
exists today — there is no `PreloadsImaging` and `AnalysisImaging` has no
`shared_preloads` / `shared_state_from`. So this is a **library + workspace**
task (imaging consumer in PyAutoLens/PyAutoArray first, workspace example
sections after), not a docs-only task. Note the sharing semantics differ from
the datacube: with per-exposure PSFs and pixel shifts, the curvature matrix
`F` and even the mapping matrix `L` are NOT shareable — what is shared is the
source-plane **mesh/mapper geometry** (one Delaunay mesh, shifted per dataset).

## Original request (verbatim)

> Ok, I now want to use the same shared likelihood API and general tools to use this functionality on other multi
> datasets (see autolens_workspace/scritps/multi), where basically we add to the existing examples docstring'd sections
> showing the API for doing this, here are the use cases I envision:
>
> - When we are fitting different exposures at the same wavelength, with pixel offsets of the same lens, the shared likelihood should be
> used to set up one Delaunay mesh which is shifted and shared across all datasets. The point is we are reconstructing
> one source for all exposures with just a shift. The shift is a optional free parameter, but default assume its
> known (see below), we may need to put these shifts in simulator.py (but maybe have them all 0 by default.). Given that
> their PSFs are different I would guess this means we cant share the blurred mappign matrix, and even the mapping matrix is different due to shifts.
>
> - When we are fitting different exposures at different wavelengths of the same lens, we still wantt he same Delaunay mesh
> with shifts, but we dont want the reconstruction to be the same for each dataset due to color differences.
>
> - I guess also do this for the imaging_and_interferomer.py example. Heres some info on how offsets are provided by our actual data reduction, its probably more detail than you need: Loading per-exposure pixel-shift (registration) information from PyAutoReduce
> frame products, for multi-exposure modeling examples.
>
> A reduction run with `TargetSpec(frame_products=True)` writes
> `<output>/<name>/frames/manifest.json` plus one directory per exposure
> (`frames/<frame_id>/data.fits`, `noise_map.fits`, `psf.fits`, ...). All shift
> information lives in the manifest's per-frame `registration` block and in each
> frame's `target_pixel`:
>
>     import json
>     from astropy.io import fits
>     from astropy.wcs import WCS
>
>     manifest = json.load(open(f"{dataset_path}/frames/manifest.json"))
>     for entry in manifest["frames"]:
>         reg = entry["registration"]
>         # target_pixel: the target's exact (x, y) in THIS frame's cutout —
>         # the per-frame registration anchor. Differences of target_pixel
>         # between frames ARE the relative pixel shifts.
>         x_t, y_t = entry["target_pixel"]
>
> HST / JWST semantics:
> - Each frame's data.fits header carries a (SIP-only) WCS; frame-to-frame
>   mapping is WCS_j^-1 ∘ WCS_i, and `target_pixel` was computed through the
>   FULL distortion model (more accurate than the shipped header WCS by
>   ~0.1 px).
> - `reg["residual_dy_px"] / ["residual_dx_px"]` are MEASURED relative
>   registration errors vs `reg["reference"]` (phase correlation after WCS
>   resampling) — i.e. how wrong "shifts are perfectly known" is. Honor
>   `reg["residual_reliable"]`: false means the number is a mask-geometry
>   artifact (heavily off-chip frame), not a shift. Manifest-level
>   `max_registration_residual_px` may be null (= unmeasured, no clean pair).
> - Do NOT use header RMS_RA/RMS_DEC — that is the group's ABSOLUTE catalog
>   alignment, not the relative registration.
>
> Keck (NIRC2) semantics:
> - No trustworthy WCS exists. `reg["offset_dy_px"] / ["offset_dx_px"]` are the
>   measured phase-correlation offsets of this frame vs the reference frame,
>   in native pixels — these ARE the shifts (exact by construction at the
>   correlation's sub-pixel accuracy). Frames are already target-centred via
>   these offsets, so `target_pixel` is ~identical across frames; residual
>   differences reflect the inversion accuracy (~0.8 px band on B1938).
>
> Recommended modeling treatment (the reduction's documented stance): treat
> shifts as KNOWN by default — apply the relative shift from target_pixel
> differences (or the WCS pair) as a fixed per-frame offset of the image-plane
> grid. For precision applications, add free per-frame (dy, dx) nuisance
> parameters with Gaussian priors of width = the recorded residuals (HST/JWST:
> residual_dy/dx_px, floor ~0.1-0.3 px; this also absorbs the SIP-serialization
> term). The choice is model-time, per dataset — the manifest carries what both
> options need.
>
> Two notes for your modeling-code design: data.fits+noise_map.fits per frame are already ts-loadable — bad/CR pixels are masked-by-noise at 10⁸, data zeroed), and units are e-/sfor HST/Keck but MJy/sr for JWST (check manifest["data_units"] rather than assuming). When you file the modeling prompt, I'd suggest it also consume entry["psf"]["method"] so the fit records which PSF tier each frame carried — that provenance matters for the AO case especially.

## Use cases → target example scripts

| Use case | Target under `autolens_workspace/scripts/multi/features/` | Sharing semantics |
|---|---|---|
| Same wavelength, per-exposure pixel offsets | `same_wavelength/` (+ `dataset_offsets/` for the shift concept; shifts may need adding to `simulator.py`, default 0) | One Delaunay mesh shared + shifted per dataset; **one source reconstruction** for all exposures |
| Different wavelengths | `wavelength_dependence/` | Same shared shifted mesh, but **per-dataset reconstructions** (colour differences) |
| Imaging + interferometer | `imaging_and_interferometer/` | Same idea across the two dataset types |

## Key design constraints

- Shifts are **known by default** (fixed per-frame image-plane grid offsets from
  PyAutoReduce `target_pixel` differences / WCS pairs); optionally free
  per-frame `(dy, dx)` nuisance parameters with Gaussian priors of width = the
  recorded registration residuals (floor ~0.1–0.3 px HST/JWST).
- Per-exposure PSFs differ → blurred mapping matrix not shareable; shifts →
  mapping matrix itself differs per dataset. The shareable object is the
  source-plane mesh (Delaunay geometry), not `F`/`L` as in the datacube case.
- Wavelength case: shared mesh geometry but independent per-dataset
  reconstructions.
- Follow the existing consumer pattern: `AnalysisInterferometer.shared_preloads`
  + `shared_state_from` + `aa.PreloadsInterferometer`; add the imaging siblings.
- Frame products loading notes: bad/CR pixels are masked-by-noise at 1e8 (data
  zeroed) so per-frame `data.fits`/`noise_map.fits` load directly; check
  `manifest["data_units"]` (e-/s HST/Keck vs MJy/sr JWST) rather than assuming;
  record `entry["psf"]["method"]` per frame for PSF-tier provenance (matters
  most for the AO case).

## Cross-references

- `issued/datacube_shared_state_consumer.md` + `issued/analysis_shared_state_cross_factor.md` — the shipped mechanism + interferometer consumer this generalises (epic archived at `z_features/complete/analysis_shared_state.md`).
- PyAutoLens#565 / PyAutoFit#1307 (both closed) — design history.
- `autolens_workspace_test/scripts/jax_likelihood_functions/datacube/shared_preloads.py` — the parity-test pattern to mirror for imaging.
- PyAutoReduce frame products: `<output>/<name>/frames/manifest.json` (registration block semantics above).
