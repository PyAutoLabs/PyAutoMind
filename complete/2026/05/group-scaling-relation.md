## group-scaling-relation
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/167
- completed: 2026-05-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/173
- notes: Two-stage task. Stage 1 added fit.py + likelihood_function.py to imaging/features/scaling_relation/; Stage 2 same for group/features/scaling_relation/. Both directories already had comprehensive modeling.py + simulator.py; this PR padded them out with the no-search demo + likelihood walkthrough. All 4 scripts assert per-galaxy (or per-tier) deflection sums match the tracer total — scaling-tier galaxies' einstein radii come from `0.3 * luminosity^1.0 = 0.135` (truth). Conflict override on autolens_workspace — ran in parallel with interferometer-multi-gaussian-expansion + interferometer-shapelets (disjoint feature dirs). Dataset gotcha: Explore agent initially reported group dataset NOT committed but it was already tracked on main (10 files); simulator regenerated noise differently on fresh seed which showed up as `M` entries in diff. .gitignore got hygiene additions: !dataset/imaging/extra_and_scaling_galaxies/** and !dataset/group/scaling_relation/** (both datasets were already tracked so allow-list was invisibly missing). Group simulator has only one main lens — lens_dict has single entry; pattern generalises naturally. No smoke entries added (per "small curated subset" memory).

## Original prompt

The imaging `features/scaling_relation` example needs improving and padding out before adapting to group.

Once the imaging version is more complete, adapt it to the group context in `scripts/group/features/scaling_relation/`.

For group lenses, scaling relations are especially important: they allow many extra galaxies to share
a luminosity-to-mass relation (einstein_radius = scaling_factor * luminosity^scaling_relation),
keeping the model dimensionality low even as galaxy count grows. The group/slam.py already implements
scaling galaxies — the feature script should document this API in a standalone, beginner-friendly way.
