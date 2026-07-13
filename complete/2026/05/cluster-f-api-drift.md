## cluster-f-api-drift
- issue: N/A (triage cluster F sweep, run 2026-04-29T14-48-47Z)
- completed: 2026-05-02
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/491
- workspace-prs: https://github.com/PyAutoLabs/autofit_workspace/pull/50, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/54, https://github.com/PyAutoLabs/autolens_workspace/pull/117
- repos: PyAutoLens, autofit_workspace, autogalaxy_workspace, autolens_workspace
- notes: 9 Cluster F triage failures resolved in 8 file changes across 4 PRs. Item 4 (double_einstein_ring `FitException`) root-caused to a swallowed `IndexError` at `PyAutoLens/autolens/analysis/result.py:445` — `plane_indexes_with_pixelizations[plane_index]` should be `.index(plane_index)`. The library bug was latent: it only triggered when not every plane had a pixelization. Items 1, 8 added back functionality removed by PyAutoArray plotter-class deletion (`b491a119`) and missing simulator outputs. Items 7, 9 fixed wrong/missing auto-sim blocks in consumer scripts — the auto-sim pattern is more reliable than ad-hoc dataset preparation. Items 2, 3, 5 were one-line script bugs: duplicate `source` kwarg, prior bound under zero-luminosity test mode, and an autoarray wrapper escaping a `@jax.jit` boundary.
