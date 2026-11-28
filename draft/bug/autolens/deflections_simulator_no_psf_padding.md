# PyAutoLens `via_deflections_galaxies_from` simulates without PSF padding/trim

Type: bug
Target: autolens
Repos:
- PyAutoLens
Themes:
- correctness
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Witness: A simulation from `SimulatorImaging.via_deflections_galaxies_from` matches `via_tracer_from` for the same lens to within noise at the image edges (padded, convolved, then trimmed), shown by a unit test in `test_autolens/imaging/test_simulator.py`.
Filed: 2026-11-26

Found during PyAutoArray#719 (shift 2026-11-26-pm, review leg 3).
`autolens/imaging/simulator.py:169` (`via_deflections_galaxies_from`) passes
an unpadded image to `via_image_from` and never calls
`trimmed_after_convolution_from`, so the PSF convolution has edge effects at
the image border. `via_tracer_from` and `via_source_image_from` pad by the PSF
shape and trim afterwards. Until PyAutoArray#719 the convolver's
"No blurring_image provided" warning was the only (vague) hint; the simulator
now silences that warning, so this path is quiet.

Fix: pad before convolution and trim after, the way `via_source_image_from` does.
