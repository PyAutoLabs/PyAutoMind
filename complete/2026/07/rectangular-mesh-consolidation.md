## rectangular-mesh-consolidation
- completed: 2026-07-24
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/402 (closed)
- prs (all MERGED): PyAutoArray#403 (library), PyAutoLens#644 + PyAutoGalaxy#520 (Enzi citations page + bib), HowToLens#53 + HowToGalaxy#43 (ch4 tutorial citation paragraph), autolens_workspace_test#209 (jax_grad migration + reference re-derivation)
- summary: Consolidated PyAutoArray's rectangular mesh family from 8 mesh classes / 5 interpolators / 2 geometries down to the two that matter. The kernel-density-CDF meshes (the strict-FD-certified gradient path, formerly RectangularKernelAdapt*, #374) TOOK OVER the plain names RectangularAdaptDensity/AdaptImage; RectangularUniform (no interpolation, HowToLens methodology) unchanged. DELETED from source: the linear empirical-CDF path (piecewise-constant likelihood in mass/shear at os=1 + interferometer sparse), the spline pair (#289, never certified), the PCA-rotated multi-node mesh (#323), density_components.py (unwired), and MeshGeometryRectangularRotated — all recoverable via git history. InterpolatorRectangular kept its name+module path as the kernel implementation, so PyAutoGalaxy/PyAutoLens needed ZERO source edits (verified: 892/1006/448 tests green; af.Model prior counts unchanged 2/4/2 via None-default bandwidth/n_knots kwargs). The surviving mesh implements the RTU formulation of Enzi et al. 2026 (arXiv:2606.30620) — citation requirement added to the docs.
- key decisions: (1) kernel takes plain names (zero workspace/prior-YAML churn, old results still load) over mass-renaming ~550 refs; (2) linear path fully deleted (one adaptive method); user-approved both 2026-07-23. Brain scored too-large/4-phase off repo COUNT — OVERRIDE to library→workspace two-leg recorded (workspace leg collapsed to test/dev cleanup under the naming decision).
- traps hit: (a) the census grepped CLASS NAMES but the real blast radius included NUMERICAL references — autolens_workspace_test/jax_likelihood_functions/imaging/rectangular*.py hard-code reference log-likelihoods computed by the deleted linear mesh; the SMOKE gate caught what static grep could not. Re-derived: rectangular.py -651693→-644121 and rectangular_mge.py -82.9→-9.1 (both IMPROVED at default bandwidth); rectangular_dspl.py is bandwidth-sensitive (default 1.0 over-smooths its adapt-image weights: -6340) so it pins bandwidth=0.1 (-3824, ≈ old linear -3696) with in-line rationale. (b) PyAutoArray#403 main-merge conflict: main's version-bump commit had CRLF'd autoarray/__init__.py — merge restored LF per repo rules. (c) wst#209 absorbed the parallel env-declaration-docstring-form __Env__ docstring migration in a second main-merge.
- bandwidth = the kernel-CDF smoothing width (h, in mesh-pixel units): F(x)=Σ wᵢ Φ((x−xᵢ)/h). Optimal h differs in SIGN across configs (smoke/MGE prefer 1.0, dspl prefers 0.1) — no single good default; it also smooths the adapt-image weights, so it interacts with the adaption you already fit. Follow-up research prompt filed on whether to fit it (it carries a smooth gradient) or auto-scale the default.
- followups (split to draft/, both blocked at wrap-up time): (1) workspace citation paragraphs for autolens_workspace/autogalaxy_workspace pixelization examples (HowTo ch4 already done) — blocked on env-declaration-docstring-form claim; (2) autolens_workspace_developer cleanup + PyAutoGut stash of the spline/rotated experiments + rename its kernel-named scripts — blocked on blackjax-smc-gradient-kernel claim; (3) research draft/research/autoarray/rectangular_kernel_bandwidth_defaults.md (fit-vs-set bandwidth, auto-scaled default).

## Original prompt

# Rectangular mesh consolidation — keep kernel + uniform, retire linear/spline/rotated

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
- autogalaxy_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autolens_workspace_developer
- HowToLens
- HowToGalaxy
- PyAutoGut
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

