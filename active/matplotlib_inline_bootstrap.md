# Remove obsolete AutoCTI notebook bootstrap

Type: refactor
Target: autocti_workspace
Repos:
- @autocti_workspace
- @autocti_workspace_test
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Depends on:
- `complete/2026/07/remove-inline-standalones.md`

Remove or replace the obsolete `%matplotlib inline` plus `pyprojroot`
bootstrap throughout maintained AutoCTI workspace scripts and notebooks and
throughout non-legacy AutoCTI workspace-test scripts. Preserve
`autocti_workspace_test/legacy/` verbatim.

Use the current workspace notebook-setup convention where working-directory
setup remains necessary. Treat scripts as the authored source and regenerate
or otherwise verify paired notebooks through supported workspace tooling.
Validate notebook JSON and assert that no non-legacy AutoCTI `.py` or `.ipynb`
file retains `%matplotlib inline` or the old `pyprojroot` bootstrap.

## Original request (verbatim)

> ok, lets get rid of the five standalones and then tackle all the CTI stuff
