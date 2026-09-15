# EP re-jit-compiles the vmapped likelihood per factor search until LLVM section memory…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- jax
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-15
Consequence: judge
Witness: an EP run over 25 AnalysisFactors with a JAX likelihood completes 12 factor_steps (300 factor searches) inside a fixed memory budget; RSS / XLA compile-cache size is flat across steps, not growing by one compiled executable per factor search.
Review-minutes: 20
Unattended: ready

Gates:
- https://github.com/PyAutoLabs/slope_hierarchy_scale/issues/3
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1631

## Report (slope_hierarchy_scale job 342410, RAL `ral` partition, 2026-09-09/10)

The N=25 EP arm ran on the JAX-on-CPU path with no pool (the PyAutoFit#1608 ruling):
each of the 25 AnalysisFactors is fitted by its own `af.Nautilus(number_of_cores=1)` under
`LaplaceOptimiser`, max_steps 12, SBATCH `--mem=64gb`, 10 kernel threads.

- 76 factor searches completed in ~11 h (22:25 → 09:16), i.e. ~3 EP steps of 25 factors.
- Every factor search logged "JAX jit compiling vectorized (vmap) likelihood function" — 76
  compiles, one per search (`grep -c 'jit compiling vectorized' output.342410_0.out` = 76).
  Each factor step builds a fresh Fitness / jitted function for the same 25 analyses, so
  nothing is reused across steps.
- At 09:15:58 the `.err` fills with `E … execution_engine.cc:54] LLVM compilation error:
  Cannot allocate memory` and `contiguous_section_memory_manager.cc:71] releaseMappedMemory
  failed`; factor dataset_24 then raises `jax.errors.JaxRuntimeError: INTERNAL: Failed to
  materialize symbols: { (<xla_jit_dylib_22>, { subtract_select_fusion }) }` and the EP
  optimiser skips it ("Factor dataset_24 raised on 1 consecutive step(s)"); the next factor
  search hits `LLVM ERROR: Unable to allocate section memory!` and the process aborts
  (core dumped) at 09:29:41.
- Logs: `slope_hierarchy_scale/hpc/batch_cpu/output/output.342410_0.out`,
  `hpc/batch_cpu/error/error.342410_0.err` (pulled to the local clone).

Hypothesis to test first: XLA's CPU JIT keeps every compiled executable's section memory
alive for the life of the process (the jitted callable is dropped but the dylib is not, or
the `jax_compile.py` wrapper caches on a key that includes the fresh Fitness object), so the
footprint grows by one executable per factor search. Candidates: reuse the compiled
likelihood across EP steps for the same analysis (cache on the analysis + model structure,
not the Fitness instance), or `jax.clear_caches()` / explicit executable release between
factor searches, with a test that asserts the compile count stays at one per factor over
several steps.

Not the same defect as PyAutoFit#1608 (pool hang) — that path is fixed; this is the memory
ceiling of the path we now take.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/32df3fc7-e0cc-4fc7-98c7-0f160dca158c/scratchpad/intake_ep_compile_memory.md -->
