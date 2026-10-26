# Inference wall-time records: search.summary per-eval times and a profiling @3 join

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: likelihood-lifecycle
Status: formalised
Consequence: judge
Witness: dashboard/walltime_validation.json records carry likelihood_eval_s_search_summary and time_per_sample_s_search_summary (from the row or the backfill sidecar) and a profiling @3 match (profiling_record_id, profiling_per_call_s, size_match) wherever an exact key match exists; Pulse walltime-validation@1 validation still passes
Filed: 2026-10-26
Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/47

## Context
PR 2 of 3 for the Pulse timings redesign (draft/feature/pyautopulse/pulse_timings_dashboard_redesign.md):
producers first. Human (2026-10-26): "Replace these 3 coluns Predicted ms/eval Measured/predicted Parallel
efficiency with the likelihood evaluation time from search.summary and a measure likelihood per eval time for
search.summary make column headers clear." and "the column which pairs the run time based on 'Profiling Runtmie'
should be to the far left, after 'Model Variant'" and "for the inference results the profiling run time should be
clickable on each row to take you to the profiling results detailed page for that setup to establish the 'link'".
Today 0/56 wall-time records match a profiling record (v2-era matcher over a cached lens snapshot).
Heart RED override: live human 2026-10-26 "I authorize you to work and overrude heart red" (this task included).

## Plan (approved in chat "ok go", 2026-10-26)
- `scripts/misc/slam/_runner.py` `_stage_row`: parse the stage's search.summary → `search_summary:
  {log_likelihood_eval_s, time_per_sample_s, path}` (null + reason when absent).
- New `scripts/misc/tooling/search_summary_backfill.py --output-root output --write` →
  `catalogue/search_summary_backfill.json` keyed by row+stage for committed rows; refuses ambiguous hash dirs;
  lists rows without a summary.
- `export_inference_summary.py`: read row field else sidecar; emit `likelihood_eval_s_search_summary`,
  `time_per_sample_s_search_summary`; replace v2 `match_reference` with an @3 exact-key matcher (likelihood,
  instrument, setup_id, host_class, model_variant; current first) over Pulse's lens snapshot; emit
  `profiling_record_id`, `profiling_per_call_s`, `profiling_source_pixels`, `size_match`; keep
  `reference_runtime_record_id`/`predicted_ms_per_eval` from the same match; update limitations.
- Pulse validator must accept the additive fields (else stop and report; no Pulse edit here).
- Tests + regenerate dashboard/walltime_validation.json + lint.
