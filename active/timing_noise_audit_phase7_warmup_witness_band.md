# Timing-noise audit phase 7: warm-up flag and witness band (fix phase 6, P3 + P5)

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- measurement-tools
Difficulty: moderate
Autonomy: supervised
Priority: high
Consequence: judge
Status: active
Filed: 2026-10-09
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Depends-on: active/timing_noise_audit_phase6_median_headline_gpu_marker.md (fix phase 5, PR #408, stacked)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request

2026-10-08 (chat): human authorized fix phases (5) and (6) of `results/notes/timing_noise_audit_2026_10.md`
under `--auto`, plus /prm of each. 2026-10-09 (chat): "finish up the timing task we were doing yesterday".

## Scope — section (b) item 6 of the audit note

- **P3:** rows after an unsettled warm-up ("NEVER SETTLED") are INCONCLUSIVE for any timing verdict
  that reads them (gates, overhead verdict, dashboard qualification).
- **P5:** `_production_config.witness_verdict` gains host class and an INCONCLUSIVE state off the
  reference host class (reuse `is_reference_host_class`); PASS/FAIL only on the reference class.
- **Witnesses:** synthetic flat / ramp / step sequences (existing T3 helper); laptop row → INCONCLUSIVE.
- No compute, no committed JSON rewritten; re-judge committed rows as facts in the audit note.
