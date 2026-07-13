## imaging-from-fits-small-datasets-cap
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/301
- repos: PyAutoArray
- notes: |
    Library-side companion to multi-viz-imaging-small-datasets-override
    (PR #80 in autolens_workspace_test). User asked for the proper fix:
    "everything in the source code should honor PYAUTO_SMALL_DATASETS=1".
    Closed the asymmetry where Mask2D.circular and Grid2D.uniform capped
    to (15, 15) at 0.6"/px under the env var but Imaging.from_fits did
    not — silently producing shape mismatches that crashed apply_mask
    with a (150,150) vs (15,15) ValueError. Added
    autoarray.util.dataset_util.cap_array_2d_for_small_datasets, a
    center-crop helper that mirrors the existing caps. Hooked it into
    Imaging.from_fits for data + noise_map (PSF intentionally untouched
    — PSFs are usually <15x15 and capping changes their shape semantics).
    No-op when env unset OR when on-disk shape is already at-or-below
    the cap, so the simulator -> from_fits round-trip is unchanged.
    +123 lines library, +123 tests across two test files; full
    test_autoarray suite 747/747 green.

    Center-crop was chosen over downsample/resample because (a) smoke
    mode doesn't need numerical correctness, (b) center-crop preserves
    central pixels (where lens/galaxy signal sits), (c) avoids a scipy
    dependency at this layer, and (d) matches the existing convention
    of "fixed cap at smoke geometry" used by Mask2D.circular.

    Cluster-E reproducer (autolens_workspace_test/scripts/multi/
    visualization_imaging.py with PYAUTO_SMALL_DATASETS=1 and the
    env_vars.yaml override stripped) now exits 0 cleanly: data 150->15,
    psf preserved at 21x21, mask 15, apply_mask succeeds.

    Smoke ran across all 6 workspaces (autofit, autogalaxy, autolens,
    autolens_test, HowToLens, euclid) with the worktree's autoarray
    active. 36/44 passed in-scope; 6 euclid failures were pre-existing
    WorkspaceVersionMismatchError (workspace pinned at 2026.4.13.6 vs
    library 2026.5.1.4) — orthogonal, confirmed by bypass with
    PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1. No regressions attributable
    to this PR.

    **Follow-ups worth filing:**
    1. PyAutoArray: extend the same helper to Array2D.from_fits and
       Grid2D.from_fits for full consistency (and PSF-aware logic in
       Kernel2D.from_fits — preserve odd shape, re-normalize after crop).
    2. autolens_workspace_test: revert the multi/visualization_imaging
       env_vars.yaml override (PR #80) once this library fix has lived
       on main for a release cycle. The override is now redundant but
       harmless; reverting confirms the library cap is sufficient.
    3. euclid_strong_lens_modeling_pipeline: bump pinned library version
       to 2026.5.1.4 (separate from this work, but surfaced by smoke).
