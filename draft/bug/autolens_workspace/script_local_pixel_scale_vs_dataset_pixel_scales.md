# Scripts derive geometry from a hardcoded pixel_scale while the dataset carries a corrected one

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-03 (backfilled from git)

Found while validating PyAutoArray#430 / PR#431 (the small-datasets loader fix), 2026-08-03.

## The bug

Workspace scripts declare a module-level `pixel_scale` literal (the dataset's true
scale in normal operation, e.g. `0.1`) and then use it in geometry arithmetic
*alongside* values read from the loaded dataset. Under `PYAUTO_SMALL_DATASETS=1`
the loader now correctly relabels capped data to `0.6`, so the script's literal
and `dataset.pixel_scales` disagree and the arithmetic silently produces nonsense.

Concrete instance — `scripts/multi_galaxy/features/scaling_relation/slam.py:863`:

    image_half_width = 0.5 * min(dataset_full.shape_native) * pixel_scale

    mask_radius_larger = min(
        max(mask_radius, float(galaxy_distances.max()) + 0.5), image_half_width - 0.1
    )

`shape_native` comes from the capped dataset (16) but `pixel_scale` is the script's
`0.1` literal, while the mask a few lines later is built from
`dataset_full.pixel_scales` (now `0.6`). The run prints:

    Standard mask radius: 3.0
    Enlarged mask radius: 0.30

— the "enlarged" mask is an order of magnitude *smaller* than the standard one. The
resulting mask has no unmasked pixels, and the failure surfaces as:

    File autoarray/operators/convolver.py:112, in ConvolverState.__init__
        y_min, y_max = ys.min(), ys.max()
    ValueError: zero-size array to reduction operation minimum which has no identity

## Not a regression

Control-tested on unpatched `main`: the same script fails *earlier*, with the
documented `Measured luminosity is 0.0` ValueError. PR#431 fixes that root cause and
this latent bug is what lies behind it. The script is already parked in
`config/build/no_run.yaml` as `multi_galaxy/features/scaling_relation/slam` and must
stay parked until this is fixed — update its NEEDS_FIX reason, which currently names
only the 0.0-luminosity cause.

## Scope: this is a class, not a one-off

Do NOT fix only line 863. Sweep the workspace for scripts that mix a local
`pixel_scale` literal with dataset-derived geometry (`shape_native`,
`pixel_scales`, mask radii, `image_half_width`-style arithmetic). The fix is to
derive geometry from `dataset.pixel_scales` rather than the literal — the literal
stays as the `from_fits` argument, which is its correct and only role.

Verification must include a capped-run pass, since the two values coincide in
normal runs and the bug is invisible there.

## Do not

Do not "fix" this by reverting the loader to keep the caller's uncapped scale — that
is PyAutoArray#430, and it mislabels the frame 6x. The loader is right; the scripts
are inconsistent.
