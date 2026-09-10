# jax_profiling scripts import jax before autolens, silently running in float32

Type: bug
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-10
Consequence: glance
Witness: for each swept script, importing it with no env var preset leaves jax.config.jax_enable_x64 True, where it is False on main.
Review-minutes: 3
Unattended: ready

33 scripts in @autolens_workspace_developer import jax before they import the PyAuto libraries. That defeats the config layer's jax_wrapper, which sets JAX_ENABLE_X64=True, XLA_FLAGS=--xla_disable_hlo_passes=constant_folding and JAX_COMPILATION_CACHE_DIR at import time - too late once JAX is already imported, exactly as its own docstring warns.

Measured 2026-09-09 while re-pinning the MGE HST regression constant (@autolens_workspace_developer issue 137, PR 138). In jax_profiling/jit/imaging/mge.py (jax at line 53, library import at line 61), a bare 'python mge.py' runs with jax_enable_x64=False and dtype float32: the JIT leg returns 27373.130859375 and the step-by-step leg 27373.1328125, agreeing with the eager NumPy value only to about 8e-7 - not the ~1e-11 the file's own comment asserts. Presetting JAX_ENABLE_X64=True restores float64 and 4e-16 agreement.

No pinned constant is wrong because of this: the eager reference is pure NumPy (xp=np) and identical either way, and PR 138's value was measured with x64 forced on. What is wrong is every JIT and vmap timing and precision claim these scripts print and write into jax_profiling/results/, unless the runner happened to preset the env var.

The fix is to move the jax import below the library import in the affected scripts, then confirm jax.config.jax_enable_x64 is True at runtime rather than assuming the reorder took. The full list of 33 is reproducible by comparing the first 'import jax' line number against the first library import line number in each file.

Witness: for each swept script, importing it with no env var preset leaves jax.config.jax_enable_x64 True, where it is False on main.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from user-intake -->

### The 33 files (2026-09-09, `main` @ 96937c9)

Reproduce with:

```bash
for f in $(grep -rl '^import jax' --include=*.py .); do
  jl=$(grep -n '^import jax' $f | head -1 | cut -d: -f1)
  al=$(grep -n '^import auto\(lens\|galaxy\|array\|fit\)' $f | head -1 | cut -d: -f1)
  [ -n "$jl" ] && [ -n "$al" ] && [ "$jl" -lt "$al" ] && echo "$f (jax:$jl before lib:$al)"
done
```

33 of the 60 files that import jax. They cluster in `jax_profiling/`
(gradient/, jit/, misc/, simulators/), plus `plotting_alignment/` (3),
`searches_minimal/` (3) and `legacy/quantity/` (1) — all written from the
same template, which is why the fix is a sweep rather than a one-file edit.

### Out of scope

- Re-measuring any pinned constant. The eager references are pure NumPy and
  unaffected; `jax_profiling/jit/imaging/mge.py` was already re-pinned under
  forced x64 in PR 138. If the swept scripts' *timings* should be re-recorded
  under float64, that is a profiling run, not this fix.
- The XLA:CPU vmap deadlock on 4-core machines
  (`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` works around it) — a
  container artefact noted in PR 138, not this bug.
