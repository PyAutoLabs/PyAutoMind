## weak-likelihood-function
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/245
- completed: 2026-07-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/246 (merged)
- notes: Step 5 of the weak series (--auto supervised, same-session). scripts/weak/likelihood_function.py in the standard guide style; by-hand == FitWeak == AnalysisWeak to 8 d.p. (-104.74144953, chi2 437.510/400). Notes the gamma vs reduced-shear g distinction ahead of step 7. Catalogue regenerated in-branch (CI staleness leg green first run). Workspace-only PR, no library gate. lenstool-example's autolens_workspace claim had cleared by this task — no parallel worktree needed.
