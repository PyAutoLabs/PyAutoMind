## ral-route-constants-fft-levers
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/429
- issued: 2026-10-17
- prompt: active/ral_route_constants_fft_levers.md
- session: Claude Code (Opus 5.5 worker under Fable, Aris arm phase 2); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-dev
- classification: research (measurement; library change only if part A supports one), Consequence judge, Autonomy supervised; human-authorized RAL A100 + CPU compute 2026-10-17; campaign PyAutoPulse#62
- worktree: /home/jammy/Code/PyAutoLabs-wt/ral-route-constants-fft-levers
- claim-note: co-claims autolens_profiling with hst-mge-pilot-qualification (#418, scripts/misc/jax_compile/* only), direct-conv-symmetric (#425 note), interferometer-streaming-memo-after and ps-source-gradient-admission; new files only, disjoint paths
- repos:
  - autolens_profiling: feature/ral-route-constants-fft-levers


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

## hst-cleanslate-light-mode
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/24
- issued: 2026-10-17
- session: Claude Code (Fable 5.1); https://claude.ai/code/session_015KxQzEhy93XdCA9cRZ8Ry6
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/26
- next: human /prm of #26 (judge tier); expect a trivial dashboard/*.json conflict with #23 (regenerate). Phase 2 (create pin dir on RAL, submit) is separately authorised.
- worktree: ~/Code/PyAutoLabs-wt/hst-cleanslate-light-mode
- repos:
  - autolens_inference: feature/hst-cleanslate-light-mode
- summary: |
    Phase 1 of Insight campaign hst-imaging-mass-samplers (clean slate, 2026-10-17): lens-light
    mode as a run variant (linear | fixed | both), schema v3 row provenance (library revisions,
    release pin, SLURM job id), --export-prepared under both modes, activate.sh library-root
    override for a pinned v2026.10.17.1 checkout, four clean-slate submits (A100 dense/sparse on
    gpu, jax_cpu dense/sparse on ral). No library change, no compute. Judge tier, human /prm.

## ps-source-gradient-admission
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/25
- issued: 2026-10-17
- prompt: active/point_source_gradient_admission.md
- session: Claude Code (Opus 5.5 worker under Fable); https://claude.ai/code/session_01QBeyBLN7ntDChx9v1fmt6M
- status: workspace-dev
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
