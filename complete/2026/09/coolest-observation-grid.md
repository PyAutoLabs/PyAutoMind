## coolest-observation-grid
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/739
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/740 (merge 223132c0)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/551 (merge 2c7a184)
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/82 (merge d83f05ca)
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/740
- summary: |
    An external review of the COOLEST guide found `al.interop.coolest.to_coolest()` wrote every template
    with an empty `observation.pixels` block (field of view and pixel counts 0), which COOLEST's plotting
    API cannot render. `to_coolest` now writes a `PixelatedRegularGrid` from `shape_native` + `pixel_size`
    or from `dataset=` (anything with `shape_native`/`pixel_scales`), warns when neither is given, and gains
    `on_unsupported="skip"`: the full mass model and any Sersic light export while MGE `Basis` and
    `Pixelization` components are omitted and listed under `meta.skipped_profiles` (default `"raise"`
    unchanged). The workspace guide passes the grid and documents the skip policy (notebook regenerated).
    The Euclid pipeline writes `files/coolest.json` from every search via `coolest_json_from` in
    `save_results`, guarded like `wcs.json` (missing package or conversion error = logged warning); the
    inspection bundle collects `coolest.json` (vis_pix) and `coolest_sersic.json` (sersic stage) best-effort;
    README gains a final "COOLEST output" section with the Galan et al. 2023 JOSS citation and
    `autolens[coolest]` in the install line; 7 fast + 2 slow tests.
- witness: |
    A 100x100 / 0.1" template loads with num_pix_x 100 and field_of_view_x (-5, 5), passes
    `check_consistency_with_instrument`, and `ModelPlotter.plot_surface_brightness/plot_convergence` render;
    the same model without a grid reproduces the reviewer's `IndexError`. PyAutoLens test_autolens 653
    passed (interop 13, 7 new). Pipeline fast 131 / slow 10 / smoke 9/9; test-mode vis_pix template =
    SIE + ExternalShear, `skipped_profiles` = `Basis(Gaussian x 40)` + `Pixelization(Delaunay)`, grid
    100x100 +-5.0". Negative controls: `on_unsupported="raise"` fails 5/7 new pipeline tests; dropping
    `dataset=` fails the grid test.
- science: |
    euclid_dr1 clone (`Science/euclid_dr1`, never pushed): pipeline branch merged (36ba572),
    `hpc/batch_cpu/submit_reload_coolest` + ledger `wiki/project/2026-09-16-coolest-json-reload-pass.md`;
    reload pass RAN 2026-09-17 as SLURM 343367 on RAL (9/9 COMPLETED, 29-35 s; two "Forcing pickle
    overwrite" per task, no `coolest.json:` warning); `files/coolest.json` in 18/18 zips and in all nine
    dr1_sep1 bundle folders; `force_pickle_overwrite` back to false; backup `output.prezip.bak.2026-09-16b`
    (108 MB) left on RAL for the human to delete. RAL venv now has `coolest` 0.1.11 and PyAutoLens main
    223132c (HPCPullPyAuto run), so the DR1 run writes COOLEST by default.
- traps: |
    Converters raise `ag.exc.ProfileException`, not `ValueError`. A `Basis` is both a LightProfile and a
    MassProfile (dedupe by id). A pixelized galaxy under "raise" still silently exports an empty entity
    (pre-existing). The pipeline CI builds PyAutoLens from the SAME-NAMED feature branch, so #82 was green
    before #740 merged. Heart RED at ship (`install verification FAILED (testpypi; checks F)`,
    `release validation FAILED (stage integrate)`), human-authorised PR-open override; a third reason
    (PyAutoArray behind origin) was local staleness. The auto-mode classifier blocked `gh pr merge` once
    ("Merge Without Review"); `/prm` typed by the human merged the rest. #82 went CONFLICTING on
    catalogue/README.md after #81 merged (both added bundle-table rows); merged main forward. Five
    parallel claims on the pipeline repo and one on autolens_workspace waived on disjoint file sets. The
    bundle script needs `OUTPUT_DIR/<sample>` nesting; the clone's flat `output/` needs a symlink dir.
    RAL venv is `$PYAUTO_HPC_BASE/PyAuto`; project `activate.sh` needs `PYAUTO_HPC_BASE` exported.
