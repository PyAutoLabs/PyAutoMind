## group-list-based-api
- completed: 2026-05-06
- repos: autolens_workspace
- notes: |
    Retroactively logged via 2026-05-06 hygiene scan. Original prompt
    `workspaces/group.md` asked for `autolens_workspace/scripts/group/start_here.py`
    to use the list-based `lens_dict` model composition (multiple main lens
    galaxies treated symmetrically, instead of one main + extras). Verified done:
    `start_here.py:198-200` builds `lens_dict` and iterates `main_lens_centres`
    to populate `lens_0`, `lens_1`, … Three sibling tasks (`group-features`,
    `group-two-main-galaxies`, `group-pixelization-delaunay-fixes`) plus three
    `issued/group*.md` files cover the related rollout. Original issue/PR not
    tracked in this registry.

## Original prompt

Update this __List-Based Model Composition__, to instead be __Dict-Based Model Composition__, updatng the docstring
as appropriate.

Is group/slam.py the same as group/features/pixelization/slam.py? In which case remove the former.

This is a bug in the group subhalo detect start_here.py file:

    lens_0 = af.Model(
        al.Galaxy,
        redshift=source_lp_result.instance.galaxies.lens_0.redshift,
        bulge=source_lp_result.instance.galaxies.lens_0.bulge,
        mass=mass,
        shear=shear,
    )

    lens_dict = {"lens_0": lens_0}

All steps of the slam detection should support multiple main lens galaxies, check back in with the
slam.py file in features/pixelization/slam.py