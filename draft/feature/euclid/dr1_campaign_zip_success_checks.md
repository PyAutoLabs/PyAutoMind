# dr1.yaml: add zip_complete success checks per stage now that a pattern is accepted

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: `python -m autofit.campaign validate hpc/campaign/dr1.yaml` passes against a PyAutoFit whose `zip_complete` accepts a glob or directory, with a `success: {zip_complete: ..., members: [files/samples_summary.json]}` check on `vis_lp`, `vis_pix` and `sed`; a `status` run over a small fixture tree with one `<hash>.zip` per finished lens marks those tasks succeeded and flags a lens with no zip, two zips, or a zip missing `files/samples_summary.json`; the "Success checks ... left out for now" comment in `dr1.yaml` is replaced by the checks
Review-minutes: 3
Unattended: ready
Lane: any
Blocked-by: draft/feature/autofit/campaign_zip_complete_pattern.md (`zip_complete` must accept a pattern in PyAutoFit first)
Epic: hpc-campaign
Phase: 5f
Filed: 2026-11-20

Source: step 4 of `draft/feature/autofit/campaign_zip_complete_pattern.md` (hpc-campaign phase 5e), split out on the human's request 2026-11-20 because it lands in a different repo from the PyAutoFit change. It is the revert path euclid_strong_lens_modeling_pipeline#133 names.

The DR1 campaign ships with no zip success checks. A fit's zip is named after its search identifier (`output/<sample>/<dataset>/initial_lens_model/vis_lp/<hash>.zip`), and `zip_complete` checked one fixed path, so turning the check on flagged every finished task. Until now the per-lens checks are the `STAGE_SETUP` seed guards and the fits' own status records.

1. Add `success: {zip_complete: <stage's fit directory>, members: [files/samples_summary.json]}` to each stage, in the form the PyAutoFit change documents (glob or directory). Use `output_sed/...` for `sed`.
2. Replace the "Success checks" comment block with a short note on what the checks catch. Keep the line about the seed guards being load-bearing after a purged dependency.
3. Update `hpc/README.md` where it describes per-lens success, if it does.
4. No RAL submit, for the same reason as `dr1_campaign_sed_status_root.md`: the shared RAL install is the human's call.
