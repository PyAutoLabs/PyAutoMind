# fnnls warm-start memo: per-key back-off on scattered evaluation streams

Completed 2026-10-07. Merged PyAutoArray#615 (head e54123b4, merge 58bdda0a)
by the human; head verified an ancestor of origin/main. Issue PyAutoArray#613 closed.

Per-key exponential back-off for the fnnls warm-start memo after consecutive
fallbacks, so scattered (iid) evaluation streams stop paying for a bad seed every
other solve; local-walk behaviour unchanged. Library leg of the Pulse task
organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md.

Validation: 1975 passed, 4 xfailed; local solver-only witness (synthetic n=576:
iid on/off 1.49x -> 1.17x, walk 0.18x unchanged, iid->walk recovery 0.69x).
Heart YELLOW acknowledged by the human at ship. No workspace impact.

Follow-ups (not merge gates, on #613): real Nautilus-replay witness (e.g. the
autolens_profiling#332 ALMA Delaunay case); autolens_profiling harnesses should
call nnls_memo.memo_clear() instead of clearing the private memo dict.


## Original prompt

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
