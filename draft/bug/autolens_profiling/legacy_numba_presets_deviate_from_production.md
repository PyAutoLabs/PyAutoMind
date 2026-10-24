# Legacy numba "production" presets in autolens_profiling deviate from the real production pipeline

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: the legacy (non-standard-size) numba production presets either build the same cell as `production_standard_data` (and their pins are re-recorded), or are retired with their pins, and the decision is recorded in the profiling wiki
Review-minutes: 15
Unattended: never
Epic: likelihood-lifecycle
Filed: 2026-10-24

Found while building autolens_profiling#457 (phase 2a PR A), checked against subhalo_validation@122079f and the euclid pipeline@9b1bc4c:
1. The HST_RECT_ADAPT and EUCLID_RECT_ADAPT cells build `RectangularBilinearAdaptDensity` (`rect_mesh_classes(cli)[0]`). Production source_pix[2] uses `RectangularBilinearAdaptImage` with free `weight_power` and `weight_floor` (`rectangular_adapt.py:74-96`).
2. The adapt image is noise-free lensed-source flux, not production's subtracted S/N map (`adapt_images.py:138`), and it is capped at 3 before the S/N > 3 over-sampling cut. So on hst, jwst and ao the cut never fires and the sub-size is 2 everywhere; production cuts on the uncapped S/N (`imaging.py:213-255`).

By human ruling (2026-10-24), these presets were kept byte-unchanged for non-standard runs and their pins, while `--standard-size` cells use the real production construction (`_production_config.production_standard_data`). Decide whether to retire the legacy presets or re-pin them to the production construction, and which existing rows and campaign notes this invalidates.
