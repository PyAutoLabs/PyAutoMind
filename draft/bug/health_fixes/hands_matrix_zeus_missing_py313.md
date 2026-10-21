# Hands Python Version Matrix: autofit_workspace mcmc.py needs `zeus` on 3.13/3.14

Type: bug
Target: health_fixes
Themes:
- ci
- dependencies
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-10-21

## Context

Heart board finding `ci_status:PyAutoHands/workflows/Python Version Matrix` (red,
advisory — not a release gate). Run 39223656300 (2026-10-19): legs
`smoke_tests (3.13|3.14, autofit_workspace)` fail on

    scripts/searches/mcmc.py ... FAIL RuntimeError: Zeus requires importable module zeus:
    No module named 'zeus'

The 3.12 leg passes. Decide whether zeus is meant to be installed on 3.13+
(install-step gap in the matrix) or is unavailable there (then the script/search
should be skipped by the existing optional-dependency mechanism, not a workspace
guard).

Primary repository: @PyAutoHands (matrix install) or @PyAutoFit (optional-dep
handling). Downstream: @autofit_workspace.
