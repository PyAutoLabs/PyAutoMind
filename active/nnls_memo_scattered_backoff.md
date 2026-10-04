# fnnls warm-start memo: per-key back-off on scattered evaluation streams

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Consequence: glance
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/613

Library leg of the Pulse task `organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md`
(related autolens_profiling#332). Original request (verbatim):

> Execute Pulse task organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md
> (original contract after the `---`; related autolens_profiling#332): the fnnls warm-start memo slows
> scattered evaluation streams on interferometer CPU — add a guard.
