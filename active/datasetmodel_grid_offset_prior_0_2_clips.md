# DatasetModel grid_offset prior ±0.2" clips real multi-band offsets — the same tile/band pairs sit at the edge in prelim and sep1; widen the prior and flag prior-edge rows in astrometric_offsets.csv

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Consequence: glance
Witness: Tile102008165 nir_j re-fitted under the widened prior gives a grid_offset_x whose 3-sigma interval does not touch a prior limit and a CSV row carrying prior_edge=False; today's row under the ±0.2" prior has grid_offset_x_upper_3_sigma exactly 0.2000 and carries prior_edge=True
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17
Issued: 2026-09-17

## Observed

The multi-band registration offsets produced by the SED chain are fitted with a uniform
`DatasetModel.grid_offset` prior of **±0.2"** (two VIS pixels at 0.1"/pixel), set in
`scripts/lens_model_waveband.py:492-497`. In two independent deliveries of the same lenses the same
tile/band pairs land **on** that limit.

`euclid_dr1` sep1 bundle, `inspect/dr1_sep1/astrometric_offsets.csv` (52 rows), rows with
|offset| > 0.17":

| lens | band | grid_offset_y | grid_offset_x | 3-sigma bounds |
|---|---|---:|---:|---|
| Tile102008165RA0109661927007DECNEG0642904268129 | nir_h | 0.1787 | 0.1909 | y [0.1537, 0.1788], x [0.1908, 0.1910] |
| Tile102008165RA0109661927007DECNEG0642904268129 | nir_j | 0.1571 | 0.1906 | y [0.0764, 0.1993], x [0.1244, **0.2000**] |
| Tile102008219RA0727857418392DECNEG0644388277074 | decam_g | 0.1938 | -0.1234 | y [0.1469, **0.2000**], x [-0.1976, -0.0122] |
| Tile102008475RA0039777627054DECNEG0637715426503 | decam_i | 0.1773 | -0.1855 | y [0.1357, 0.1996], x [**-0.1999**, -0.1359] |

`euclid_dr1_prelim` bundle,
`/mnt/c/Users/Jammy/Science/euclid_dr1_prelim/inspect/dr1_prelim_grade_ab_342629/astrometric_offsets.csv`,
same threshold:

| lens | band | grid_offset_y | grid_offset_x | 3-sigma bounds |
|---|---|---:|---:|---|
| Tile102007903RA0668831429074DECNEG0648901814905 | decam_r | -0.1848 | -0.1802 | y [-0.1999, -0.1238], x [-0.1997, -0.1141] |
| Tile102008165RA0109664211519DECNEG0642902327064 | nir_h | 0.1835 | 0.1836 | y [0.1578, 0.1942], x [0.1821, 0.1988] |
| Tile102008165RA0109664211519DECNEG0642902327064 | nir_j | 0.1728 | 0.1908 | y [0.0700, **0.2000**], x [0.1245, **0.2000**] |
| Tile102008219RA0727851454839DECNEG0644382776514 | decam_g | 0.1966 | -0.1735 | y [0.1713, **0.2000**], x [-0.1992, -0.0861] |

Several 3-sigma bounds are exactly **0.2000** / **-0.1999**: the posterior is **truncated by the
prior**, not merely close to it.

## Why this is the prior, not a fluke

Cross-matched through the tile mapping (the sep1 delivery renamed seven of the ten tiles), **the same
two tile/band pairs sit at the same edge in both deliveries**: `Tile102008165…` nir_h and nir_j
(x ≈ +0.19 in both) and `Tile102008219…` decam_g (y ≈ +0.19 in both). These are not the same cut-outs
— the sep1 cut-out centres moved by **0.79"** (Tile102008165) and **2.19"** (Tile102008219), the
segmentation is a different delivery, and the mask radii changed — yet the fit lands on the same
limit. A limit that survives a change of cut-out and segmentation is a limit that is clipping a real
offset larger than 0.2".

The pixel scales say the same thing: ±0.2" is **two VIS pixels**, but it is **smaller than one NISP
pixel (0.3")** and **smaller than one DECam pixel (~0.26")**. A genuine one-pixel registration error
in those instruments cannot be represented by the model at all — and NISP and DECam bands are exactly
where the edge rows appear.

## Ask

1. **Widen the uniform `grid_offset` prior** at `scripts/lens_model_waveband.py:492-497`. Proposal:
   **±0.5"**, i.e. comfortably more than one NISP pixel; or per-instrument limits derived from each
   band's pixel scale, if that is cleaner than one global number. The point is that the prior must be
   able to represent a one-pixel offset in the coarsest instrument.
2. **Re-check the producer's tests under the widened prior** — the header pin fixture and the
   known-answer test in the `astrometric_offsets` producer's tests both encode the current limits;
   they should assert the new prior, not the old numbers, and should keep asserting that the CSV
   columns and row identity are unchanged.
3. **Add a prior-edge flag to `astrometric_offsets.csv`** — a `prior_edge` boolean (or
   `at_prior_edge_y` / `at_prior_edge_x`) computed from **the prior limits held on the result's own
   model**, never a hard-coded 0.2. A row whose 3-sigma interval reaches a limit is flagged. Document
   the column in `catalogue/README.md`, where the other columns are described, and say plainly that a
   flagged row is a QA signal rather than a measurement.
4. **One-line drift to fold in:** `catalogue/scripts/catalogue_util.py` line 5 says "The six catalogue
   producers" — there are now **eight** (astrometric_offsets, deblending, lens_mass, lens_mass_maps,
   lens_sersic, magnitudes, multi_wavelength, source_sersic). Fix the docstring in the same change.

## Witness

Re-fit `Tile102008165…` `nir_j` under the widened prior: `grid_offset_x` and its 3-sigma interval no
longer touch a prior limit, and the CSV row carries `prior_edge=False`. The same tile/band row built
from today's ±0.2" fit carries `prior_edge=True` (its `grid_offset_x_upper_3_sigma` is exactly
0.2000).

## Evidence

- `/mnt/c/Users/Jammy/Science/euclid_dr1/wiki/project/2026-09-17-sed-chain-sep1.md`, sections
  "`astrometric_offsets.csv`" and "Same edge in both deliveries".
- The two bundle CSVs named above.
- Prior: `euclid_strong_lens_modeling_pipeline/scripts/lens_model_waveband.py:492-497`.

<!-- formalised by the Intake (Conception) Agent on 2026-09-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/7bff8610-4b84-413a-a994-d72484c4c14c/scratchpad/intake_2b.md -->
