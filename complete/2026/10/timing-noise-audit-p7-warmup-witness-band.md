Timing-noise audit phase 7 (fix phase 6 of the inventory): unsettled warm-ups and off-reference witness rows are INCONCLUSIVE. Issue autolens_profiling#362 stays open for phase 3b and leftovers.

**Shipped:** autolens_profiling#409 (merged 2026-10-09, 4db4d988, head 8ff9d8a4) via human `/prm`, stacked on #408.

- **P3:** `scripts/misc/likelihood_breakdown/warmup_gate.py::warmup_unsettled_reason` (missing `steady` counts as unsettled) turns P1 `abba_overhead_verdict` PASS/FAIL into INCONCLUSIVE (FAIL_GROSS still fires), makes P2 promotion INCONCLUSIVE with `warmup_unsettled_rows`, and leaves dashboard points unqualified (top-level and per-row `warmup`). The 3-vs-3 / 10 % / 12-call rule is kept with documented limits (false-unsettle 0 / 0.4 / 2.3 % at 5 / 10 / 15 % noise; a 3 %/call ramp settles 99 %).
- **P5:** `_production_config.witness_verdict(cold, instrument, host_class)` PASS/FAIL only on `is_reference_host_class`; else INCONCLUSIVE ("off reference host class (<class>)" / "untagged"). Band unchanged.
- **Re-judgement:** 0/28 committed warm-ups unsettled; all 8 committed P5 verdicts (laptop/untagged, 2026-09-08; 4 PASS rectangular, 4 FAIL Delaunay) → INCONCLUSIVE; no decision changed; dated note added to `results/notes/production_representative_cells.md`.
- **Witness:** flat/ramp/step sequences in `test_fixed_light_numba.py`, new `test_warmup_and_witness_band.py` (T10). Suite 1301 passed / 6 skipped. Review FINDINGS (3 low) fixed, re-review CLEAN. Audit note 35 rows: 26 SOUND / 5 FRAGILE / 4 UNSAFE-SILENT.

## Original prompt

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
Depends-on: complete/2026/10/timing-noise-audit-p6-median-headline-gpu-marker.md (fix phase 5, PR #408, merged 3ce8d789)
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
