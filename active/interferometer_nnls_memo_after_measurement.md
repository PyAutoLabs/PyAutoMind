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
