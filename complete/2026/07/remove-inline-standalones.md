## remove-inline-standalones
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/160
- completed: 2026-07-24
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/161; https://github.com/PyAutoLabs/autolens_workspace/pull/337
- summary: Removed five inert standalone `%matplotlib inline` comments from the AutoGalaxy and AutoLens top-level script/notebook pairs and the unpaired AutoLens SLACS dataset helper. Generated notebooks parse, targeted smoke passed 19/19, both PRs passed CI and merged. An unrelated AutoLens full-generator partial-tree failure was restored before commit, leaving no residual churn. Four AutoLens occurrences embedded in old `pyprojroot` blocks remain intentionally outside this task; the dependent AutoCTI bootstrap sweep follows.
