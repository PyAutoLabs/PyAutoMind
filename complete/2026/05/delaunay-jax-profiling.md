## delaunay-jax-profiling
- completed: 2026-05-06
- repos: autolens_workspace_developer
- notes: |
    Retroactively logged via 2026-05-06 hygiene scan. Original prompt
    `autolens_workspace_developer/imaging_delaunay_jax_profiling.md` asked for
    `jax_profiling/imaging/delaunay.py` to be aligned with the current pytree /
    register_model approach used by `mge.py` and `pixelization.py`. Verified
    done: `jax_profiling/jit/imaging/delaunay.py` now mirrors the sibling
    Timer + register_model + xp pattern. Original issue/PR not tracked.
