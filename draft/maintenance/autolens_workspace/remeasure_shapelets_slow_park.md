# Re-measure the shapelets/modeling.py SLOW park (#586) under the harness — likely the XLA vmap hang, not slowness

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: `multi_galaxy/features/advanced/shapelets/modeling.py` timed 3× under `run_smoke.py` (profile_smoke) with and without `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`; the no_run entry is kept only if the median under the flag exceeds the smoke cap, else it is un-parked.
Filed: 2026-10-16
Dependency-resolved: complete/2026/10/python-matrix-harness.md (Hands PR #314 merged; per-script timeout restored)

## Finding

`smoke_tests.txt:47` comments out shapelets as SLOW (#586, 10-08). The 2026-10-16 matrix diagnosis showed every 6h matrix wedge in that script is the XLA Eigen thread-pool vmap hang (stack at jax_compile.py:249), the same misreading as the earlier `shared_preloads.py` "300s+" case. Re-measure before treating it as slow. Heart no_run_census lists it among the 1800 s release-cap entries.
