# euclid_dr1: sanitise positions.json (drop central/spurious multiple images) before modelling

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Scheduled: 2026-09-24
Consequence: glance
Witness: sanitised positions.json for the 5 output_locked example tiles trace to a max source-plane separation < 0.2" under the adopted check, and the check reproduces the census verdicts on locked_tiles.csv / completed_tiles.csv (≥99% of locked flagged, ≤0.5% of clean unlocked flagged).
Review-minutes: 3
Unattended: needs-slicing


Scheduled for 2026-09-24. Code: the positions.json producer lives in euclid_strong_lens_modeling_pipeline (preprocess/segmentation.py, util.py load path); then port it to the euclid_dr1 science project (/mnt/c/Users/Jammy/Science/euclid_dr1) and apply it to its dataset/dr1_sep1_rest tiles.

Do all three steps:
1. Reject any image within 0.3" of the lens light, or one dominated by lens flux.
2. Merge images closer than 0.2" apart.
3. Run the tracing check and drop the one image that makes the set traceable.

Tiles where no single drop fixes the set, or where any drop does, go to a by-eye review list rather than being auto-dropped.

## Research first: how best to set up the ray-tracing check
The 2026-09-23 prototype is a numpy SIE + external shear point-tracing check. It fixes the mass centre at the brightest-pixel light centre, runs multi-start Nelder-Mead over (einstein_radius, ell_comps, gamma) within the vis_lp bounds, minimises the max pairwise source-plane separation, and fails the set if the best is > 0.2". It reproduces PyAutoLens positions.info to 1e-11 at fixed parameters, and predicts 99.0% of locked / 0.1% of unlocked fits (13/4882 disagreements). Open questions to research before adopting it:
- Honour the sigma=0.3 Gaussian ellipticity prior (currently bounds only, so it is too permissive).
- Optimiser robustness (local multi-start; the 13 disagreements).
- The fixed-centre assumption (should the centre be free within a small box?).
- Whether the 0.2" threshold is too tight for 0.1" pixels: 22% of even clean unlocked fits finish pinned at the 0.2" wall.
- Should it use PyAutoLens's own tracer rather than a numpy re-implementation, and where should it live (segmentation writer vs load_vis_dataset vs a standalone pre-submit gate)?

## Evidence (2026-09-23 census)
- 736 / 4,912 completed vis_lp fits (15.0%) are positions-penalty locked (the manifest's 741/4922 includes 10 completed tiles with no zip). Causes: central/nucleus <0.3" 108 (15%); inner spurious image on the lens-light wings 322 (44%); outer/neighbour 142 (19%); other or by-eye 155 (21%); traceable but locked anyway 7 (1%).
- Raw arcsec distance barely discriminates (median min_r_light 0.63" locked vs 0.65" unlocked). Distance relative to the Einstein-radius proxy does: min_r/thetaE < 0.5 in 68% of locked vs 20% of unlocked.
- 294 unlocked fits (7.1%) carry an image within 0.3" of the light centre and bent the mass model to absorb it. Compared with clean fits, 34% vs 22% have separation pinned at 0.2", 60% vs 25% have |gamma| > 0.25, and the median thetaE/ring is 0.81 vs 0.96. Six RAL spot-checks confirm the pattern.
- Of roughly 9,000 tiles not yet on RAL, about 1,650 are predicted to lock and 573 more carry a central image. 76 of the 85 unfinished RAL runs are predicted to lock.

## Deliverables
- Copy the census into the project (e.g. inspect/positions_census/). Source (session scratchpad, ephemeral): /tmp/claude-1000/-home-jammy-Code-PyAutoLabs/f6d9d1ab-336c-4bd3-adb2-ec380b7ed943/scratchpad/census. It contains trace.py, geometry.py, analyse.py, ral_extract.py, figures.py, per_tile.csv (with suggested_drop_index and category), affected_tiles_by_category.csv, locked_tiles.csv, completed_tiles.csv, summary_numbers.txt and fig1-4.
- Implement the three-step sanitiser, keeping the original positions.json recoverable (e.g. write positions_raw.json).
- Remodel set: 736 locked + 294 unlocked-central + 5 unlocked failing the check + 85 unfinished. Pending (unsubmitted) tiles get sanitised positions before submission.
- Spot-check a sample of "inner" drops by eye before bulk-dropping, because some could be genuine counter-images.
- Record the census and outcome in the euclid_dr1 Cortex ledger / wiki/project.

<!-- formalised by the Intake (Conception) Agent on 2026-09-23 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/f6d9d1ab-336c-4bd3-adb2-ec380b7ed943/scratchpad/intake_raw.md -->
