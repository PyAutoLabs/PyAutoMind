## pyautoscientist-3b-smoke
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/51 (closed)
- completed: 2026-07-10
- prs: Heart#52 (reusable) + 9 conversions all merged 2026-07-10: autolens_workspace#259 (parity proof), autofit_workspace#84, autogalaxy_workspace#125, autofit_workspace_test#40, autogalaxy_workspace_test#68, autolens_workspace_test#160 (disjoint claim-override), HowToFit#14, HowToGalaxy#17, HowToLens#23
- summary: smoke_tests.yml generalised — Heart-owned reusable (chain input + repository_owner checkouts = zero instance facts, adopter forks reuse unmodified) + workspace-owned smoke_install.sh epilogues (exact pip parity incl. NSS git pins, jax<0.7 pins, autoconf force-reinstall quirks); all 18 matrix jobs green through the reusable; ~900 duplicated lines deleted; workflow NAME unchanged so Heart gating untouched. Follow-up: spawn stamps thin callers into the template family (spec-gated, now unblocked).
