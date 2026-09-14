The Enzi et al. (2026) RTU citation paragraph reached the user-workspace pixelization
examples in both autolens_workspace and autogalaxy_workspace — carried silently by the
rectangular mesh split rather than by its own task.

## What shipped

- The citation landed on 2026-08-21 in autolens_workspace `44998cf7` ("feat: rectangular mesh
  split — Bilinear default (imaging), RTU advanced/interferometer"), the workspace leg of
  `complete/2026/08/rectangular-bilinear-rtu-mesh-split.md` (PyAutoArray#462, autolens_workspace#495,
  autogalaxy_workspace#221). A follow-up `f8df9268` added the end-of-script RTU doc section.
- The paragraph reads exactly as this prompt specified — it names the ray-guided transformed
  uniform (RTU) grid formulation, links https://arxiv.org/abs/2606.30620, and says it "should
  be cited when using these meshes".

## Why the prompt's own witness is satisfied

The prompt's witness asked that, in both workspaces, the set of files introducing the adaptive
rectangular mesh and the set carrying the Enzi paragraph be the same set.

- autogalaxy_workspace — exact match. `RectangularRTU*` and `2606.30620` both appear in exactly
  `scripts/imaging/features/pixelization/{README.md, likelihood_function.py, modeling.py}`.
- autolens_workspace — the citation is in all six files that introduce the mesh
  (`scripts/imaging/features/pixelization/{README.md, adaptive.py, likelihood_function.py, modeling.py}`,
  `scripts/interferometer/features/pixelization/{README.md, modeling.py}`). The one remaining
  `RectangularRTU*` mention, `scripts/guides/modeling/searches.py:156`, is a cross-reference
  ("gradient-based searches must use the kernel-CDF meshes"), not an introduction, so it is
  correctly outside the citation set.
- The diff touched scripts and guides only — no library or model code.

## Trap: the prompt's class names no longer exist

The prompt targets `RectangularAdaptDensity` / `RectangularAdaptImage`. The same mesh split that
carried the citation **renamed** those classes to the `RectangularBilinear*` / `RectangularRTU*`
four, so a literal grep for the prompt's own anchor returns nothing in either workspace and reads
as "not shipped". The citation belongs to the RTU half of the split; check the current class names
before concluding a rename-era prompt is unstarted.

## Retirement note

`complete/2026/08/rectangular-bilinear-rtu-mesh-split.md` says in two places (its "Left open"
bullet and its ship notes) that this draft "was to be folded in; it remains a separate draft and
stands on its own". That was true of the *prompt*; it was not true of the *work*. Those two
pointers should be repointed at this record. The related `RectangularAdaptDensity:` /
`RectangularAdaptImage:` orphan prior file in `autolens_workspace_test/config/priors/mesh/rectangular.yaml`
is that record's hygiene item, not this one's.

## Original prompt

# Rectangular mesh Enzi citation — user-workspace pixelization examples

Type: docs
Target: workspaces
Repos:
- autolens_workspace
- autogalaxy_workspace
Themes:
- pixelization
- notebooks
- docs-hub
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: In both workspaces the set of files introducing `RectangularAdaptDensity`/`RectangularAdaptImage` and the set carrying the Enzi et al. (2026) arXiv:2606.30620 paragraph are the same set, and the diff touches scripts and guides only — no library or model code.
Review-minutes: 0
Unattended: ready
Filed: 2026-07-24 (backfilled from git)

## Context (split from rectangular-mesh-consolidation, PyAutoArray#402, closed 2026-07-24)

The rectangular-mesh consolidation added an Enzi et al. 2026 (arXiv:2606.30620,
RTU grids) citation requirement to the docs citations pages
(PyAutoLens#644 / PyAutoGalaxy#520) and to the HowToLens/HowToGalaxy pixelizations-chapter (chapter 3 since the 2026-08 restructure)
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
