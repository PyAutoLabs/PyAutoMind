# Regenerate setup_notebook-drifted notebooks in autogalaxy/autofit/HowToFit workspaces

Themes:
- notebooks
- hygiene
Difficulty: small
Autonomy: supervised
Priority: low
Filed: 2026-08-07 (backfilled from git)

## The problem

The same generator/notebook drift fixed in @autolens_workspace (#480/#481 —
committed notebooks carry the commented `# from auto* import setup_notebook;
setup_notebook()` form while PyAutoHands regeneration uncomments it, so the
notebooks never call it) exists in three sibling repos. Measured 2026-08-07 by
clean-tree `generate.py` dry-runs with PyAutoHands `2a4fb11`:

| Repo | Modified notebooks | setup_notebook flips | Other diff lines |
|---|---|---|---|
| @autogalaxy_workspace | 127 | 126 | **6 — audit before committing** |
| @autofit_workspace | 31 | 32 | 0 |
| @HowToFit | 13 | 13 | 0 |
| @HowToLens | 0 | — | — |
| @HowToGalaxy | 0 | — | — |

## Proposed fix

Mirror of autolens_workspace#481: one dedicated regeneration sweep per repo
(three PRs under this one task, mge-sigma phase-2 precedent), committing the
clean-main `generate.py <project>` notebook diff. In autogalaxy_workspace,
audit the 6 non-flip diff lines first — in autolens_workspace the analogous
extras were harmless JSON-indent normalizations of hand-edited lines, but
verify before committing.

## Verification (per repo)

- Second regeneration on the swept tree is a no-op.
- No diff content beyond the setup_notebook flip + audited/explained extras.
- Each repo's navigator/catalogue checks stay green.

## Provenance

Sibling check registered in the notebook-setup-notebook-regen-drift task
(autolens_workspace#480), run 2026-08-07 while that task's PR was in CI.
