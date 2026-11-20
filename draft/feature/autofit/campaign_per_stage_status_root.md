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
Witness: a campaign test with one stage whose `status_root:` differs from the campaign's (records written under e.g. `output_sed/`) shows `status` reporting that stage's failed task with its recorded reason instead of a bare `failed`, while a stage with no `status_root:` still reads the campaign-wide root and `retro.py` reads the same per-stage root; the existing campaign tests still pass (the pipeline `dr1.yaml` follow-up is out of this witness)
Lane: any

Source: risks found in the review of PyAutoLabs/euclid_strong_lens_modeling_pipeline#133 (HPC campaign phase 5d, merged 2026-11-16); see Mind `complete/2026/11/hpc-campaign-p5d-pipeline-adoption.md`.

`status_root` is campaign-wide (`spec.py` ~14; `collector.py` ~178 scans `campaign.status_root`). The Euclid SED stage writes its `*.status.json` records under `output_sed/`, outside it, so `status` shows SED failures as a plain `failed` with no reason.

1. Allow an optional `status_root:` on each stage, defaulting to the campaign's; the collector scans each stage's root for that stage's tasks. `retro.py` (~101-151) takes the same per-stage root.
2. Tests, and the spec docstring.
3. The pipeline follow-up (`status_root: output_sed` on the sed stage in `hpc/campaign/dr1.yaml`, caveat dropped) is its own prompt, `draft/feature/euclid/dr1_campaign_sed_status_root.md` (phase 5f, filed 2026-11-20). Do not edit the pipeline in this task.

## Answers from the human
- Q12 (2026-11-18, ruling claimed, shift 2026-11-18-pm): (a) — the gate is clear: compound-prior-model-json shipped (PyAutoFit#1783 merged 2026-11-18T17:40Z by human /prm) and its active.md claim is released; PyAutoFit is free for this task.
