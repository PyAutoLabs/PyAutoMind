## critical-curves-linewidth
- completed: 2026-05-16
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/319
- merge-commit: 41465a35
- summary: |
    User-reported visual tweak — critical curves and caustics overlays
    were too thick to inspect underlying lens-model results. Reduced the
    hardcoded matplotlib linewidth from 2 to 1 in three PyAutoArray plot
    sites (autoarray/plot/{array.py,inversion.py,grid.py}) that draw the
    generic `lines=` overlay. The `lines=` parameter is currently consumed
    exclusively by critical curves and caustics across PyAutoGalaxy and
    PyAutoLens, so the change targets exactly the reported overlays with
    no incidental side-effects. No public API touched; no config files
    involved — only the legacy z_projects/subhalo mat_wrap_2d.yaml
    contained these keys and it is not loaded by the active plot code
    path. Ran in parallel with knn-barycentric on PyAutoArray (distinct
    branches, disjoint file sets) without conflict. 780/780 PyAutoArray
    unit tests passed; user opted to merge without smoke tests given the
    surgical 3-line scope.
