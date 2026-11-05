# Write `compile_repeats` from autolens_profiling's jax_compile tooling so compile drift can be repeat-summarised

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- measurement-tools
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Filed: 2026-11-05
Consequence: judge
Witness: a jax_compile record written by the tooling carries an integer `compile_repeats` (the number of compile timings its `compile_s` summarises); the Brain profiling conductor reports a drift between two such records with `comparison: repeat-summarised` instead of the single-sample caveat.
Review-minutes: 5
Unattended: ready

PyAutoBrain#588 (record `complete/2026/11/compile-drift-single-sample.md`) made the profiling
conductor label every compile-drift row `single-sample` unless both endpoints carry
`compile_repeats >= 2` (P7's `single_jit_repeats` rule). No producer writes the field yet, so
every real drift today is reported as a gross single-sample flag. Decide whether the jax_compile
scripts should time N cold compiles (cost: N× compile time per cell) and record N plus the summary
estimator; if repeats are too expensive, record `compile_repeats: 1` explicitly so the caveat is
evidence-based rather than defaulted.

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/d_compile_repeats.md -->
