# JAX compile time is prohibitive for complex likelihood functions and JAX-native samplers

Type: research
Target: workspaces
Repos:
- autolens_profiling
- autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

JAX compile time is prohibitive for complex likelihood functions and JAX-native samplers.

We are now running into issues where for certain likelihood functions the time compiling them into JAX is prohibitive,
with a number of good examples in autolens_profiling.

In particular, this seems to have gotten even worse when we use JAX native samplers, like autolens_profiling/searches/multi_start_adam
and others in autolens_workspace_developer/searches_minimal (there are many). Maybe its jax.grad that is also compounding
the problem, with many samplers only use jax.jit.

This will become prohibitive for users, in some cases the compile time is longer than the sampling time.

Its time to research and asses what we can do about it:

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/eaea5567-d274-4de9-928f-921aa1a3c8c7/scratchpad/intake_jax_compile_time.md -->
