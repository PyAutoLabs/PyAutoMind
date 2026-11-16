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
