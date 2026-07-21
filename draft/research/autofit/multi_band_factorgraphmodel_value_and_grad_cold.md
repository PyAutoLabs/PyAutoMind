# Multi-band FactorGraphModel value_and_grad cold compile is unbounded on CPU (hours,

Type: research
Target: PyAutoFit
Repos:
- PyAutoFit
- autolens_profiling
- pyautonerves
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Multi-band FactorGraphModel value_and_grad cold compile is unbounded on CPU (hours, not the 117s single-band figure).

Type: research. Target: autolens_profiling. Repos: autolens_profiling, PyAutoFit. Difficulty: large. Autonomy: supervised. Priority: normal.

The autolens_profiling #71 -> #74 -> #77 compile-time arc certified SINGLE-band cold compile (CPU MGE value_and_grad 117s, A100 ~35s) and concluded "settings suffice, no source restructure." But those settings do NOT bound the MULTI-BAND af.FactorGraphModel gradient compile used by real multi-wavelength fits (multi/start_here.py: MGE lens + MGE source + Isothermal SIE + ExternalShear, fitted with MultiStartProdigy value_and_grad).

Reproducer: the 4-band COSMOS-Web Ring MGE maximum-likelihood fit. A single jit_call XLA compile exceeds ONE HOUR on CPU (observed >2h wall, ~1h inside one compile, no cache file written) with ALL shipped defaults confirmed live: persistent compile cache on (JAX_COMPILATION_CACHE_DIR set), --xla_disable_hlo_passes=constant_folding present, --xla_gpu_autotune_level=0 present, PyAutoNerves at latest. It is a cache MISS because the 4-band graph structure is new, so the cold compile cost is paid in full, ~30-60x the documented 117s single-band CPU figure.

Suspected drivers (all recorded in #71): (a) value_and_grad is 11-15x jit compile; (b) op-pattern-driven cost from HETEROGENEOUS per-band data shapes -- F115W/F150W at 0.03 arcsec/px (21821 masked px) vs F277W/F444W at 0.06 arcsec/px (5449 px) -- which prevents XLA from sharing fused sub-graphs across the four factors, welding four large distinct fusions into one jit_call; (c) the positive-only linear MGE inversion op pattern differentiated across 4 factors.

Investigate: (1) per-factor jit boundaries so each band compiles independently and caches separately; (2) shape canonicalization / padding short-wavelength bands to a common grid so all four factors share ONE fused kernel (also the immediate user-side workaround); (3) whether MultiStartProdigy batch_size (lax.map over starts) changes multi-band compile even though vmap batching was inert single-band in #71; (4) quantify cold vs warm compile+trace for the multi-band factor graph on CPU and A100, add a multi-band row to the jax_compile/ census. Deliverable: census row for multi-band value_and_grad plus either a productizable compile-reduction lever or a documented "GPU-only / same-shape-bands" verdict for N-band gradient fits. Out of scope: re-opening the single-band settings verdict from #71.

<!-- formalised by the Intake (Conception) Agent on 2026-07-21 from user-intake -->