- follow-ups: |
    Filed: `draft/feature/autolens/coolest_pixel_grid_export.md` (MGE -> PixelatedRegularGrid, pixelized
    source -> IrregularGrid); `draft/maintenance/euclid/skip_fit_output_no_longer_gates_save_results_docs_drift.md`.
    Human: delete RAL backups `output.prezip.bak.2026-09-16{,b}` once trusted; euclid_dr1 clone
    `git merge origin/main` (carries #81 + #82) and `hpc/sync push --no-data`. `autolens_workspace_test`
    `misc/interop/coolest_round_trip.py` emits the new no-grid warning twice (harmless).

## Original prompt

# COOLEST: fix the empty Observation pixel grid, emit coolest.json from the Euclid pipeline by default, carry it into euclid_dr1

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
- euclid_strong_lens_modeling_pipeline
Themes:
- coolest
- interop
- euclid
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-09-16
Issued: 2026-09-16

## Request (verbatim)

> Hi Aaron,
> The models and results for the 3,000 DR1 lenses described in ECLIPSE C are here: Next week I'm planning to model the full DR1 sample (~15,000 lenses). I've also added COOLEST outputs to PyAutoLens, which are described here:
> https://github.com/PyAutoLabs/autolens_workspace/blob/main/scripts/guides/coolest_interop.py
> These aren't included in the 3,000 models above. it's a new feature that I'll use for the full run next week.
> The COOLEST guide and the conversion code above are fairly vibe-coded and have had less human oversight than I'd normally like. If you could take a look and confirm that everything makes sense before I blitz through the full DR1 sample next week, that'd be massively appreciated!
>
> Hey James,
>
> I just wanted to let you know that I checked out the COOLEST conversion code. I noticed one small problem with the json it created. In the "observation/pixels" attribute, "field_of_view_x(/y)" and "num_pix_x(/y)" are all automatically set to 0. It appears that the al.interop.coolest.to_coolest() imports an empty COOLEST Observation object with these values preset to 0.
>
> When I try to plot with these values in the COOLEST api, however, COOLEST doesn't know how to handle them. After editing the values in the json so that they result in a pixel scale equal to the one found in the "instrument" attribute, COOLEST makes a nice-looking plot. This was the only issue I was able to find so far!
>
> Can you 1) Check and fix the issue Aaron brought up; 2) ensure COolest is supported documenting and working on the euclid_strong_lens_modeling_pipeline, dont make it front and centre but ensure runs output coolest by default and that the bottom of the README.md mentions this with citation this includes ensuring its output as a .json file when we do catalogue generation; 3) Add Coolest support to the euclid_dr1 science project and ensure its in the catalogue, if it isnt already!

## Scope

1. **PyAutoLens** — `to_coolest` builds a `PixelatedRegularGrid` for `lazy.Observation` from
   `shape_native` + `pixel_size` (or a `dataset=`), warns when no grid is given, and gains
   `on_unsupported="skip"` which exports the mass model plus any Sersic light and records the
   omitted components (MGE `Basis`, pixelized source) under `meta.skipped_profiles`. Tests.
2. **autolens_workspace** — the COOLEST guide passes a pixel grid and documents the skip policy;
   notebook regenerated.
3. **euclid_strong_lens_modeling_pipeline** — every search writes `files/coolest.json` from
   `save_results` (guarded like `wcs.json`, missing package is a logged warning); the
   inspection bundle collects `coolest.json` / `coolest_sersic.json`; README gains a final
   "COOLEST output" section with the Galan et al. 2023 JOSS citation and `autolens[coolest]`
   in the install line; unit + slow tests.
4. **euclid_dr1 science clone** (after the pipeline PR merges) — merge pipeline main, add
   `hpc/batch_cpu/submit_reload_coolest`, ledger page; RAL reload leg on the human's go.

Decision (user-confirmed at planning): unsupported light/source components are **skipped and
recorded**, not converted. Pixel-grid export (MGE → `PixelatedRegularGrid`, pixelized source →
`IrregularGrid`) is the follow-up prompt `draft/feature/autolens/coolest_pixel_grid_export.md`.