In PYAutoArray we have ended up with loads of Rectangular mesh classes and
associated other classes, and its confusing and unecessary. I think only two
are actually use: The kernel one which actually does gradients ok, and the
uniform one which does not use interpolation which is used in HowToLens to
illustrate the methodology. Can you do a census of all these different
classes, confirm only these are useful (but keep both adaptdensity and
adaptimage) and refactor and tidy up this part of the source code? In turn
make sure all workspaces only use this gradient one which is the one users
will actually use. Double check none others have any use. We also did some
work on a more adaptive rectangular mesh which for example adapts to multiple
nodes. This work may come back (e.g. once we have the basic rectangular
working with gradients well) but lets move it out the source code, if its
thre, for now, and stash workspace work in PyAutoGut. im not usre what
rectangular_rotated_adapt_image.py is for and if we still need it, and if the
split / kernel separrate methods both have uses but lets get down to just one

## Census context (2026-07-23)

Current family in `autoarray/inversion/mesh/`:

- Mesh classes (`mesh/`): RectangularAdaptDensity, RectangularAdaptImage
  (linear empirical-CDF, piecewise-constant likelihood at os=1 —
  the pre-kernel gradient path), RectangularKernelAdaptDensity,
  RectangularKernelAdaptImage (kernel-density CDF, Enzi RTU, strict-FD
  certified 2026-07-10, PR #374), RectangularSplineAdaptDensity,
  RectangularSplineAdaptImage (deg-11 spline CDF, PR #289 2026-04-22, shipped
  with known JIT oscillation limitation, superseded by kernel),
  RectangularRotatedAdaptImage (PCA-rotated spline, "ghost-peak"/multi-modal
  Path A experiment, PR #323 2026-05-17 — the "adapts to multiple nodes"
  work), RectangularUniform (no interpolation, HowToLens methodology
  illustration).
- Interpolators (`interpolator/`): InterpolatorRectangular (linear),
  InterpolatorRectangularKernel, InterpolatorRectangularSpline (+
  InvertPolySpline), InterpolatorRectangularRotatedSpline,
  InterpolatorRectangularUniform.
- Geometries (`mesh_geometry/`): MeshGeometryRectangular,
  MeshGeometryRectangularRotated.

Downstream libraries (PyAutoGalaxy/PyAutoLens) reference only:
RectangularUniform (test fixtures, heavily), RectangularAdaptDensity /
RectangularAdaptImage (packaged prior YAMLs, rst autosummary, exc
docstrings), InterpolatorRectangular (plain `__init__` re-export). Zero
downstream references to kernel/spline/rotated variants.

## Task

1. Keep: RectangularKernelAdaptDensity + RectangularKernelAdaptImage (the
   gradient meshes users will use) and RectangularUniform (HowToLens
   illustration), plus whatever base machinery they need.
2. Retire from source: spline pair, rotated mesh + rotated
   geometry/interpolator (multi-node work — may come back once the kernel
   mesh is proven; preserve as recoverable refs via PyAutoGut condemned-
   material lifecycle), and consolidate linear-vs-kernel down to kernel only
   — the linear empirical-CDF interpolator goes unless it is load-bearing as
   the kernel/uniform base.
3. Decide the public naming: with only one gradient method left, consider
   whether the kernel meshes should take the plain RectangularAdaptDensity /
   RectangularAdaptImage names (prior YAML keys, docs and workspace scripts
   follow the chosen names).
4. Update downstream: PyAutoGalaxy/PyAutoLens prior configs, rst docs, exc
   docstrings, fixtures; workspaces + HowTo tutorials use the kernel mesh
   everywhere except the HowToLens uniform-mesh methodology sections.
5. Stash workspace-side experimental rectangular scripts (rect_adapt_duo
   demo, spline/rotated experiments in autolens_workspace_developer) in
   PyAutoGut.
6. Double-check no other variant has a live use before deleting (grep +
   test suite + smoke).

## Constraints

- Library unit tests numpy-only; JAX validation via workspace_test jax_grad
  scripts (kernel FD certification must stay green).
- Never rewrite pushed history; deletions land as normal PRs.
- Prior-config keys are serialization-load-bearing (model save/load) — check
  aggregator/database round-trip against renamed classes.
