# HowToGalaxy: should_simulate every dataset load; run under SMALL_DATASETS

Shipped 2026-07-21 (HowToGalaxy #30 MERGED). Slice 2/3 of the HowTo should_simulate migration.

17 raw exists-guards → `ag.util.dataset.should_simulate` (autogalaxy namespace — NOT al).
tutorial_3_fitting: fixed 1st-load guard (howtogalaxy produced by tutorial_2_data.py, not
simulators/simple.py) + added 2nd-load guard (simple). Removed dead howtogalaxy/+guides/
SMALL_DATASETS-unset overrides. Regen notebooks+catalogue. Verified every chapter passes on
FRESH dataset at 16x16: ch1 6/6, ch2 8/8, ch3 3/3, ch4 5/5. Sims in scripts/simulators/ (plural).

## Original prompt

# HowToGalaxy: should_simulate every dataset load; run under SMALL_DATASETS (slice 2/3)

Type: bug
Target: workspaces
Repos:
- HowToGalaxy
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Slice 2/3 of the HowTo should_simulate migration (mirror of the merged HowToLens#39).
Sims live in `scripts/simulators/` (**PLURAL**): simple.py→`simple`, sersic.py→`simple__sersic`,
sersic_x2.py→`sersic_x2`. The `howtogalaxy` dataset is produced by a chapter tutorial
(tutorial_2_data.py, analog of HowToLens tutorial_6_data).

Plan: 17 raw `if not dataset_path.exists():`→`al.util.dataset.should_simulate(str(dataset_path))`;
add guard for tutorial_3_fitting's unguarded 2nd load; verify/fix any guard pointing at the wrong
producer for the `howtogalaxy` dataset (tutorial_7-style latent bug); remove the DEAD
`howtogalaxy/`+`guides/` SMALL_DATASETS-unset overrides (matched 0 files); regen notebooks+catalogue.
Verify every chapter passes on a FRESH dataset/ (rm -rf per chapter) at 16x16. Do NOT restore
committed datasets (#126). dataset/ gitignored.
