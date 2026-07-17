# Final compile-time census + remaining-speedup close-out

- **Issue:** autolens_profiling#77 (closed) · **PR:** autolens_profiling#78 (merged 2026-07-17)
- **Repos:** autolens_profiling (jax_compile/: census tables, export_probe.py, close-out section)
- **Census (defaults-live, #128+#132):** A100 worst cold cell ~35 s (mge vag: 6.8 trace + 27.9 compile; was ~70 min pre-defaults); warm 5–9 s ≈ all tracing. CPU reference in note (2× cross-day variance caveat).
- **Remaining levers closed:** jax.export RULED OUT on jax 0.10.2 (4 ms deserialize but ~156 s recompile EVERY process — exported-call compiles bypass the persistent cache); XLA parallel-codegen flags inconclusive, ceiling ~10 s once-per-machine; tracing floor jax-internal (58/34/7).
- **Arc verdict:** compile cost is seconds everywhere; further reduction is upstream JAX's. #71 → #74 → #77 complete.

## Original prompt

# Final compile-time census with the new defaults live (cache PyAutoConf#128

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Final compile-time census with the new defaults live (cache PyAutoConf#128 + autotune-off PyAutoConf#132), and a final analysis of where any remaining speedup would come. Census: cold (fresh cache) and warm compile+trace times for mge and pixelization across jit/vag (+laxmap_vag) on local CPU and the A100, exactly as users now experience them via autolens_profiling jax_compile/probe.py. Remaining-speedup research: (a) can jax.export/AOT serialization beat the uncacheable ~5-17s tracing floor for repeat runs; (b) do XLA compilation-parallelism flags cut the residual no-autotune compile (e.g. MGE vag 117s CPU / 29s A100); (c) quantify the warm floor (trace + cache read). Deliverable: census table + final addendum in jax_compile/README.md, follow-ups only if a lever is worth productizing.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from user-intake -->
