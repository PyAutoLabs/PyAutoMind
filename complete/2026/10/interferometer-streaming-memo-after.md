## Summary
Two interferometer after-measurements on the released 2026.10.17.1 tag (autolens_profiling#435; issues #368 reopened for streaming phase 2 and #426 for the fnnls memo; private checkout `/mnt/ral/jnightin/profiling/PyAuto_2026.10.17.1_interf_meas`: Nerves 7f3055b, Fit 4b183e2, Array e59d5fa, Galaxy 35100de, Lens c90eceb). Measurement only; no library change.

**A. Streaming scaling phase 2** (jobs 412522 ral compute-10-5 Xeon 8490H 8 threads; 412523 euclid-ral-gpu-1 A100 80GB exclusive; fp64, persistent cache off, phase-1 synthetic dataset seed 1234, 400×400 mask, TransformerNUFFT, chunk 65536):
- Streamed 1e6/1.6e7/5e7/1e8 vis — CPU wall 15.4/117.6/368.1/707.5 s (compile ~3.2 s each, RSS 1.62–1.81 GB); A100 wall 6.6/27.5/79.2/157.3 s (compile ~3.6 s, device 1.48 GB). Rates 7.04 s per 1e6 (CPU), 1.53 s (A100); 2e8 ≈ 24 min / 5 min. Compile constant in N and chunk size, so the chunk-4096 penalty is execution, not recompilation (corrects phase 1).
- In memory: RAL CPU 10 GB cap fails at 2.5e5 (laptop failed at 1e6); uncapped 1.6e7 builds in 68.3 s at 119.3 GB peak RSS (~7.5 kB/vis; 2e8 ≈ 1.5 TB); A100 fails at 4e6 (46.2 GB vs 63.8 GB limit). Parity 1.2e-9 nats at 5e5 (both devices), 6.1e-8 at 4e6 (uncapped CPU).

**B. fnnls memo after-measurement** (job 412526, ral compute-10-2, load ~10, numba 1 thread, same cells/dataset as #332, six rounds, headline median(on)/median(off) with paired whole-round bootstrap 90 % CI): Delaunay iid at #332 flags 1.918 [1.887, 1.925] (#332: 2.17); 15 timed solves 1.018 [1.013, 1.023]; Delaunay walk 0.46; rect iid 0.887 (4 timed) / 0.987 (15); rect walk 0.15; FoM identical on/off. The regression at #332's stream length persists; on longer streams the bad seeds stop after ~10 solves, consistent with PyAutoArray#615's back-off. Reported as an after-measurement, not "fixed". Limits: rounds re-time one fixed iid seed (CI covers timing noise only); host class differs from #332.

Also in the PR: `--hardware` tag and compile/exec/device-memory fields on the streaming cells; `memo_clear()` resets #615's back-off state; the breakdown harness accepts PyAutoArray#632's `None` numba gate (job 412521 had failed on it).

**Human decision 2026-10-17 (Pulse chat):** interferometer CPU lane closed as exhaustive; GPU work filed as research with no source changes; campaign parked at knowledge-complete (PyAutoPulse#67). Not filed: the chunked `transformer.image_from` candidate, the Nautilus-replay memo witness, varied-seed rounds, optional 2e8 rows. Merged under human `/prm` after main merge + regeneration (head bfd95e5e). Heart STALE at ship, no override.

## Original prompt

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

## Original prompt (second, fnnls memo after-measurement)

# fnnls warm-start memo after-measurement on the #332 ALMA cells (2026.10.17.1)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Consequence: judge
Pulse task: `organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md` (library half PyAutoArray#613 fixed by #615, released 2026.10.7.1)

## Request (verbatim from the architect, human-authorized 2026-10-17 "Do all that, I authorise all")

B. Pulse task `tasks/interferometer_nnls_memo_scattered_stream_guard.md` (PyAutoArray#613 fixed by #615, released 2026.10.7.1). Owed: re-run the autolens_profiling#332 ALMA Delaunay memo on/off measurement that showed 2.17× slowdown on scattered streams, now on 2026.10.17.1, same cell/dataset/host class as the original, CPU `ral` partition, quiet core, memo on vs off, iid vs walk streams. Report the ratio with its interval using the repo's timing-audit conventions (median headline, repeats as #410–#412 define). Never "fixed" as a conclusion — report the after-measurement.

Measurement only: no PyAutoArray edits.
