# HowToLens: should_simulate every dataset load; run under SMALL_DATASETS

Shipped 2026-07-21 (HowToLens #39 MERGED). Slice 1/3 of the HowTo should_simulate migration
(Build#155 Phase 2, fork b).

22 raw `if not dataset_path.exists()` → `al.util.dataset.should_simulate(str(dataset_path))`
(re-simulates stale data under the cap). Added missing guards: tutorial_0 (simple__no_lens_light),
tutorial_7 2nd load (simple__no_lens_light__mass_sis), tutorial_6_lens_modeling (lens_sersic).
Fixed tutorial_7 1st-load latent bug (the `howtolens` dataset is produced by tutorial_6_data.py,
not scripts/simulator/). Removed the DEAD howtolens/ + guides/ SMALL_DATASETS-unset overrides
(matched 0 files). Regenerated notebooks + navigator.

Verified every chapter passes on a FRESH dataset/ (cloud-shard isolation) at 16x16: ch1 9/9,
ch2 8/8, ch3 6/6, ch4 green. tutorial_5_borders + tutorial_10 stay no_run/SLOW-parked.
Slices 2/3 HowToGalaxy + 3/3 HowToFit remain.

## Original prompt

# HowToLens: adopt should_simulate for every dataset load (per-repo slice 1/3)

Type: bug
Target: workspaces
Repos:
- HowToLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Per-repo slice **1 of 3** of the decided fix in
`active/howto_validation_needs_simulator_stage.md` (Build#155 Phase 2, fork (b)).
This slice does **HowToLens only**; HowToGalaxy and HowToFit follow as slices 2
and 3. Do NOT restore committed datasets (re-opens #126). Build/verification runs
churn tracked `dataset/*.json` — restore before committing.

## Why should_simulate, not the raw exists-check
`al.util.dataset.should_simulate(str(dataset_path))`
(`PyAutoArray/autoarray/util/dataset_util.py:54`) is a **drop-in replacement for
`not dataset_path.exists()`** that additionally, under `PYAUTO_SMALL_DATASETS=1`,
`rmtree`s an existing dataset so the simulator re-creates it at reduced
resolution — avoiding the full-res-FITS-vs-15×15-mask shape mismatch. HowToLens
currently uses the **raw** `if not dataset_path.exists()` idiom (should_simulate
usage = ZERO), which is why `config/build/env_vars.yaml` carries a `howtolens/`
pattern that unsets `PYAUTO_SMALL_DATASETS` as a workaround. Canonical usage to
mirror: `autolens_workspace/scripts/weak/modeling.py:72`.

## Scope (audit each load; a dataset is self-sufficient only if EVERY distinct
## dataset_path it loads is preceded by a should_simulate guard to the right sim)

HowToLens sims live in `scripts/simulator/` (**singular**): `no_lens_light.py`,
`no_lens_light__mass_sis.py`, `lens_sersic.py`, `lens_x2.py`, `source_complex.py`.

1. **Add a missing guard** — `chapter_1_introduction/tutorial_0_visualization.py`
   (loads `simple__no_lens_light`, 1 load, 0 guards).
2. **Add guard for the 2nd (unguarded) distinct load** —
   `chapter_1_introduction/tutorial_7_fitting.py` (load ~line 617,
   `simple__no_lens_light__mass_sis`).
3. **Audit these multi-load files (loads > guards)** — add a should_simulate
   guard for each DISTINCT new dataset_path; a same-path reload needs no extra
   guard, so verify per load, do not blindly add:
   `chapter_2_lens_modeling/tutorial_6_masking_and_positions.py` (2/1),
   `chapter_3_search_chaining/tutorial_3_lens_and_source.py` (3/1),
   `chapter_4_pixelizations/tutorial_3_inversions.py` (2/1),
   `chapter_4_pixelizations/tutorial_5_borders.py` (5/1),
   `chapter_4_pixelizations/tutorial_6_lens_modeling.py` (2/1).
4. **Migrate raw → canonical** — replace `if not dataset_path.exists():` with
   `if al.util.dataset.should_simulate(str(dataset_path)):` in all guarded
   HowToLens tutorials, so `PYAUTO_SMALL_DATASETS` re-sim works. Once every
   HowToLens load is should_simulate-guarded, the `howtolens/` SMALL_DATASETS
   workaround in `config/build/env_vars.yaml` can be dropped (do it in THIS slice
   and confirm green, or leave a note for a follow-up — decide during impl).

Only edit `scripts/`, never `notebooks/` (regenerated). Preserve teaching prose;
the guard is a code block only.

## Verification (the real gate — a fresh clone per chapter in cloud CI)
`rm -rf HowToLens/dataset/` then run the full HowToLens sweep
(`run_all.py howtolens`) and confirm EVERY chapter passes first-time (no
FileNotFoundError). Then regenerate notebooks + navigator catalogue
(`generate.py howtolens`) and commit them with the scripts. Restore any churned
tracked `dataset/*.json` before committing.

<!-- filed 2026-07-21 as per-repo slice 1/3 of howto_validation_needs_simulator_stage
     (user chose per-repo, start HowToLens). Parent umbrella: Build#155 Phase 2. -->
