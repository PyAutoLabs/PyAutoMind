# multi_galaxy/features/scaling_relation/slam measures 0.0 luminosities under the smoke profile — third park cause

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-29
Related: autolens_workspace#514 (the gated un-park that found this), autolens_workspace#513 (imaging sibling, passes)

`scripts/multi_galaxy/features/scaling_relation/slam.py` is still parked in
`config/build/no_run.yaml` — now for a third, distinct reason, found by the cache-free
capped run of 2026-08-29 (autolens_workspace#514) that was meant to un-park it.

## What was verified (so nobody re-diagnoses it)

- Cause 1 (0.0 luminosity from the capped-loader pixel-scale mislabel, #419) → fixed by
  PyAutoArray#430/#431. Confirmed on the imaging sibling: anchor luminosity 22.47 (#513).
- Cause 2 (mask collapse from `image_half_width` computed off the script's `pixel_scale`
  literal, radius 0.30, "zero-size array") → fixed by #501/#502 and **verified here**:
  the run prints `Standard mask radius: 3.0` / `Enlarged mask radius: 4.70`
  (= `0.5 * 16 * 0.6 - 0.1`), masks are populated (80 and 192 pixels), and both
  `lens_light[1]` and `lens_light[2]` run to `Search complete`.

## What fails now

```
File ".../scripts/multi_galaxy/features/scaling_relation/slam.py", line 969, in <module>
    main_luminosities, scaling_luminosities = luminosities_from(
File ".../slam.py", line 193, in luminosities_from
File ".../slam.py", line 146, in luminosity_from
ValueError: Measured luminosity is 0.0, but the scaling relation needs a positive value ...
```

`luminosity_from` (`slam.py:120-146`) sums `2π σ² / q · intensity` over
`galaxy.bulge.profile_list`; every linear `intensity` in the max-likelihood sample of the
truncated MGE stages is 0.0. Runs: 4 attempts, all exit 1 in 8–12 s; the two authoritative
ones were on a fully cleared tree (`output/multi_galaxy`, `output/test_mode/multi_galaxy`,
`dataset/multi_galaxy/scaling_relation` removed — the script's `path_prefix` is
`multi_galaxy/slam/`, NOT `multi_galaxy/features/scaling_relation/`, so the obvious clear
path clears nothing and a stale tree fakes a pass via "Fit Already Completed").

## Why this is not "test mode can't do it"

The imaging sibling (`imaging/features/scaling_relation/slam.py`) runs the same smoke
profile (`PYAUTO_TEST_MODE=2`, `PYAUTO_SMALL_DATASETS=1`) and measures a non-zero anchor
from its light stage. Both simulators put their galaxies within ~0.35" of the origin, so
this is not the off-frame mechanism of cause 1 either. The difference is in this script's
two-stage light setup: `lens_light[1]` fits the co-dominant pair on the standard mask,
`lens_light[2]` fits the scaling tier on the enlarged mask with the pair fixed
(`slam.py:30-48, 240, 253, 331`). Candidates to check first:

- which stage's sample yields the zeros — the pair (`lens_light[1]`) or the tier
  (`lens_light[2]`); and whether the tier galaxies fall outside the 16×16 capped frame
  even though the mask radius is right (the enlarged mask is 4.7" on a 4.8" half-width);
- whether the fixed-instance pair in `lens_light[2]` leaves the linear solve nothing to
  fit (the `slam.py:331` message hints the stage "has no free parameters");
- whether `PYAUTO_TEST_MODE=2`'s single likelihood call ever populates the MGE
  intensities on the enlarged dataset the way it does for the imaging script.

## Fix shape

Diagnose first (one capped run with the intensities printed per galaxy per stage). If the
tier is off-frame under the cap, the fix is the simulator/dataset geometry or the capped
mask, not the script. If the linear solve genuinely returns zeros for a fixed-pair stage,
fix the stage setup. Only then re-run the #514 gate and un-park. Do not add a
test-mode-only luminosity fallback: that hides exactly what the guard was written to catch.
