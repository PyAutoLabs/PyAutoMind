# Prepare the Euclid pipeline for an ordered, low-disk DR1-prelim catalogue rebuild

Type: feature
Target: workspaces
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: large
Autonomy: supervised
Priority: normal
Issued: 2026-09-09
Status: formalised
Consequence: judge
Witness: A vis_lp run under the new config leaves no unzipped sibling directory beside its zip and writes no samples.csv, cutting its zip payload below 40% of the 2026-09-07 baseline of 130 MB across 17 zips; the new row-level comparator reports zero mismatches against the original euclid reference for the ten dr1_prelim tiles outside the declared tolerances (identity and astrometry exact, Einstein radius and per-band magnitudes within combined 3 sigma, MGE ell_comps matched up to a set swap); and scripts/build_inspection_bundle.sh runs to completion against a vis_lp-only tree instead of aborting on an empty aggregator.
Review-minutes: 25
Unattended: ready

# Prepare the Euclid pipeline for an ordered, low-disk DR1-prelim catalogue rebuild

Type: feature
Difficulty: large
Autonomy: supervised
Priority: normal
Witness: A vis_lp run under the new config leaves no unzipped sibling directory beside its zip and writes no samples.csv, cutting its zip payload below 40% of the 2026-09-07 baseline of 130 MB across 17 zips; the new row-level comparator reports zero mismatches against the original euclid reference for the ten dr1_prelim tiles outside the declared tolerances (identity and astrometry exact, Einstein radius and per-band magnitudes within combined 3 sigma, MGE ell_comps matched up to a set swap); and scripts/build_inspection_bundle.sh runs to completion against a vis_lp-only tree instead of aborting on an empty aggregator.

Work in euclid_strong_lens_modeling_pipeline. Prepare this repo so the euclid_dr1_prelim runs
can be repeated under ordered MGE bases at a fraction of the disk cost, and so a catalogue can
be rebuilt from them and checked against the original euclid catalogue locally and on RAL. The
run and science arc is tracked separately as one science task; this prompt is only the code it
depends on. Items 1-4 gate the reruns and should land first; items 5-7 are only needed before
the catalogue build, so this splits naturally into two phased PRs.

1. Temporary unzip for every aggregator. Pass `unzip_temporary=True` at all nine
   `Aggregator.from_directory` call sites: `catalogue/scripts/{deblending,lens_mass,
   lens_sersic,source_sersic,multi_wavelength,magnitudes}.py` and
   `workflow/{csv_make,fits_make,png_make}.py`. None pass it today. Default extraction leaves
   a permanent sibling directory beside every zip; the measured local `output/` tree is 501 MB
   = 130 MB of zips plus ~371 MB of redundant extracted duplicates, and all 17 zips currently
   have such a sibling. Reading results straight out of a zip is not available — no
   zipfile-backed loader exists in the aggregator, and that approach was rejected earlier —
   so temporary extraction is the supported answer.

2. HPC mode on, without turning on-the-fly updates on. In `config/general.yaml` set
   `hpc.hpc_mode: true` (currently false). This is also the real disk lever: the search
   library's `non_linear/paths/abstract.py:184` forces `remove_files = True` under HPC mode,
   deleting the unpacked output after zipping. In the same edit set
   `hpc.iterations_per_quick_update: 1e99` (currently 10000), because
   `non_linear/search/abstract_search.py:250` swaps the whole `hpc:` block in when HPC mode is
   on — leaving 10000 would switch on-the-fly quick updates ON, the opposite of the intent,
   and a quick update is what killed run 342301_3.

3. Disable samples.csv. In `config/output.yaml` set `samples: false` (currently true).
   Measured: `samples.csv` is 79.0 MB of the 130 MB zip payload (61%). The original euclid
   project already ran with `samples: false` and still built its full 2990-row catalogue, so
   the catalogue producers do not need it. Explicitly KEEP `search_log: true` and KEEP image
   visualization output — both are deliberate user decisions, not oversights.

4. Extend MGE ordering across the pipeline. `scripts/initial_lens_model.py` already passes
   `ell_comps_limit=0.5, order_bases=True` for the lens and `0.7` for the source (PR #58), but
   the other MGE builders do not: `scripts/full_model.py` at its two two-basis lens
   `mge_model_from` calls and its source call, and `scripts/mge_lens_only.py`. Bring these in
   line with initial_lens_model.py. Do NOT change `hpc/diagnostics/jax_fork_control.py` — it
   is a deliberate unordered control. `scripts/sersic_lens_model.py` and
   `scripts/lens_model_waveband.py` need no change: they build no MGE, they swap in a Sersic
   and read centres from the vis_lp result.

5. A catalogue-build submit script. This repo has no SLURM submit script that runs
   `scripts/build_inspection_bundle.sh`, so a RAL catalogue build currently has nothing to
   launch. Port one into `hpc/batch_cpu/`, modelled on the original euclid project's
   `hpc/batch_cpu/submit_build_inspection_bundle` (partition ral, 6 h, 8 GB, SAMPLE and
   RUN_TAG env overrides).

6. A row-level catalogue comparator. Today `tests/test_catalogue_parity.py` only reconstructs
   producer headers statically and compares them to stored fixtures; nothing compares the
   values of two built catalogues. Add a comparator that diffs a freshly built catalogue
   against the original euclid reference at
   `catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/` (2990 rows; all ten
   dr1_prelim tiles are confirmed present in it). It must compare tile identity and astrometry
   exactly, Einstein radius and per-band magnitudes within combined 3 sigma (independent
   nested-sampling runs are not bitwise reproducible), and treat MGE `ell_comps` as matching
   up to a set swap, since ordering deliberately changes the labelling.

7. Fix an empty-aggregator crash. `catalogue/scripts/lens_mass.py` lets
   `ValueError("The aggregator is empty.")` out of `af.AggregateCSV` when the query matches
   nothing, aborting the whole of `scripts/build_inspection_bundle.sh`.
   `catalogue/scripts/deblending.py` degrades gracefully on the same case; make lens_mass.py
   behave the same way. The bundle defaults to `--search_name=vis_pix`, so pointing it at a
   vis_lp-only tree trips this.

Note: the aggregator's `unzip_temporary` is merged but not yet released. The local install is
a source install so it works locally, and RAL tracks the library mains, so an HPCPullPyAuto is
owed before the reruns launch.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/99cc7b63-471e-41d6-8867-5fced69005fd/scratchpad/intake_raw.md -->
