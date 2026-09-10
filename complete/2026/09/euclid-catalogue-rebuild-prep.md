## euclid-catalogue-rebuild-prep
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/60
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/61
  (phase 1, merge commit `93a389ee815e9ee746adeba93e0e39de653da2b6`)
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/68
  (phase 2, merge commit `dbbb2a510989d0fdd985df294c6c75550b21fca1`)
- summary: One issue, two phased PRs, preparing
  `euclid_strong_lens_modeling_pipeline` so the `euclid_dr1_prelim` runs can be
  repeated under ordered MGE bases at a fraction of the disk cost and a
  catalogue rebuilt from them and checked against the original euclid
  reference.
  **Phase 1 (#61, items 1-4 — gates the reruns):** `unzip_temporary=True` at all
  **nine** `Aggregator.from_directory` call sites
  (`catalogue/scripts/{deblending,lens_mass,lens_sersic,source_sersic,multi_wavelength,magnitudes}.py`
  and `workflow/{csv_make,fits_make,png_make}.py`), none of which passed it —
  default extraction was leaving a permanent sibling directory beside every zip
  (~371 MB of duplicates on a 130 MB zip payload). `hpc.hpc_mode: true` in
  `config/general.yaml` — the real disk lever, since
  `non_linear/paths/abstract.py` forces `remove_files=True` under HPC mode — with
  `hpc.iterations_per_quick_update: 1e99` in the same edit, because
  `abstract_search.py` swaps the whole `hpc:` block in when HPC mode is on and
  leaving `10000` would have switched on-the-fly quick updates *on*, the opposite
  of the intent (a quick update is what killed run 342301_3). `samples: false` in
  `config/output.yaml` (79.0 MB = 61% of the zip payload), with `search_log: true`
  and image visualization deliberately kept. MGE ordering
  (`ell_comps_limit`, `order_bases=True`) extended from `initial_lens_model.py`
  to `full_model.py` (two two-basis lens calls and the source call) and
  `mge_lens_only.py`; `hpc/diagnostics/jax_fork_control.py` left unordered as the
  deliberate control.
  **Phase 2 (#68, items 5-7 — gates the catalogue build):**
  `hpc/batch_cpu/submit_build_inspection_bundle`, the SLURM job this repo had no
  way to launch (partition `ral`, 6 h, 8 GB, `SAMPLE`/`RUN_TAG`/`OUTPUT_DIR`/
  `SED_OUTPUT_DIR` as `--export` overrides, `PROJECT_PATH`/`PYAUTO_HPC_BASE`
  carrying RAL defaults because `sbatch` does not inherit the login shell's
  exports), wired into `hpc/sync` usage/help and the `hpc/README.md` route table.
  `scripts/tools/compare_catalogues.py`, the row-level comparator the repo had
  never had — `tests/test_catalogue_parity.py` only reconstructed producer
  headers statically — implementing the issue's tolerances (tile identity and
  astrometry **exact**; declared quantities `effective_einstein_radius` and the
  per-band magnitudes within **combined 3σ**, σ being each side's 1σ half-width;
  MGE `ell_comps` matched **up to a set swap**, since `order_bases=True`
  deliberately re-labels the bases) plus **latent-completeness** checks on the
  catalogue under test (no blank latent cell — the `latent.`-prefix regression
  writes blank rather than raising; 3σ bounds strictly outside 1σ — the
  `row.py:102` regression that shipped a published DR1 catalogue with error bars
  understated threefold; `max_lh ≠ median` where a `_max_lh` column exists).
  Reference rows A has not built are reported as non-gating coverage; every
  undeclared column is measured under the same statistic and reported as
  informational. The **empty-aggregator guard** went to **three** producers, not
  the one the issue named: `lens_mass.py`, `lens_sersic.py` and
  `source_sersic.py` all let `ValueError("The aggregator is empty.")` out of
  `af.AggregateCSV` and aborted `build_inspection_bundle.sh` at stages 3, 4 and 5
  (`deblending.py`, `magnitudes.py` and `multi_wavelength.py` were already
  guarded). A `config/build/no_run.yaml` entry excludes the comparator from the
  smoke runner with a reason. 103 tests pass (`main` baseline 94): 6 new
  comparator cases and 3 new empty-query cases parametrized over the three
  producers, verified red before the fix.
- baseline: the comparator was run once as the PR's witness — **A** = the
  pre-fix `inspect/dr1_prelim_grade_ab_ordered_v2/` bundle (5 tiles), **B** = the
  June reference `dr1_prelim_grade_ab_catalogue_csvs_20260623/` (2990 rows). No
  catalogue was built and no `output*` tree touched. `RESULT: FAIL`, exit 1, on
  blank `effective_einstein_radius` cells in all five A rows — the expected
  pre-fix signature, and the thing the post-342629 rebuild has to clear. MGE
  `ell_comps` matched on neither ordering for any tile.
- finding (informational, and the reason the baseline was run): A and B are two
  independent runs of the **same model on the same data**, and they disagree by
  roughly **2-9× their own combined error bar, with excursions past 100σ** —
  `centre_0` median z 8.86 / max 152.4, `shear_gamma_1` 5.03 / 117.9,
  `einstein_radius` 2.30 / 84.6. The posteriors are tight enough (1σ half-widths
  ~0.0015 on values near 3) that a 0.3-arcsec shift between runs is z ≈ 85.
  Consequence: **a "within combined 3σ" parity witness cannot hold between two
  reruns**, so the Cortex task's witness must be restated against this measured
  rerun scatter rather than an absolute tolerance. A rebuild landing *inside*
  these numbers is reproducing the reference; one that reproduces these z values
  has changed nothing.
- trap: `tests/test_repo_invariants.py` requires **every** script in the repo to
  be either in the smoke allowlist or in `config/build/no_run.yaml` with a
  reason. A new tool script that takes anything other than the runner's
  `--dataset`/`--sample` fails the invariant test until its `no_run.yaml` entry
  lands in the same commit.
- trap: PyAutoHeart's reusable `smoke-tests.yml` skips its matrix on
  `pull_request` unless `scripts/`, `config/`, `.github/` or the smoke lists
  change. Phase 2 touched `scripts/tools/compare_catalogues.py` and
  `config/build/no_run.yaml`, so all nine legs (unit / slow / smoke × `changes` +
  3.12 + 3.13) actually ran and passed on `5551169`; an `hpc/`-and-`catalogue/`-
  only diff would have skipped them all.
- not this task's call: the phase-1 disk witness landed at **47.3%** of the
  130 MB 2026-09-07 baseline against the prompt's `<40%` clause (Cortex scoring,
  2026-09-10). That is the science task's judgement, not the code task's — the
  code did what items 1-3 specified.
- science follow-through: Cortex task
  `euclid_dr1_prelim/ordered_rerun_catalogue_parity`, RAL run 342629 (in flight
  at close-out). The catalogue rebuild and the parity ruling live there, not
  here.
- session: `claude --resume session_01JsGeXEmGmSJzvxzC7GUpZo`; worktree
  `~/Code/PyAutoLabs-wt/euclid-catalogue-rebuild-prep`, removed at close-out.

## Original prompt

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
