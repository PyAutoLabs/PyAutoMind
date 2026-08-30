# Deferred: make the `*Power` adapt classes the defaults (breaking)

Type: feature
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
Themes:
- pixelization
- inference
Difficulty: large
Autonomy: human-required
Priority: low
Status: deferred — decision only, do not start without an explicit human call
Consequence: judge
Review-minutes: 25
Unattended: never
Filed: 2026-08-29

## The deferred decision

On 2026-08-29 the `AdaptPower` / `AdaptSplitPower` / `AdaptSplitZerothPower` /
`MaternAdaptPowerKernel` classes shipped as **siblings** of the legacy
`Adapt` family (`feature/autoarray/adapt_linear_regularization.md`). The
legacy classes were kept byte-for-byte so that `af.Model` identifiers, stored
`output/` directories and aggregator reloads stay valid.

The open question: **should the `*Power` classes eventually become the
defaults** — i.e. should `Adapt` itself adopt the λ² convention (`power=1.0`)
and the single-scatter builder, with the legacy behaviour reachable only as
`Adapt(power=2.0)` on the old scatter?

## Why it would be worth doing

- One scheme, one convention: `Adapt`, `AdaptSplit` and `Constant` would all
  put the coefficient into the matrix as λ², so the shared
  `LogUniform(1e-6, 1e6)` prior means the same thing everywhere.
- The λ⁴ scale is what makes the adaptive schemes go numerically non-PD from
  `c ≈ 1e4` instead of `c ≈ 1e6`, which is the mechanism behind the
  likelihood-overflow flood diagnosed on RAL pilot 341908_5.
- `Adapt(inner=outer=c)` would finally equal `Constant(c)`, as its docstring
  claimed for years.

## Why it is deferred

It is **breaking in the worst way**: silent and science-visible.

- Every stored adaptive result's coefficient changes meaning
  (`c_new = c_old ** 2`, plus a factor 2 on the non-split scatter).
- `af.Model` identifiers do **not** change (same class path), so an aggregator
  reload would silently mix pre- and post-change runs.
- Every SLaM pipeline, workspace example, config default, HowTo tutorial and
  profiling ledger row that pins an adaptive coefficient would need re-scaling
  and re-certifying.

## What a decision would need

1. A named breaking release with a migration note and a `c_new = c_old ** 2`
   converter.
2. An identifier-bump mechanism (or a documented "results before version X are
   not comparable" boundary), since the class path alone will not disambiguate.
3. Re-certification of the adaptive reference runs in `autolens_profiling`.
4. A sweep of the workspace/HowTo/SLaM coefficient literals and prior configs.

Until a human explicitly asks for it, the answer is: use `*Power` for new
work, leave `Adapt` alone.
