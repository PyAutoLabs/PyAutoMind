## interferometer-streaming-scaling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/368 (CLOSED)
- completed: 2026-10-04
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/375 (MERGED)
- head: bec889905b3478c363124f42d4ff71e8c3f05e4d
- merge: 7f5a7a8b5e5692e6e3c41be7ff1d9cffb8a8bafe
- verification: confirmed PR state and merge SHA through GitHub; git proves the task head is an ancestor of origin/main. Published PR reports 1018 tests passed, 5 skipped, lint/layout/wiki/submit checks and script smoke passed; these historical tests were not rerun during cleanup.
- summary: CPU streaming scaling cells and evidence shipped, including accumulation to 5e7 visibilities, in-memory failures under a 10 GB cap and parity at 5e5 (1.2e-9 nats). Parity at 4e6 could not run because the in-memory arm OOMs.
- remainder: 1e8 accumulation was skipped; optional A100 measurements and transformer.image_from memory wall remain campaign work in PyAutoPulse/tasks/interferometer_streaming_scaling.md. This closes only the shipped phase, not the full campaign.
- cleanup: user explicitly authorized continuation and removal on 2026-10-05. All 202 ignored files and root setup files archived and SHA256-verified at /home/jammy/Code/PyAutoLabs/.worktree-archives/interferometer-streaming-scaling-2026-10-05/retained-files.tar.gz with manifest.json before removal. No uncommitted source changes existed.
- calibration: no shadow-row action recorded. The earlier session's human question about substantive pre-merge changes remains unanswered; removal authorization is not evidence for either answer. This cleanup uses --no-shadow-row and does not invent a calibration outcome.
- session: Codex; session ID unavailable. Cleanup only, not original implementation.

## Original prompt

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
