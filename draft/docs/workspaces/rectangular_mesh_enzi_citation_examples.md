# Rectangular mesh Enzi citation — user-workspace pixelization examples

Type: docs
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Context (split from rectangular-mesh-consolidation, PyAutoArray#402, closed 2026-07-24)

The rectangular-mesh consolidation added an Enzi et al. 2026 (arXiv:2606.30620,
RTU grids) citation requirement to the docs citations pages
(PyAutoLens#644 / PyAutoGalaxy#520) and to the HowToLens/HowToGalaxy chapter 4
tutorials (HowToLens#53 / HowToGalaxy#43). The remaining piece — a short
paper-link paragraph in the **user-workspace pixelization examples** — was
blocked at wrap-up time because `autolens_workspace` / `autogalaxy_workspace`
were claimed by the `env-declaration-docstring-form` task
(PyAutoHands#189). File issued when that claim releases.

## Task

Add a short docstring paragraph where each rectangular pixelization example
first introduces `RectangularAdaptDensity` / `RectangularAdaptImage`:
`scripts/*/features/pixelization/*.py`, `scripts/*/features/pixelization/likelihood_function.py`,
and the SLaM pixelization guides (grep `RectangularAdapt` in both workspaces).

Wording (mirror the HowTo ch4 paragraph already merged): the adaptive
rectangular mesh implements the ray-guided transformed uniform (RTU) grid
formulation of Enzi et al. (2026), https://arxiv.org/abs/2606.30620, which
should be cited when using this mesh; note the paper pairs the RTU grid with a
Gaussian-process source prior whereas these examples use PyAutoLens's own
regularization schemes (`reg.Constant` / `reg.Adapt`).

Scripts only; notebooks regenerate at release (regen + navigator catalogue for
any HowTo/workspace edits). Tutorial prose = judgment tier.

## Constraints

- Serialise on autolens_workspace/autogalaxy_workspace if still claimed.
- Docs-only; no library or model changes.
