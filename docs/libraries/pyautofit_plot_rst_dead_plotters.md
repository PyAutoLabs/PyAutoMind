# Fix dead plotter references in PyAutoFit docs/api/plot.rst

Type: docs
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Filed 2026-07-12 from a `/hygiene docs` (`/audit_docs`) audit.

## Why

`PyAutoFit/docs/api/plot.rst` documents three classes under
`.. currentmodule:: autofit.plot` that **no longer exist** in the installed
`autofit`:

- `NestPlotter`
- `MCMCPlotter`
- `MLEPlotter`

A package-wide search finds no `*Plotter` class anywhere in `autofit` (not
renamed — removed/relocated). `autofit.plot` imports but exposes zero public
classes. The autosummary block therefore generates broken `_autosummary`
stubs. This was previously parked behind the graphical-model docs work; the
docs audit re-surfaces it as the only broken reference across all three
libraries' API docs (18/18 modules OK, 392/395 class refs OK).

## Scope

- Determine the **current** PyAutoFit plotting entry points (what replaced the
  removed plotters — likely a different plotting API surface) and repoint or
  remove the `plot.rst` autosummary block accordingly. Do **not** just delete
  and leave a hole if a live plotting API exists to document.
- This is a judgement call on the current API, hence a `/docs` task not an
  auto-fix.

## Coordination

There is an active `feature/ep-graphical-docs` worktree on PyAutoFit whose
scope covers plotting/graphical docs but which has **not** yet touched
`plot.rst` (verified identical to `main`). Either fold this fix into that
branch or ship it standalone — decide at plan time to avoid a collision.

## Verify

- `python -c "import autofit.plot"` and confirm each documented name resolves.
- Docs build produces no missing-reference / autosummary warnings for plot.rst.
