## cluster-c-point-source-rebaseline
- completed: 2026-05-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/78
- repos: autolens_workspace_test
- notes: |
    Surfaced in a release-prep triage report as Cluster C: three JAX
    point-source likelihood scripts (image_plane.py, point.py,
    source_plane.py) failing `np.testing.assert_allclose` against
    hardcoded `expected_likelihood` literals. Root cause was upstream
    commit 931a381 (six days earlier) changing
    `positions_noise_map` from `grid.pixel_scale` (0.2") to `0.005"`
    in `scripts/jax_likelihood_functions/point_source/simulator.py` —
    the committed seed dataset under `dataset/point_source/simple/`
    was last regenerated under the old noise from `pre build`
    (a88f0f6, May 1) and was never refreshed when the simulator
    changed. Because `should_simulate` only fires when the dataset
    path is missing, canonical `main` was actually passing — old
    dataset matched old literal — but any clean re-simulation hit
    the failure the user reported.

    Fix regenerated the seed dataset (`point_dataset_positions_only.json`,
    `tracer.json`) and rebaselined three literals: 1.313508 →
    -83.38049778 (image_plane.py and point.py — same dataset, same
    prior medians, identical values), and -199.1555813 →
    -331481.25978149 (vmap) / -331481.26508536364 (eager) for
    source_plane.py. The 1664x source_plane.py drift checks out as
    chi-squared rescaling: noise dropped 40x, so chi^2 scales by
    1600x.

    Verify-triage-clusters habit paid off — going through the chain
    `simulator → committed dataset → should_simulate semantics →
    canonical state` exposed that the failure mode required deleting
    the on-disk dataset to reproduce, which changed how I handed the
    user the choice (regenerate-and-commit vs leave-alone). Smoke
    tests 11/11 passed; one pre-existing skip (database/scrape/general,
    NEEDS_FIX 2026-04-27) unrelated.
