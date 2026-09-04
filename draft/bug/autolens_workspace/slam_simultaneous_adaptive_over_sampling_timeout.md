# SLaM multi-dataset `simultaneous.py` times out (1805 s) after the #523 adaptive over-sampling change

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci
- hygiene
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Review-minutes: 5
Unattended: ready
Filed: 2026-09-04

## The finding

PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194
(profile `release`, per-script cap `BUILD_SCRIPT_TIMEOUT=1800`) hit
`TIMEOUT (1805s)` on `scripts/multi_dataset/features/slam/simultaneous.py`.

Timing history for the same script under the same profile:

| Date | Result |
|------|--------|
| 2026-09-02 | PASS 355.7 s |
| 2026-09-03 | PASS 366.9 s |
| 2026-09-04 | **TIMEOUT 1805 s** |

The runner is not the cause: every other `multi_dataset` script in the same job
ran at 0.74-1.03x its previous time (the sibling
`scripts/multi_dataset/features/slam/independent.py` went 179.7 s -> 166.4 s).

The only change to the script in that window is commit `17568188`
(autolens_workspace #523, "SLaM adaptive over-sampling thresholds the S/N map
once, from source_pix_2"), which added

```python
dataset.apply_over_sampling(
    over_sample_size_pixelization=al.Array2D(
        values=np.where(source_image_raw > 3.0, 4, 2), mask=...
    )
)
```

to the `source_pix_2`, `light_lp` and `mass_total` analyses, inherited by the
SUBHALO stages. #532 (`94665797`, per-band `DatasetModel`) does not touch those
calls.

The nominal sub-pixel count went **down** (the dataset default is a uniform
sub-size of 4, the new map is 4 on the bright source and 2 elsewhere), so the
suspect is the switch from a uniform `int` to a non-uniform `Array2D`
over-sample map on the `use_jax=True` pixelized + subhalo-grid-search path -
or a script-level misuse of the new API specific to this multi-dataset script.
`independent.py` makes the same change and got *faster*, so whatever is slow is
particular to the simultaneous (FactorGraph + subhalo) pipeline.

## What to do

1. Time the script per stage under the release-profile environment to find
   which search explodes.
2. Fix it minimally, keeping the script near its ~367 s baseline: prefer
   repairing a genuine misuse; otherwise drop the adaptive
   `over_sample_size_pixelization` from the affected stages of this script with
   a comment naming #523 and the follow-up.
3. If the cost is a library-side slow path for non-uniform over-sample maps,
   file that separately against PyAutoArray.
