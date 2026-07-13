## group-double-einstein-ring
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/156
- completed: 2026-05-16
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/157
- summary: |
    Padded out the imaging double Einstein ring example with new fit.py
    and likelihood_function.py (parametric MGE source, no pixelization);
    refreshed modeling.py with an upfront "use chaining for real fits"
    callout and a fixed-Planck18 cosmology with a commented Om0-free
    snippet. Mirrored the imaging set into a new scripts/group/features/
    advanced/double_einstein_ring/ folder using lens_dict for two main
    lens galaxies (simulator + fit + modeling + likelihood_function +
    chaining + slam + README). Committed datasets for both. slam.py's
    pixelized stages couldn't be validated under TEST_MODE=2 due to a
    pre-existing autoarray limitation that also affects imaging slam.py;
    structurally mirrors imaging so should work in production. Inner
    dataset/.gitignore required `git add -f` for the new datasets,
    matching existing convention. Tracker z_features/group_lensing_workspace.md
    now has 4 sub-prompts remaining (los_halos, mass_stellar_dark,
    scaling_relation, subhalo_sensitivity).

## Original prompt

The imaging `features/advanced/double_einstein_ring` example needs improving and padding out before adapting to group.

Once the imaging version is more complete, adapt it to the group context in
`scripts/group/features/advanced/double_einstein_ring/`.

A double Einstein ring in a group context involves two source galaxies at different redshifts being
lensed by the group. The multi-plane ray-tracing must account for all group galaxy masses at the lens
redshift plus the intermediate source galaxy acting as a secondary lens for the more distant source.
