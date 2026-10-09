Timing-noise audit phase 6 (fix phase 5 of the inventory): the single-jit headline gains a steady median and the "GPU-only" marker needs a qualified timeout. Issue autolens_profiling#362 stays open for phase 3b and leftovers.

**Shipped:** autolens_profiling#408 (merged 2026-10-09, 3ce8d789, head 5788b960) via human `/prm`.

- **P8:** shared `timing.headline_steady_median` called by 11 runtime cells after the legacy block; writes `full_pipeline_single_jit_median` (s), `_median_ms`, `_p10_ms`, `_p90_ms`, `_median_protocol` beside the unchanged block mean. Timed calls = 30 s / block mean clamped to [20, 200]; no median above a 2 s block mean. `build_dashboard` headlines the median ("steady median") where present; drift compares like estimators only — a mismatch is `estimator-mismatch`, published `insufficient`.
- **P9:** `sweep.py` timeouts write `verdict: INCONCLUSIVE` + host, loads, timeout, elapsed (`cpu_unusable` kept); `build_dashboard.marker_verdict` renders GPU-only only when `qualify` passes; `--skip-existing` re-measures unqualified markers.
- **Re-judgement:** no committed row has a median, no headline/badge changed; all 4 committed `.unusable.json` are laptop/no-load → inconclusive; ALMA `local_cpu_fp64` page entry GPU-only → "did not finish (inconclusive)".
- **Pulse:** no profiling-summary@2 field changed (median maps to the existing `single_jit_median` metric).
- **Witness:** `test_headline_estimator_and_marker.py` (T9): block mean 2.40× vs median 1.00× on an injected transient. Suite 1260 passed / 6 skipped. Review FINDINGS (3 low) fixed in 69e19ee, re-review CLEAN. Heart reason set human-acknowledged 2026-10-09.
- **Leftovers:** README runtime table on the old headline; no producer writes `single_jit_repeats`; `wall/rates.py` omits the median calls.

## Original prompt

# Timing-noise audit phase 6: median headline estimator and GPU-only marker (fix phase 5, P8 + P9)

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
Depends-on: complete/2026/10/timing-noise-audit-p5-round-bootstrap.md (fix phase 4, PR #407, merged 8be806cc)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request

2026-10-08 (chat): human authorized fix phases (5) and (6) of `results/notes/timing_noise_audit_2026_10.md`
under `--auto`, plus /prm of each. 2026-10-09 (chat): "finish up the timing task we were doing yesterday".

## Scope — section (b) item 5 of the audit note

- **P8:** opt every runtime cell that reports the `jit_profile` block-mean headline into
  `steady_median_profile` beside the legacy block mean (keys kept for continuity); the dashboard reads
  the median where present, else the legacy value, and labels which estimator it shows.
- **P9:** a `--per-run-timeout` timeout records INCONCLUSIVE / "timed out on host X at load Y" and is
  re-measured before it is ever rendered as GPU-only; a marker whose load exceeds the cap never renders
  as GPU-only; `--skip-existing` does not honour an unqualified marker.
- **Witnesses:** injected-clock transient (T4 pattern) where the block mean moves 2.4x and the median
  does not; a high-load marker is not rendered GPU-only.
- No compute launched, no committed measurement JSON rewritten; re-judge committed rows as facts in the
  audit note. Check whether `build_catalogue.py` (Pulse v2 feed) reads the headline — if a v2 field
  changes, stop and flag (Pulse contract).
