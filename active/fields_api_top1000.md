# Adopt fields API in the Euclid pipeline and launch DR1 top 1000

Type: refactor
Target: @euclid_strong_lens_modeling_pipeline
Autonomy: supervised
Filed: 2026-09-18
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/89

## Original request

Can you accept this https://github.com/PyAutoLabs/autolens_workspace/pull/560, and then implement the fields API in euclid_storng lens modeling piepline, then do it in the Science project euclid_dr1, HPCHPCPullPyAuto and get the 1000 lens run wehave been setting ussing up eclipse_catalogue_fits_sep1_top1000_brightest.csv going

## Proposed plan

1. Resolve workspace PR #560's explicit release hold. All three head workflows succeeded; PyAutoGalaxy#621 and PyAutoLens#742 merged September 17, but live PyPI still publishes 2026.9.15.1 from September 15. The sibling workspace_test#322 belongs to the same task; do not close the whole task on a partial merge.
2. Migrate pipeline shear composition to `fields=af.Collection(field=af.Model(al.MassField, ...))`, with lens redshift and existing shear priors preserved. Chain model or instance fields at the same stages as the existing shear. Preserve the full-model final-stage shear-prior reset.
3. Update result readers, simulator and regression fixtures; verify numerical parity, model parameter counts and prior/fixed chaining, catalogue shear columns, and COOLEST output. Run fast tests, the applicable smoke chain and real-output checks.
4. Apply the validated pipeline changes to the Cortex-registered euclid_dr1 science clone, preserving its 18 local commits, science configuration, datasets, old outputs and untracked top-1000 preparation. Never push that clone to its pipeline origin.
5. Verify no jobs use the shared RAL stack, resolve and run the existing HPCPullPyAuto command, confirm remote library revisions and fields support, sync through the project's CLI, and smoke one selected real dataset without overwriting production output.
6. Submit the existing CPU vis_lp-only top-1000 array using the project's hpc/sync CLI, confirm its job ID and queue state, then record the submission with Cortex verbs and update science session notes.

## Detailed implementation surface

- `scripts/initial_lens_model.py`: vis_lp model composition and vis_pix result chaining.
- `scripts/full_model.py`: all source/light/mass stages, including deliberate reset_shear_prior behavior.
- `scripts/sersic_lens_model.py`, `scripts/lens_model_waveband.py`: fixed fields carried alongside lens mass into photometric fits.
- `scripts/simulator.py`: separate tracer fields; preserve the simulated image and truth semantics without regenerating committed data unnecessarily.
- `catalogue/scripts/lens_mass.py`, `workflow/csv_make.py`, `workflow/example/csv/lens_mass.py`: fields.field.shear result paths; inspect compatibility requirements for existing galaxy-attached results.
- Existing tests including COOLEST, catalogue columns, Witt-Wynne and model-chain coverage: update fixtures and add meaningful parity/chaining coverage where absent.
- Science clone: port the validated diff selectively; review any science-only model/readout callers too. New model identifiers must not be mistaken for a resume of the old galaxy-attached fits.

## Branch survey and holds

- Pipeline canonical checkout is clean on main at cf66194. Proposed branch: feature/euclid-fields-api; worktree: euclid-fields-api via standard worktree helper after approval.
- worktree_check_conflict reports sed-chain-cpu-route, sersic-variants, sersic-variants-analysis and grid-offset-prior claims. Open PRs are #70 and #75. Coordinate overlapping script changes before implementation; no claim is silently waived.
- Science clone is main, 18 commits ahead of its pipeline origin, with untracked dataset/dr1_sep1/, dataset/dr1_sep1_top1000/, eclipse_catalogue_fits_sep1_top1000_brightest.csv and hpc/batch_cpu/submit_initial_lens_model_vis_lp_top1000. Preserve all.
- Plan approval required under workspace AGENTS.md before source edits. No issue, source edit, submission or merge performed at filing.

## Verified run preparation

- CSV has exactly 1000 rows; id_str exactly matches the submit script's 1000 unique tile names in order.
- All 1000 selected tiles have their named FITS and info.json under dataset/dr1_sep1_top1000/.
- Prepared script: hpc/batch_cpu/submit_initial_lens_model_vis_lp_top1000; array 0-999; partition ral; 8 CPUs, 64 GB and 18 hours per task; stage vis_lp only.
- hpc/sync jobs returned an empty queue on September 18. Recheck immediately before changing the shared stack or submitting.

## Approval — 2026-09-18

The human approved all three delivery phases and coordinating the existing branches: "yes do 1, 2, 3 remember that RAL is a clone of github so we dont need a release for those changes rto take effecft, letts merge PRs if possible on stuffl ike autolens_Workspace". This lifts the PyPI release hold for the workspace merges in this session. CI must still pass. Work proceeds in an isolated feature/euclid-fields-api worktree; other claimed branches remain untouched. The pipeline migration is one coherent PR, followed by science deployment and the already-authorized submission; no new library API is needed.
