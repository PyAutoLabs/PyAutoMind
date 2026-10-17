## point-source-image-gpu-admission
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/427
- issued: 2026-10-17
- prompt: active/point_source_image_plane_gpu_admission.md
- session: Claude Code (Opus 5.5 worker under Fable); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/point-source-image-gpu-admission
- repos:
  - autolens_profiling: feature/point-source-image-gpu-admission
- note: guard reported co-claims on autolens_profiling (hst-mge-pilot-qualification and the other parallel-array arms); proceeding as a human-authorised parallel-array arm on disjoint paths (results/breakdown/point_source_image, wiki point_source_gpu_breakdown, new submit). A100 job 412519 done.

## imaging-production-over-sampling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/430
- issued: 2026-10-17
- prompt: active/imaging_production_over_sampling_phase1.md
- session: Claude Code (Opus 5.5 worker under Fable, imaging over-sampling arm); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-shipped, awaiting-merge (2026-10-17: phase 1 PR open; CPU smoke 8/8 production runs OK; Heart readiness stale, not RED, no override; human /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/431
- classification: feature (workspace-only, phase 1 of PyAutoPulse task imaging_production_over_sampling), Consequence judge, Autonomy supervised; human-authorised 2026-10-17; CPU smoke only, no compute
- worktree: /home/jammy/Code/PyAutoLabs-wt/imaging-production-over-sampling
- claim-note: co-claims autolens_profiling with ral-route-constants-fft-levers, interferometer-streaming-memo-after, direct-conv-symmetric, hst-mge-pilot-qualification and ps-source-gradient-admission; this branch touches _profile_cli.py, _production_config.py, scripts/imaging/delaunay{,_nn}/likelihood_{runtime,breakdown}.py, wiki/campaigns/imaging_over_sampling.md and one wiki/index.md row only, disjoint from every co-claim diff
- repos:
  - autolens_profiling: feature/imaging-production-over-sampling

## delaunaynn-wide-row-overhead
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/629
- issued: 2026-10-17
- prompt: active/delaunaynn_wide_row_imaging_overhead.md
- session: Claude Code (Opus 5.5 worker under Fable, DelaunayNN imaging arm); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: library-shipped, awaiting-merge (2026-10-17: PR #637 open; RAL job 412525 A/B: DelaunayNN sub4 0.569→0.392 s, 2.20× Delaunay (was 3.00×; ~1.5× target not met — remaining cost is Sibson + curvature), sub2 1.75×; logL bit-identical; Heart STALE (no rehearsal), not RED; merge human /prm)
- classification: feature (library, PyAutoArray), Consequence judge (undeclared) — merge mode human /prm; plan approved 2026-10-15 (session 0b91c774), launch authorised by the human 2026-10-17 incl. RAL CPU acceptance timing; Pulse campaign delaunay-nn-cpu created by the architect (worker does not edit PyAutoPulse)
- worktree: /home/jammy/Code/PyAutoLabs-wt/delaunaynn-wide-row-overhead
- claim-note: co-claims PyAutoArray with direct-conv-symmetric (#636, interferometer files + inversion/factory.py + test_interferometer_numba.py); this task edits mappers/mapper_util.py, mappers/mapper_numba_util.py, mesh/interpolator/sibson.py + _sibson_numba.py and their tests only — disjoint paths, branched from main
- heart-red-override: 2026-10-15 (verbatim on #629); permitted commit, push, PR-open; merge separate
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/637
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/637
- repos:
  - PyAutoArray: feature/delaunaynn-wide-row-overhead

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
- status: workspace-dev
- classification: research (measurement only), Consequence judge, Autonomy supervised; human-authorized RAL compute 2026-10-17
- prompts: active/interferometer_streaming_ral_a100_rows.md, active/interferometer_nnls_memo_after_measurement.md
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-streaming-memo-after
- claim-note: overlaps hst-mge-pilot-qualification (#418 shipped, files scripts/misc/jax_compile/*.md only; no file overlap)
- repos:
  - autolens_profiling: feature/interferometer-streaming-memo-after

## direct-conv-symmetric
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/635
- issued: 2026-10-16
- prompt: active/direct_conv_symmetric_row_restriction.md
- status: workspace-shipped, awaiting-merge (2026-10-17: v3 shipped; RAL real-data witness PASS 1.49x/1.53x/1.58x, logL round-off; Heart STALE (no override); merge library-first: PyAutoArray#636 then autolens_profiling#425; Pulse Knowledge (h) + decision direct-conv-symmetric-gate drafted for the architect to persist)
- session: Claude Code CLI (Opus 5.5); session 13efb443, resumed 2026-10-17 by the Aris L2 worker (session 01QBeyBLN7ntDChx9v1fmt6M)
- worktree: ~/Code/PyAutoLabs-wt/direct-conv-symmetric (scripts/patches/logs in l2_scratch/, outside git)
- repos:
  - PyAutoArray: feature/direct-conv-symmetric
  - autolens_profiling: feature/direct-conv-symmetric
- classification: feature (PyAutoArray primary; write-up phase autolens_profiling + PyAutoPulse after library), Consequence glance, Autonomy supervised; serial numba only (human: Nautilus-level parallelism); campaign PyAutoPulse#62
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/636
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/636
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/425

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

## ps-source-gradient-admission
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/25
- issued: 2026-10-17
- prompt: active/point_source_gradient_admission.md
- session: Claude Code (Opus 5.5 worker under Fable); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-shipped, awaiting-merge
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_inference/pull/29
  - https://github.com/PyAutoLabs/autolens_profiling/pull/432
- next: human /prm #29 and #432 (judge); human admission decision on the gradient evidence; Pulse next/Knowledge draft handed to the parent session
- worktree: ~/Code/PyAutoLabs-wt/ps-source-gradient-admission
- repos:
  - autolens_inference: feature/ps-source-gradient-admission
  - autolens_profiling: feature/ps-source-gradient-admission
- companion-issue: https://github.com/PyAutoLabs/autolens_profiling/issues/428
- note: guard reported co-claims (hst-cleanslate-light-mode on autolens_inference, hst-mge-pilot-qualification on autolens_profiling); proceeding as a human-authorised parallel-array arm on disjoint paths
- summary: |
    Pulse point-source-source admission measurement: af.MultiStartAdam (forward gradient_mode via
    AnalysisPoint) on the L5 source-plane solved model, seeds 0-4, RAL CPU (ral) + A100 (exclusive),
    same-stack Nautilus control, private released-wheel venv 2026.10.17.1; runtime-cell median rows
    for #371. Judge tier, human /prm.
