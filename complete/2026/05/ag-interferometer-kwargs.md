## ag-interferometer-kwargs
- issue: none — direct follow-up to point-source-jax-viz; user-approved file-level safety alongside in-flight jax-interp-2d / nfw-jax-port worktrees
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/399
- repos: PyAutoGalaxy
- notes: |
    Final piece of the kwargs-gap series. Added **kwargs passthrough to
    ag.AnalysisInterferometer.__init__ (2-line change), mirroring the
    earlier al.AnalysisInterferometer (#500) and al.AnalysisPoint (#506)
    fixes. test_autogalaxy/interferometer/ 37/37 pass.

    Coexisted on PyAutoGalaxy with two other in-flight worktrees
    (jax-interp-2d — actually merged via #398 before this PR; nfw-jax-port
    — mass profile work). User confirmed file-level safety: this PR
    touched autogalaxy/interferometer/model/analysis.py only, well away
    from mass-profile code. Parallel worktrees on different feature
    branches are exactly what the worktree flow is designed to handle;
    the conflict check is a soft policy guard, not a physical lock.

    With this PR, all four Analysis subclasses across PyAutoLens +
    PyAutoGalaxy now accept use_jax_for_visualization without TypeError.
    Phase 1C of the JAX visualization roadmap is unblocked from a
    library-API perspective.
