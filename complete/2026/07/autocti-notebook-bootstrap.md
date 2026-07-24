## autocti-notebook-bootstrap
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/7
- completed: 2026-07-24
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/8; https://github.com/PyAutoLabs/autocti_workspace_test/pull/10
- summary: Replaced the obsolete `%matplotlib inline` / `pyprojroot` bootstrap in 79 maintained AutoCTI scripts with `autonerves.setup_notebook()`, regenerated all 79 paired notebooks through PyAutoHands, and removed the obsolete block from 26 maintained workspace-test scripts while preserving all 13 legacy occurrences. Script, notebook, and 3/3 CTI smoke validation passed; both pending-release PRs passed their gates and merged.
