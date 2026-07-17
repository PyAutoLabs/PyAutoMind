# JAX compile-time research — settings suffice, no restructure

- **Issue:** autolens_profiling#71 (closed) · **PR:** autolens_profiling#73 (merged 2026-07-17)
- **Repos:** autolens_profiling (additive `jax_compile/`: probe.py, README research note, results)
- **Question:** jit boundaries inside the source to break up compilation, vs settings/small changes?
- **Verdict:** settings suffice. Persistent compilation cache certified both scales (local MGE vag 117s→2.3s, 51×; A100 pixelized Nautilus end-to-end 5518s→937s, 5.9× — the 1h10m input_reduce_fusion compile serializes to 1.7MB). lax.map/vmap batching exonerated by controlled A/B (7m23s vs 7m24s identical). Differentiation is 11–15× jit's compile (inherent to AD). Compile cost is op-pattern-driven, not complexity-driven. Piecewise source jit-boundaries rejected by evidence.
- **Key traps recorded:** XLA compiles on HOST CPUs — compile timings load-sensitive even for GPU jobs (morning matrix wrong by up to 7×); slow-compile alarm banner re-fires during ONE compile; autoconf jax_wrapper CLOBBERED XLA_FLAGS (fixed in PyAutoConf#128) — made dump flags look inert and invalidated the 2026-07-15 "autotune ruled out" A/B (now unproven).
- **Follow-ups:** cache-by-default SHIPPED same day (PyAutoConf#127/#128); cold-compile reduction research filed (draft/research/workspaces/investigate_ways_to_reduce_the_cold_jax.md); HLO artifact un-parked (re-run after #128).
- **Provenance:** started by bg session b44b0e0f 2026-07-16 (dup issue #72 filed by evening session, closed); resumed and completed by evening/morning session 2026-07-16/17.

## Original prompt

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

## Core question (user clarification, 2026-07-16)

Do we need to put JAX compiles in the source code to break up compilation (e.g. jit
boundaries inside the likelihood so it compiles in pieces), or can we speed things up
via smaller source code changes or JAX settings (persistent compilation cache,
donate/static argnums, avoiding closure cache-busts, compiler flags)? We may need to
think hard about how JAX is implemented throughout the source code — the answer decides
whether this stays a research note or spawns a library-wide restructuring task.

Known prior evidence to start from:
- Pixelized gradient sampling on the A100: compile dominates (~453s per latent sample).
- Fresh-closure-per-call JIT cache-busting is a known trap in this stack; cache
  (closure, solver) on the instance.
- JAX-native samplers (multi_start_adam etc.) appear worse than jit-only samplers —
  test whether jax.grad/value_and_grad compounds compile cost vs plain jax.jit.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/eaea5567-d274-4de9-928f-921aa1a3c8c7/scratchpad/intake_jax_compile_time.md -->
