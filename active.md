
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
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/hst-cleanslate-light-mode
- repos:
  - autolens_inference: feature/hst-cleanslate-light-mode
- summary: |
    Phase 1 of Insight campaign hst-imaging-mass-samplers (clean slate, 2026-10-17): lens-light
    mode as a run variant (linear | fixed | both), schema v3 row provenance (library revisions,
    release pin, SLURM job id), --export-prepared under both modes, activate.sh library-root
    override for a pinned v2026.10.17.1 checkout, four clean-slate submits (A100 dense/sparse on
    gpu, jax_cpu dense/sparse on ral). No library change, no compute. Judge tier, human /prm.
