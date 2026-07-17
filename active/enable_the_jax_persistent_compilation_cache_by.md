# Enable the JAX persistent compilation cache by default across the stack

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- workspaces
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Enable the JAX persistent compilation cache by default across the PyAuto stack. autolens_profiling#71 research verdict: the cache (jax_compilation_cache_dir) eliminates prohibitive XLA compile times at both scales measured — local CPU MGE value_and_grad 117s -> 2.3s warm (51x), A100 pixelized Nautilus end-to-end 5518s -> 937s (5.9x, a 1h10m single-fusion compile serializing into a 1.7MB entry). @PyAutoFit should enable jax_compilation_cache_dir by default when JAX is active (location e.g. ~/.cache/pyauto_jax or under the workspace output/, configurable via config/general.yaml; set jax_persistent_cache_min_compile_time_secs ~1s), with a log line on first-compile ('first run on this machine compiles for ~N min') for first-fit UX. Do NOT restructure likelihoods or samplers — ruled out by the research (batching structure adds no compile cost; the pathology is one op-pattern fusion, cacheable). Mirror any new config key into the workspaces per the workspace-config-override convention.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from user-intake -->
