## multi-viz-imaging-small-datasets-override
- completed: 2026-05-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/80
- repos: autolens_workspace_test
- notes: |
    Cluster E from the 2026-05-07 release-prep triage.
    `autolens_workspace_test/scripts/multi/visualization_imaging.py`
    crashed in the local triage runner with `ValueError: operands
    could not be broadcast together with shapes (150,150) (15,15)` at
    `dataset.apply_mask(mask=mask)`. The triage report's prescribed
    fix ("derive mask shape from dataset.shape_native, not from a
    hardcoded constant") was a no-op — the script already does that.
    Real cause: `PyAutoArray/autoarray/mask/mask_2d.py:363-366`
    silently overrides `shape_native` to (15,15) when
    `PYAUTO_SMALL_DATASETS=1`, *even when shape_native is explicit*,
    while `Imaging.from_fits` does not cap the dataset. The triage
    runner picked up the failure because
    `autolens_workspace_test/config/build/env_vars.yaml` sets
    `PYAUTO_SMALL_DATASETS: "1"` as a workspace-wide default; the
    GitHub Actions release.yml does not (only sets it for non-`_test`
    workspaces, lines 965–971), which is why CI passes. Fix: 9-line
    additive entry in env_vars.yaml unsetting the cap for
    `multi/visualization_imaging` (matching the existing
    `imaging/visualization` precedent). Sibling
    `multi/visualization_interferometer.py` was left alone — it
    passes under the cap currently and the triage didn't flag it
    (whether its likelihood is correct under a 15x15 real-space mask
    is a separate correctness question). Pure config change; no
    library or script touched.

    **Follow-up worth filing as a PyAutoArray issue:**
    `Mask2D.circular`'s `PYAUTO_SMALL_DATASETS=1` cap silently
    overrides an explicit `shape_native` argument. Two options for a
    proper fix: (a) only apply the cap when shape_native is at its
    default, or (b) make `Imaging.from_fits` also honour the env var
    so dataset and mask stay consistent. Both need a careful audit of
    every smoke test that currently relies on the implicit cap.
