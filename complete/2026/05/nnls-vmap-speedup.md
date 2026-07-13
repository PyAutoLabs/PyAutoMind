## nnls-vmap-speedup
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/307 (closed without library changes)
- completed: 2026-05-11
- repos: PyAutoArray, PyAutoConf (both — no commits, worktree branches deleted)
- outcome: |
    Closed without shipping. Investigation found the prompt's premise
    ("8.84x Delaunay vmap regression caused by NNLS") was a batch=3
    measurement artifact. At production batch=20 on A100:
      - Rect full pipeline = 11.2 ms/element (target was <=25 ms — already met)
      - Delaunay full pipeline = 69.5 ms/element (target was <=200 ms — already met)
      - NNLS = 6.2 ms/element = 9% of Delaunay (vmap regress = 0.40x, faster than single)
    Delaunay bottleneck is scipy.spatial.Delaunay via pure_callback
    (16.87 ms/element under sequential vmap = 99% of source-mapper sub-cost).
    Algorithm survey (PDIP/ADMM/FISTA): PDIP wins on correctness — ADMM/FISTA
    can't converge at production conditioning. Gradient audit: custom_vjp is
    lazy, no forward-only entry needed. MAX_ITER sweep: PDIP self-stops at
    15-20 iters, lowering MAX_ITER doesn't speed typical case.
- findings: ~/Code/PyAutoLabs/z_projects/profiling/FINDINGS_nnls_v2.md
- followup: pure-JAX Delaunay triangulation (highest-value lever for Delaunay
    science throughput; ~1.3x speedup vs current state from this alone,
    up to ~2x combined with optimising other inversion-setup work).
