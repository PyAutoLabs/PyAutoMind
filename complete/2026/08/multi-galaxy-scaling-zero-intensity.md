- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/518 (CLOSED)
- completed: 2026-08-29
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/519 (merged -> main)
- repos: autolens_workspace
- summary: Third (and last) park cause for `multi_galaxy/features/scaling_relation/slam` fixed and the park REMOVED. Root cause (static diagnosis reproducing the measured 80/192 mask counts, then confirmed by an instrumented run): the simulator placed the five scaling-tier galaxies at 6.40–7.11" on a ±7.5" grid; under PYAUTO_SMALL_DATASETS=1 the frame is 16x16 @ 0.6" = ±4.8", so every tier member was off-frame and the positive-only (fnnls) linear solve returned exactly 0.0 (main galaxies 15.09 / 11.54, tier 0/0/0/0/0) → `Measured luminosity is 0.0`. Not a library or test-mode bug — a simulator-geometry artefact of the cap; the imaging sibling's tier sits at 4.7–5.1" and survives. Fix: `simulator.py` tier centres as fractions of the grid half-width (literals/7.5 — full-res `scaling_galaxies_centres.json` round-trips to exactly the old values; under the cap the tier lands ≤ 4.55", inside the 4.70" mask); `slam.py` raises a legible geometry ValueError when a tier member falls outside the post-cap enlarged mask (verified on the old geometry: "needs a radius of 7.61" … image is only 4.80" … Galaxy radii are [0.43, 0.43, 7.11, 6.4, 6.95, 6.95, 6.96]"); `lens_light_1` takes sigma_min from its own dataset (was a module-global read). Gate through the CI runner, cache-free, both forms: exit 0 (9.4 s), radius 4.70, luminosities 49.58 / 31.23 / 0.79 / 0.51 / 0.55 / 0.33 / 0.23, 7 searches, 0 "Fit Already Completed". Notebooks regenerated. CI green (Smoke py3.12/3.13, Navigator x3, Size Guard).
- history: cause 1 (#419, loader mislabel) → PyAutoArray#431; cause 2 (mask collapse) → autolens_workspace#502, verified in #516; cause 3 (this) → #519. The un-park attempts were #514 (kept, reason rewritten) and now #518.
- traps: the simulator has no noise seed, so FITS arrays cannot be bit-compared — identity is proven at the centres JSON. The mask request's `+0.5` is a light-enclosure buffer, not a frame requirement, so a guard on `galaxy_distances.max() + 0.5 > image_half_width − 0.1` would fire on every capped run; the guard checks members against the post-cap mask radius instead.
- heart-ack: shipped/merged under human-acknowledged YELLOW (2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source".

## Original prompt

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
Issued: 2026-08-29
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
