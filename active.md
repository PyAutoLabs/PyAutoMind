# Active Tasks

## timing-noise-audit-p6-median-headline-gpu-marker
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase6_median_headline_gpu_marker.md
- session: Claude Code CLI (Opus 5.5 main + Opus worker under --auto, supervised)
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/408
- autonomy: --auto authorized 2026-10-08 for fix phases 5–6, resumed 2026-10-09 ("finish up the timing task"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p6-median-headline-gpu-marker
- repos:
  - autolens_profiling: feature/timing-noise-audit-p6-median-headline-gpu-marker
- tier: judge (human /prm)
- heart-ack: Heart STALE/monitoring-RED reason set of 2026-10-09 (Queue filing, PyAutoArray Tests, 3× workspace_test Smoke, CI wall-clock, autolens_inference/profiling red, worktree drift) human-acknowledged 2026-10-09 ("work on heart will fix later") for this task
- contract: Pulse v2 (profiling-summary@2) contract change approved by human 2026-10-09 if the median headline needs it

## timing-noise-audit-p7-warmup-witness-band
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase7_warmup_witness_band.md
- session: Claude Code CLI (Opus 5.5 main + Opus worker under --auto, supervised)
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/409 (stacked on #408 — merge #408 first)
- autonomy: --auto authorized 2026-10-08 for fix phases 5–6, resumed 2026-10-09; effective supervised (bug, Consequence judge); decide-and-flag at ship
- stacked-on: timing-noise-audit-p6-median-headline-gpu-marker (PR #408; claim guard reports that sibling's autolens_profiling claim — deliberate stack, merges after #408)
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p7-warmup-witness-band
- repos:
  - autolens_profiling: feature/timing-noise-audit-p7-warmup-witness-band
- tier: judge (human /prm)
- heart-ack: Heart reason set of 2026-10-09 human-acknowledged 2026-10-09 ("work on heart will fix later") for the timing-noise phase PRs

