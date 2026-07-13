## assertions-fix
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1215
- completed: 2026-04-14
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1217
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/7

## Original prompt

Assertions are broken, which can be demonstrated by running the code @autofit_workspace_test/scripts/feature/assertion.py

Assertions are defined in the autofit source code @PyAutoFit/autofit/mapper/prior/arithmetic/assertion.py.

Inspect and compare both these files and then work on a way to fix the bug. Can you give me a plan of how you will do
this?