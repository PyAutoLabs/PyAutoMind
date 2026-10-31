# Results index skips campaign task records; batch wait loop keeps the fit's exit status

Merged 2026-10-31: PyAutoFit#1750 (issue PyAutoFit#1749). hpc-campaign phase 5a follow-up. Tier judge, human /prm, under the Heart RED development override the human extended on 2026-10-31.

- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1750

## What shipped
- `autofit/results/index.py`: `CAMPAIGN_TASKS_DIRNAME = ".campaign_tasks"` is added to `_SKIP_DIRS`, so the pending/failed task records the assistant template's `hpc/batch_cpu/stage` writes are no longer phantom results. The campaign collector (`scan_status`) walks for them itself.
- `autofit/campaign/scheduler/slurm.py`: the generated batch script's wait loop is now `while true; do status=0; wait "$child" || status=$?; kill -0 … || break; done`. Before, a fit that checkpointed on USR1 and then exited 0 was recorded as exit 138.
- Tests: an index test, plus two tests that run a generated batch script under bash with a real USR1. The USR1 test fails on the old loop. Full suite 4170 passed.

## Review
Independent review (a different model from the author's): CLEAN. The slurm tests ran 10× with no flakes; its test-runner nit is applied.

## Follow-on
After the release, rerun autolens_assistant#174's wiki-currency check (it audits released PyAutoFit for `autofit.campaign`), then /prm #174 and close out hpc-campaign p5a.

## Original prompt

Issued: 2026-10-31
Epic: hpc-campaign
Phase: 5a follow-up
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1749
Consequence: judge
Autonomy: human-required

# Results index skips campaign task records; batch wait loop keeps the fit's exit status

Original request (human, 2026-10-31): "start the PyAutoFit fix too" — the two PyAutoFit defects found by the
independent review of autolens_assistant#174 (hpc-campaign p5a); Heart RED development override extended to
this task by the human ("yes extend the override, go ahead").

@PyAutoFit:
1. `autofit/results/index.py` `_SKIP_DIRS = {"files", "image", INDEX_DIRNAME}` does not skip `.campaign_tasks`,
   so the shell task records the assistant's `hpc/batch_cpu/stage` writes under
   `output/.campaign_tasks/<campaign>/<stage>/<index>.status.json` (state `pending` / `failed`) show up as
   phantom results in `python -m autofit.results index`.
2. `autofit/campaign/scheduler/slurm.py` generated batch script: `until wait "$child"; do status=$?;
   kill -0 "$child" 2>/dev/null || break; done` leaves `status=138` when the pre-timeout USR1 interrupts the
   wait and the fit then checkpoints and exits 0 — a clean finish recorded as a failure. Fix:
   `while true; do status=0; wait "$child" || status=$?; kill -0 "$child" 2>/dev/null || break; done`
   (the same fix shipped in autolens_assistant 271f939). Tests for both, the wait-loop one driving a real
   USR1 against a generated script.
