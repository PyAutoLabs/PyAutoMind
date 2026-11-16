Follow-up from the human's seeded glance audit (row 08). Shipped as PyAutoGalaxy#718 (b5c6ec163), merged 2026-11-16 on the human's /prm, on `ci-verdict` GREEN with Heart dev-ship GREEN. The `public-names` check flagged the seven added names, as the narrowing intends, which made this a human merge. Issue PyAutoGalaxy#717.

**Changed:** the seven `latent_*_from` helpers in `autogalaxy/convert.py` are now `*_dict_from`. The `_dict` suffix was the human's choice, so these can't be confused with the existing tuple functions:
- `shear_magnitude_angle_dict_from`
- `axis_ratio_angle_dict_from`
- `multipole_k_m_phi_m_dict_from`
- `scaled_multipole_k_m_phi_m_dict_from`
- `light_multipole_3/4_k_phi_dict_from`
- `light_multipoles_k_phi_dict_from`

The six profile declarations use the new names. The old names stay one release as `DeprecationWarning` aliases.

**Witness:**
- Suite: 1486 passed, also with alias warnings as errors.
- Latent names and values are identical to main for ExternalShear, Sersic and PowerLawMultipole.
- Independent review: CLEAN.

**Found:** `EllipseMultipole` latents raise without `m` (draft `draft/bug/autogalaxy/ellipse_multipole_latent_missing_m.md`).

## Original prompt

# autogalaxy.convert: drop the `latent_` prefix from the parameter-conversion helpers

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: medium
Status: draft
Filed: 2026-11-16
Lane: any

Source: the human's seeded glance audit (seed 20261114, row 08), verdict *would have changed*
on PyAutoGalaxy#656 (`latent-profile-declarations`):

> I would not use latent_ in autogalaxy.convert as this is mixing an autofit concept (latent
> variables) with a galaxy concept (parameter conversions).

PyAutoGalaxy#656 added `latent_shear_from`, `latent_ellipse_from`, `latent_multipole_from`,
`latent_scaled_multipole_from`, `latent_light_multipole_3_from`,
`latent_light_multipole_4_from` and `latent_light_multipoles_from` to `autogalaxy/convert.py`
(lines ~521-575 on main). Rename them to galaxy-language names that say what they convert,
for example `shear_magnitude_angle_from` or `ellipse_axis_ratio_angle_from`. The human picks the
naming scheme in the plan. Update every caller: profile `latent_*` declarations that call them,
`config/notation.yaml` and the workspaces. Keep the autofit-side `latent` declaration API as it is;
only the convert-module names move. Decide whether to keep deprecated aliases for one release.

Witness: `git grep -n "def latent_" autogalaxy/convert.py` returns nothing. The library tests and
workspace smoke pass. Every former call site imports the new names.
