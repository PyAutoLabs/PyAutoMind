## point-source-image-gpu-admission
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/427
- issued: 2026-10-17
- prompt: active/point_source_image_plane_gpu_admission.md
- session: Claude Code (Opus 5.5 worker under Fable); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/434
- next: human /prm #434 (judge); human admission decision on the job-412519 evidence; Pulse next/Knowledge draft handed to the parent session
- worktree: ~/Code/PyAutoLabs-wt/point-source-image-gpu-admission
- repos:
  - autolens_profiling: feature/point-source-image-gpu-admission
- note: guard reported co-claims on autolens_profiling (hst-mge-pilot-qualification and the other parallel-array arms); proceeding as a human-authorised parallel-array arm on disjoint paths (results/breakdown/point_source_image, wiki point_source_gpu_breakdown, new submit). A100 job 412519 done.

## ral-route-constants-fft-levers
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/429
- issued: 2026-10-17
- prompt: active/ral_route_constants_fft_levers.md
- session: Claude Code (Opus 5.5 worker under Fable, Aris arm phase 2); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-shipped, awaiting-merge (2026-10-17: A100 witness job 412515; pruned FFT saves 19.4/22.1/29.7% of F at alma/alma_high/jvla, F rel <= 1.7e-15, FoM unchanged; jvla coarser pixel scale fails 0.5-nat bar (+1,310..+2,757 nats). Part A dropped: CPU lane closed by the human 2026-10-17, no CPU jobs. Heart STALE (no override). Judge tier, human /prm)
- classification: research (measurement; library change only if part A supports one), Consequence judge, Autonomy supervised; human-authorized RAL A100 + CPU compute 2026-10-17; campaign PyAutoPulse#62
- worktree: /home/jammy/Code/PyAutoLabs-wt/ral-route-constants-fft-levers
- claim-note: co-claims autolens_profiling with hst-mge-pilot-qualification (#418, scripts/misc/jax_compile/* only), direct-conv-symmetric (#425 note), interferometer-streaming-memo-after and ps-source-gradient-admission; new files only, disjoint paths
- repos:
  - autolens_profiling: feature/ral-route-constants-fft-levers
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/433

## interferometer-streaming-memo-after
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/368 (reopened, phase 2 RAL CPU 1e8 + A100 rows); https://github.com/PyAutoLabs/autolens_profiling/issues/426 (fnnls memo after-measurement)
- issued: 2026-10-17
- session: Claude Code (Opus worker, arm 4 of 4; https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M)
- status: workspace-shipped, awaiting-merge (human /prm; Consequence judge)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/435
- heart-at-ship: STALE — "release validation incomplete: no rehearsal for current source" (no override)
- ral: jobs 412522 (CPU), 412523 (A100), 412526 (memo); private libs /mnt/ral/jnightin/profiling/PyAuto_2026.10.17.1_interf_meas; RAL wt /mnt/ral/jnightin/profiling/autolens_profiling_wt/interferometer-streaming-memo-after
- next: /prm #435, then close #368 and #426; Pulse next/Knowledge drafts are with the architect
- classification: research (measurement only), Consequence judge, Autonomy supervised; human-authorized RAL compute 2026-10-17
- prompts: active/interferometer_streaming_ral_a100_rows.md, active/interferometer_nnls_memo_after_measurement.md
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-streaming-memo-after
- claim-note: overlaps hst-mge-pilot-qualification (#418 shipped, files scripts/misc/jax_compile/*.md only; no file overlap)
- repos:
  - autolens_profiling: feature/interferometer-streaming-memo-after

## hst-mge-pilot-qualification
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
- issued: 2026-10-13
- session: Codex; session ID unavailable
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/418
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/hst-mge-pilot-qualification
- next: Review and merge #418; independently validated witness implementation, coefficient tolerances and production collection remain separate pending work.
- repos:
  - autolens_profiling: feature/hst-mge-pilot-qualification
