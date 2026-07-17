# Cold JAX compile research — autotuning is the cost; verdict 2

- **Issue:** autolens_profiling#74 (closed) · **PR:** autolens_profiling#76 (merged 2026-07-17)
- **Repos:** autolens_profiling (jax_compile/ additions: findings 6–8 + verdict 2, trace_profile.py, A100 matrix results)
- **Headline:** the pathological ~7m30 cold GPU compile IS XLA autotuning — hidden behind the pre-#128 XLA_FLAGS clobber (every prior "autotune off" run, incl. the 2026-07-15 "ruled out" A/B, silently ran autotune-on). Off: 17× cold probe (498s→29s), −40% cold full fit (2081s→1253s), bit-identical fixed-input logL, steady-eval parity (A100 matrix; 4800-eval fit faster end-to-end).
- **Closed directions:** tracing floor is jax-internal (58% jax / 34% stdlib / 7% autoarray — no PyAuto lever); cache-proliferation + pre-warming deprioritized (cold now ~seconds); upstream XLA report moot (fusion explained; HLO dump artifact retained, RAL job 330596).
- **Implementation:** PyAutoConf#131/#132 (merged same day) — wrapper defaults --xla_gpu_autotune_level=0, env-respecting.
- **Combined effect with #128:** worst-case first-fit UX ~70 min → ~30 s; restarts warm from disk.

## Original prompt

# Investigate ways to reduce the COLD JAX compile time itself

Type: research
Target: workspaces
Repos:
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Investigate ways to reduce the COLD JAX compile time itself (first fit on a machine, and each new model-structure/data-shape). Follow-up to autolens_profiling#71, which certified the persistent compilation cache for repeat fits but left the cold cost untouched: ~7m30 for the pathological GPU pixelized-gradient fusion, ~2min for CPU MGE value_and_grad, plus an uncacheable ~15s-2min Python tracing floor per process. Users iterating over model compositions pay one cold compile per distinct structure. Research in autolens_profiling (reuse jax_compile/probe.py). Leads: (1) XLA compile-speed knobs — compilation parallelism, optimization-level/fusion flags (e.g. priority-fusion off) measured on the 7m30 fusion; (2) produce the HLO artifact via jax.stages.Lowered.as_text() (xla_dump_to is INERT on jax 0.10.2) and understand/upstream-report WHY one input_reduce_fusion costs 7m30; (3) tracing-time reduction for deep structures (the uncacheable floor); (4) shape/graph canonicalization so more model variants share cache entries; (5) pre-warming strategies — background cache warmup on install/first-run, shared cluster cache dirs, jax.export/AOT serialization portability. Out of scope: restructuring likelihoods into piecewise jit stages (ruled out by #71).

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from user-intake -->
