## subhalo-refine-source-fix
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/133
- repos: autolens_workspace
- notes: |
    Cluster F of the recent release-prep triage. scripts/group/features/
    advanced/subhalo/detect/start_here.py crashed with `NameError: name
    'source' is not defined` at line 634 of `subhalo_refine`. Fallout from
    PR #117 ("Cluster F triage", 2026-05-02): PR #117 removed the
    redundant `"source": ...` key from five lens_dict literals (they
    collided with the explicit `source=source` kwarg on `af.Collection`).
    Four functions had a local `source = ...` assignment already, so the
    explicit kwarg remained resolvable. `subhalo_refine` was the
    exception — PR #117 dropped `"source": subhalo_grid_search_result.
    model.galaxies.source` from its lens_dict without lifting that
    expression into a standalone assignment. Fix: add the missing
    `source = subhalo_grid_search_result.model.galaxies.source` line
    before the lens_dict literal. Restores exactly the value PR #117
    dropped; matches the standalone-assignment style every other
    subhalo_* function uses; preserves the SLaM-like pipeline
    (grid-search posterior source flows into refine search).
    User's original suggestion (`source=source` → `source=source_lp`,
    based on Python's NameError "Did you mean: 'source_lp'?" hint)
    would have type-errored at fit time — `source_lp` is a function in
    this file, not a Galaxy. Python's NameError suggestion is lexical
    proximity, not type-correct. Verified locally:
    `subhalo[3]_[single_plane_refine]` (the previously-failing phase)
    now completes successfully.
