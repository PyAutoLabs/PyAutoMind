
## direct-conv-symmetric
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/635
- issued: 2026-10-16
- prompt: active/direct_conv_symmetric_row_restriction.md
- status: library-dev — PAUSED 2026-10-16 by the human; uncommitted v2 (+v3 in flight: ymin ordering, gate 0.7, human-approved). Resume from the checkpoint comment https://github.com/PyAutoLabs/PyAutoArray/issues/635#issuecomment-6219325769 ; next = RAL real-data witness (staged /mnt/ral/jnightin/scratch/aris_l2_20261016), ship, then write-up phase (autolens_profiling note + Pulse Knowledge/decision)
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/direct-conv-symmetric (scripts/patches/logs in l2_scratch/, outside git)
- repos:
  - PyAutoArray: feature/direct-conv-symmetric
- classification: feature (PyAutoArray primary; write-up phase autolens_profiling + PyAutoPulse after library), Consequence glance, Autonomy supervised; serial numba only (human: Nautilus-level parallelism); campaign PyAutoPulse#62
