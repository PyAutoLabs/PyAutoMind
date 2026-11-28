# dr1.yaml: give the sed stage its own status_root (output_sed/) and drop the known-gap caveat

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
Witness: `python -m autofit.campaign validate hpc/campaign/dr1.yaml` passes against a PyAutoFit that carries per-stage `status_root`, with `status_root: output_sed` on the `sed` stage; a `status` run over a small fixture tree (one SED task with a failed `*.status.json` under `output_sed/`) shows that task's recorded failure class instead of a plain `failed`; the "Known gap" comment in `dr1.yaml` and the `output_sed/` caveat in `hpc/README.md` step 7 are gone
Review-minutes: 3
Unattended: ready
Lane: any
Blocked-by: draft/feature/autofit/campaign_per_stage_status_root.md (per-stage `status_root:` must be merged into PyAutoFit first)
Epic: hpc-campaign
Phase: 5f
Filed: 2026-11-20

Source: step 3 of `draft/feature/autofit/campaign_per_stage_status_root.md` (hpc-campaign phase 5e), split out on the human's request 2026-11-20 because it lands in a different repo from the PyAutoFit change.

The DR1 campaign's `sed` stage writes into `output_sed/` (`PYAUTO_OUTPUT_DIR`), outside the campaign-wide `status_root: output`. `status` therefore sees SED only through the stage's shell record and sacct, and an SED failure shows as a plain `failed`. Risk 4 of euclid_strong_lens_modeling_pipeline#133 (human ruling 2026-11-16: acceptable until autofit.campaign has a per-stage root).

1. In `hpc/campaign/dr1.yaml`, set `status_root: output_sed` on the `sed` stage and delete the "Known gap" comment under the campaign-wide `status_root:`.
2. In `hpc/README.md` step 7, drop the paragraph saying `status` does not scan `output_sed/`.
3. No RAL submit. Running against the shared RAL install needs PyAutoFit main there, and pulling mains into `/mnt/ral/jnightin/PyAuto` during a campaign is the human's call (Mind `policy/hpc_ral.md`).

## Answers from the human
- Q21 (2026-11-26, ruling blocked-by, shift 2026-11-20-am): (a) wait for campaign_per_stage_status_root; blocker promoted to #1 of the autopilot queue.
- Q23 (2026-11-26, ruling claimed, shift 2026-11-23-am2): (a) resolved: sed-waveband-search-cap shipped 2026-11-24 and its euclid pipeline claim cleared.
