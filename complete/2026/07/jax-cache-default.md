# JAX persistent compilation cache by default (+ XLA_FLAGS clobber fix)

- **Issue:** PyAutoConf#127 (closed) · **PR:** PyAutoConf#128 (merged 2026-07-17)
- **Repos:** PyAutoConf (`autoconf/jax_wrapper.py`, new `test_autoconf/test_jax_wrapper.py`)
- **What:** `JAX_COMPILATION_CACHE_DIR` defaults to `$XDG_CACHE_HOME/pyauto_jax` / `~/.cache/pyauto_jax` when unset (pre-set respected; empty string disables); `JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS` defaults to 1; first-compile UX log line. Bug fix: wrapper now APPENDS the constant_folding disable to existing `XLA_FLAGS` instead of overwriting (was silently discarding user/job flags — --xla_dump_to, autotune).
- **Why:** rollout of autolens_profiling#71 verdict — warm compiles for every user, no workspace config changes (env-based; target corrected autofit→PyAutoConf at start_dev).
- **Tests/verification:** 9 new env-handling tests (no JAX import); 147 autoconf; 1493 PyAutoFit downstream against the branch; fresh-process proof env-only path reaches jax.config and writes cache entries.
- **Heart:** RED at both PR-opens (5 pre-existing unrelated reasons), human-acked contemporaneously; merges human (2026-07-17).

## Original prompt

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
