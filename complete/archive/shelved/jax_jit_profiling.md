# We have lots of examples which profile how long JAX

Type: research
Target: autolens_workspace_developer
Themes:
- jax-compile
- profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: SHELVED 2026-09-04 — superseded by the compile-axis arc. Originally `draft/research/autolens_workspace_developer/jax_jit_profiling.md`.
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-05-10 (backfilled from git)

## Shelved 2026-09-04 — superseded, do NOT start dev on this prompt

This prompt's question — how long do our `jax.jit`s take to *compile*, and can we
make that faster — is the compile axis, and it was answered and shipped there.
`complete/2026/08/jax-compile-time-profiling-absorbed.md` records the absorption:
the speed-up leg closed with "settings suffice" (persistent cache 117.0 s → 2.3 s,
autotune-off 498 s → 29 s), the measurement leg was executed by the MultiStartProdigy
census (autolens_profiling#93), and the standing surface is the compile-warm-baseline
dashboard (`complete/2026/08/compile-warm-baseline-dashboard.md`, autolens_profiling#104
+ PyAutoBrain#220), with the arc record at
`complete/2026/08/profiling-agent-compile-axis-arc.md`. Nothing in this prompt is
unanswered by that arc. Archived rather than left as pickable backlog. The prompt
text is kept verbatim below for the record.


We have lots of examples which profile how long JAX jitted functions take to run on various datasets.

However, we have not profiled the time it takes to jit functions thesmevles, which can also impact a 
users experience and how long it takes for claude to test things s it runs.

Do an assessment of this for all jax.jit's in the autolens_Workspace, autolens_workspace_test
and autolens_workspace_developer and do an assessment of if we need to put in some JAX jits
in the source code to speed this up, or if there are other placdes or options or things we can
do to make this aspect of JAX also run fast.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
