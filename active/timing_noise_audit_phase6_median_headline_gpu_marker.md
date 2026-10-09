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
