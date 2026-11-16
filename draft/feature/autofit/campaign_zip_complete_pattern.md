# autofit.campaign: zip_complete success check accepts a glob pattern

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-16
Epic: hpc-campaign
Consequence: judge
Lane: any

Source: risks found in the review of PyAutoLabs/euclid_strong_lens_modeling_pipeline#133 (HPC campaign phase 5d, merged 2026-11-16); see Mind `complete/2026/11/hpc-campaign-p5d-pipeline-adoption.md`.

`success: {zip_complete: ...}` (`autofit/campaign/collector.py` ~105-108) opens one fixed path, `<zip_complete>.zip`. Real fit zips are named `<hash>.zip` (e.g. `output/<sample>/<tile>/initial_lens_model/vis_lp/<hash>.zip`), so turning the check on reports every finished task as failed. The Euclid DR1 campaign therefore ships with no zip success checks.

1. Let `zip_complete` take a glob (or a directory meaning "exactly one `*.zip` in it"); keep the fixed-path form working. Decide and document what happens with 0 or >1 matches (fail, naming the count).
2. `members:` checks apply to the matched zip.
3. Tests in the campaign test module; update the `spec.py` docstring example.
4. Follow-up in the pipeline: add `success: {zip_complete: ..., members: [files/samples_summary.json]}` per stage as in `hpc/campaign/dr1.yaml:54-55` (the revert path #133 names).
