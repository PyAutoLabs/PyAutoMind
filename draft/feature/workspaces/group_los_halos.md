# The imaging `features/advanced/los_halos` example needs improving and padding out before

Type: feature
Target: workspaces
Themes:
- cluster
- notebooks
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: `scripts/group/features/advanced/los_halos/` runs to completion under the smoke profile with at least one LOS halo at a redshift distinct from the group redshift, and its `model.info` places that halo on its own plane rather than the group plane — the distinction the prose must teach, made checkable.
Review-minutes: 3
Unattended: ready
Filed: 2026-04-27 (backfilled from git)

The imaging `features/advanced/los_halos` example needs improving and padding out before adapting to group.

Once the imaging version is more complete, adapt it to the group context in
`scripts/group/features/advanced/los_halos/`.

For group lenses, line-of-sight halos at different redshifts from the main group introduce additional
deflections via multi-plane lensing. The distinction between "extra galaxies at the group redshift"
(which are already modeled) and "LOS halos at other redshifts" must be clearly explained.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
