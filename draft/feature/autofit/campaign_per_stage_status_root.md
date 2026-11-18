# autofit.campaign: per-stage status_root

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
Phase: 5e
Consequence: judge
Lane: any

Source: risks found in the review of PyAutoLabs/euclid_strong_lens_modeling_pipeline#133 (HPC campaign phase 5d, merged 2026-11-16); see Mind `complete/2026/11/hpc-campaign-p5d-pipeline-adoption.md`.

`status_root` is campaign-wide (`spec.py` ~14; `collector.py` ~178 scans `campaign.status_root`). The Euclid SED stage writes its `*.status.json` records under `output_sed/`, outside it, so `status` shows SED failures as a plain `failed` with no reason.

1. Allow an optional `status_root:` on each stage, defaulting to the campaign's; the collector scans each stage's root for that stage's tasks. `retro.py` (~101-151) takes the same per-stage root.
2. Tests, and the spec docstring.
3. Follow-up in the pipeline: set `status_root: output_sed` on the sed stage in `hpc/campaign/dr1.yaml` and drop the caveat from its header and README.
