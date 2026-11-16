# autofit.campaign: submit stragglers and fills with no upstream dependency

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

`act submit --stage <s> --indices ...` always attaches `aftercorr:<upstream job>` (`autofit/campaign/submit.py` ~119-134). For fills and stragglers days after the upstream array finished, RAL may reject that dependency (`--kill-on-invalid-dep=yes`, purged job records after MinJobAge), so the job dies before it runs. The old Euclid fill scripts ran with no dependency.

1. Add a `--no-dependency` option (or drop the dependency automatically when the upstream job no longer exists in the scheduler) to `submit`; say which in the plan. The seed guards in each stage still stop a task whose upstream output is missing.
2. Tests with the fake scheduler.
3. Document it in the campaign README and `hpc/sync` help; note it in Mind `policy/hpc_ral.md` if that page describes fills.

Related: whether `aftercorr` fires at all on RAL slurmctld 22.05.9 is unproven; the first 10-tile pilot checks it (risk 1 of #133).
