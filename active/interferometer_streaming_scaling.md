# Campaign phase 1: interferometer streaming vs in-memory scaling (CPU)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- memory
Difficulty: small
Autonomy: supervised
Priority: high
Consequence: glance
Issued: 2026-10-04
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/368
Epic: streaming-visibilities

Contract: the PyAutoPulse task `organs/PyAutoPulse/tasks/interferometer_streaming_scaling.md`
(migrated from Mind on 2026-10-03; original text after its `---`). This prompt files phase 1
of it.

## Phase 1 scope (CPU only, local machine)

- `scripts/interferometer/streaming_scaling/{accumulate,in_memory,parity}.py` via `_profile_cli.py`,
  each measurement in a fresh child process under a 10 GB `RLIMIT_AS` cap and per-child timeout.
- accumulate: N_vis in {1e6, 4e6, 1.6e7} x chunk in {4096, 65536} (5e7/1e8 optional if wall allows);
  in_memory: up to the first failure under the cap; parity: log_evidence streamed vs in-memory at 4e6.
- `results/streaming_scaling/` JSON + PNG, `wiki/campaigns/interferometer_streaming.md`, `wiki/index.md`
  row, regenerated README and dashboard.
- Streaming epic phases 3-5 already shipped (PyAutoArray #589/#593/#601; released 2026.10.2.1), so the
  go/no-go framing is overtaken: the measurement is recorded as release evidence.

## Original request (verbatim)

> do the proposed priority order stuff, all of it
