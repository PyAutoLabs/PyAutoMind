# Interferometer streaming scaling: 1e8 RAL CPU row + A100 rows (2026.10.17.1)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Consequence: judge
Pulse task: `organs/PyAutoPulse/tasks/interferometer_streaming_scaling.md` (campaign interferometer)
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/368 (reopened; phase 1 merged as #375)

## Request (verbatim from the architect, human-authorized 2026-10-17 "Do all that, I authorise all")

A. Pulse task `organs/PyAutoPulse/tasks/interferometer_streaming_scaling.md` (issue autolens_profiling#368; wiki `lens/autolens_profiling/wiki/campaigns/interferometer_streaming.md`; results `results/streaming_scaling/`). Phase 1 CPU cells merged in #375 (2026-10-04). Now: the 1e8 CPU row (`--partition=ral` only, never gpu; CPU-only; memory recorded; euclid_dr1 arrays are running there so queueing is fine) and the A100 rows of the same table (`--gres=gpu:1`, `--exclusive` for timing legs so the node is not shared with the other A100 arm). Keep memory (peak RSS / device memory) and seconds in separate columns; compile separate from execution; streaming (array-free) vs in-memory side by side at matched hardware/precision/dataset/SHAs. Use the released 2026.10.17.1 stack.

Measurement only: no PyAutoArray edits (PyAutoArray#635 owns the interferometer library files).
