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
