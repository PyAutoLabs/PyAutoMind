# autofit.campaign: a fill or straggler submit with no dependency on the upstream array

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-18
Epic: hpc-campaign
Phase: 5e
Consequence: judge
Witness: a `FakeScheduler` test shows a fill/straggler submit in the new no-dependency mode emits an argv with no `--dependency`, the default submit still emits `--dependency=aftercorr:`/`afterok:` on the upstream array, and the no-dependency submit refuses — naming the stage — when one of the upstream stage's success-check outputs is missing; the existing campaign tests still pass and the mode is documented beside `resubmit --class`
Lane: any

Source: risks found in the review of PyAutoLabs/euclid_strong_lens_modeling_pipeline#133 (HPC campaign phase 5d, merged 2026-11-16); see Mind `complete/2026/11/hpc-campaign-p5d-pipeline-adoption.md`. The third PyAutoFit follow-up that review implied, beside `campaign_zip_complete_pattern.md` and `campaign_per_stage_status_root.md`. Phase 5e was set by the human's ruling on Q7 (2026-11-18).

Every fill or straggler submit in the `SlurmScheduler` path chains on the upstream array (`aftercorr` / `afterok`). A fill submitted after that array has finished, been cancelled or been purged from slurm's memory therefore waits on a dependency that never resolves, or is rejected. There is no route to resubmit the missing tasks of a stage on their own.

1. Add a no-dependency mode to the fill/straggler submit (a flag or an explicit `depends_on: none`), keeping the chained default.
2. Refuse it, naming the stage, when the upstream stage's outputs are not all present (the collector's success checks), so a fill never runs on a half-finished upstream.
3. Tests with `FakeScheduler`: the argv has no `--dependency` in the new mode and keeps it by default; a missing upstream output refuses.
4. Document it beside `resubmit --class` (propose-only rule F5 unchanged: the human approves every resubmit).

## Answers from the human
- Q11 (2026-11-18, ruling claimed, shift 2026-11-18-pm): (a) — the gate is clear: compound-prior-model-json shipped (PyAutoFit#1783 merged 2026-11-18T17:40Z by human /prm) and its active.md claim is released; PyAutoFit is free for this task.
