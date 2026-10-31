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
