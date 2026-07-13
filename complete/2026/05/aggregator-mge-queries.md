## aggregator-mge-queries
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/130
- repos: autolens_workspace
- notes: |
    Cluster B of the recent release-prep triage. Two autolens aggregator
    tutorials (scripts/guides/results/aggregator/{queries,samples_via_aggregator}.py)
    crashed with `AttributeError: 'Model' object has no attribute 'sersic_index'`
    after PR #118 swapped the source bulge in _quick_fit.py from Sersic to
    MGE (al.model_util.mge_model_from). MGE is a Basis of fixed-sigma
    Gaussians whose only free parameters are the basis's shared centre +
    ell_comps — there is no sersic_index. Fix: queries.py Model Queries
    section now demos `lens.mass.einstein_radius < 1.5` (vs the Logic
    section's `& mass.einstein_radius > 1.0` — same parameter, different
    API features); samples_via_aggregator.py's two with_paths calls now
    use `lens.mass.centre.centre_0` as the second filter path (path was
    already used at line 533 of the same script, so known valid). Cluster A's
    fix to _quick_fit.py is the prerequisite that allowed these scripts
    to reach the failing line at all. autogalaxy versions of the same
    scripts are unaffected — that workspace's _quick_fit.py still uses
    Sersic + Exponential.
