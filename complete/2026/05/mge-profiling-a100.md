## mge-profiling-a100
- completed: 2026-05-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/56
- repos: autolens_workspace_developer (+ z_projects/profiling local-only)
- notes: |
    Follow-up to fft-mixed-precision-fix: extends profiling from
    consumer (RTX 2060 + i9-10885H) to A100 80GB and consolidates 10
    configs into canonical
    jax_profiling/results/jit/imaging/mge/ tracking dir.

    Tooling: z_projects/profiling/scripts/mge_profile.py (single-config
    step-by-step JIT profiler) + mge_aggregate.py (--ingest-pre-fix to
    convert /tmp logs, --consolidate-from to move HPC pulls, default to
    emit comparison.json+png) + 2 SLURM submits for A100 fp64+mp.

    Headline timings:
    - A100 fp64: 5.7 ms full pipeline / 2.4 ms vmap-per-call
    - A100 mp: 5.4 ms / 2.3 ms (5% noise — mp delivers ~zero on A100)
    - RTX 2060 fp64: 43.7 ms / 23.9 ms
    - RTX 2060 mp: 43.0 ms / 15.0 ms (37% vmap win on consumer GPU)
    - CPU fp64: 308 ms / 234 ms

    Key conclusion: use_mixed_precision is a consumer-GPU lever, not a
    production one. A100's 1:2 fp64:fp32 ratio means fp64 is not
    punitive on production hardware.

    Caveat surfaced (filed as separate follow-up): A100 JIT log_likelihood
    truncates to fp32 precision (-159734.59 vs eager fp64
    -159736.355042) — jax_enable_x64 likely not set in HPC PyAutoNSS
    venv. Doesn't affect timing, but worth investigating before
    quoting A100-served NSS / Nautilus log Z to high precision.
