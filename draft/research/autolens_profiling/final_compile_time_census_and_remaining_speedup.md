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
