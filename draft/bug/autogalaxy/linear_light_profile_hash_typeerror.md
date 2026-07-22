# `__hash__ method should return an integer` in linear_light_profile_intensity_dict (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked 2026-04-27; still parked after the 2026-07-21 census.

`autolens_workspace_test/scripts/database/scrape/general` fails: PyAutoGalaxy
`abstract_fit.linear_light_profile_intensity_dict` raises `TypeError: __hash__ method should return
an integer` during `subplot_fit_imaging` after the search completes — a light-profile object's
`__hash__` returns a non-int. Surfaced once the `dataset_label="build"` path fix let the script
progress past `Imaging.from_fits`.

Fix the offending `__hash__` in the light-profile class (must return int), add a unit test that hashes
the profile, then remove the NEEDS_FIX marker from autolens_workspace_test/config/build/no_run.yaml.
