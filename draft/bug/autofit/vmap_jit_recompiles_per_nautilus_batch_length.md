# vmap(jit) likelihood recompiles once per distinct Nautilus batch length

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- jax
- nautilus
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: a Nautilus fit with use_jax_vmap=True over a likelihood whose call sites arrive in varying batch lengths (e.g. sample_shell tails) compiles the vectorised likelihood a bounded number of times (one, or one per padding bucket), not once per distinct batch length; a compile-count probe over one search stays flat after warm-up.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-17

Follow-up split out of PyAutoFit#1631 (release each EP factor search's internals
so JAX executables are collectable). That fix makes the executables collectable
when a search ends; this prompt is about how many are compiled during a search.

`Fitness.call_wrap` promotes a `(d,)` parameter vector to `(1, d)` and hands
the batch to `jax.vmap(jax.jit(call))` (`autofit/non_linear/fitness.py`,
`_vmap`). XLA specialises on the leading batch dimension, so every distinct
Nautilus batch length (`n_batch` in the steady state, but shorter tails from
`sample_shell` and the final exploration phase) triggers another compile of the
same function. Only the first compile is logged ("JAX jit compiling vectorized
(vmap) likelihood function"), so the extra executables are invisible in the
run log; they still cost compile time and, before #1631, section memory.

Proposal: pad or bucket the leading dimension to a small fixed set of sizes
(powers of two up to `n_batch`, or a single `n_batch` pad) and mask the
figure of merit for the padded rows so results are unchanged. Instrument with
a compile-count probe (jax's compilation cache hooks, or a counter on the
wrapped function) and assert it in a test on a synthetic search that feeds
varying batch lengths; report the before/after count and the wall-clock delta
on the 5-factor JAX witness from #1631.
