# PyAutoLens#532: `Tracer` accepts non-iterable galaxies; negative redshifts accepted

Type: bug
Target: autolens
Repos:
- @PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

[PyAutoLens#532](https://github.com/PyAutoLabs/PyAutoLens/issues/532), filed
2026-05-23 by @rhayes777 auditing released `2026.5.21.1`. Both findings
re-verified against `main` on 2026-07-28 and **both still reproduce**. Answered
on the issue 2026-07-28 (`#issuecomment-5105855829`); tracking epic is
[PyAutoArray#415](https://github.com/PyAutoLabs/PyAutoArray/issues/415).

## Depends on the PyAutoArray helper

The guards here should use the shared `_validate_*` helper and message template
defined by `draft/bug/autoarray/rhayes_333_input_validation_guards.md`. Start
that prompt first so all three repos speak with one voice.

## In scope — two guards

**B4 — `Tracer(galaxies="not a list")` is silently constructed.**

```python
t = al.Tracer(galaxies="not a list")   # constructed
t.image_2d_from(grid=grid)             # AttributeError: 'str' object has no attribute 'redshift'
```

The first usage does eventually fail, but with a downstream error that names
nothing the caller passed. Wanted:
`TypeError("galaxies must be an iterable of Galaxy")` at construction. Note a
string *is* iterable — an `isinstance(x, Iterable)` check alone does not catch
this case. Validate the element type, not just iterability.

**Negative / degenerate redshift.** `redshift = -0.5` and `redshift = 1e-12` are
both accepted today. A negative redshift is unphysical and **can raise
outright**.

Per `planned.md`, the negative-redshift half of #532 is explicitly **not** blocked
on the phase-4 question below — it rides with the phase-2 validation sweep, i.e.
with this prompt.

## Out of scope — HELD, do not implement

**`z_lens > z_source` must not be touched by this prompt.**

```python
l = al.Galaxy(redshift=1.0, mass=al.mp.IsothermalSph(einstein_radius=1.0))
s = al.Galaxy(redshift=0.5, bulge=al.lp.Sersic(...))
al.Tracer(galaxies=[l, s]).image_2d_from(grid=grid).sum()   # 65.05, finite, no warning
```

Multi-plane lensing genuinely supports geometries that look wrong under
two-plane naming, so this should **warn at most, never raise**. On 2026-07-28 the
reply on #532 asked @rhayes777 directly whether even a warning would be noise in
a real multi-plane setup. **No reply as of 2026-08-09.** This is phase 4 of the
epic and stays held until he answers — everything else on this issue is
unblocked, which is why the two guards above can ship without him.

If a `/wake_up` or `/community` pass finds he has since answered, that is a
separate prompt, not a late addition to this one.

## Binding constraint — JAX

`Tracer` construction sits on **JAX-traced** paths. Guards must stay correct
under tracing and cost nothing when traced: no Python `if` on a value that may be
a tracer. Use the tracer-safe form settled in the PyAutoArray prompt.

## Verification

- Regression test per guard, built from the reporter's snippets.
- Assert the `TypeError` message names `galaxies`, and that a **string** input is
  rejected (the trap in B4).
- Assert a negative redshift raises and names `redshift`.
- Controls that must keep passing: a normal `[lens, source]` list, and — until
  phase 4 resolves — a `z_lens > z_source` configuration must still **construct
  and evaluate without raising**. A test pinning that is worth adding here, so
  phase 4 cannot silently regress it.
- Library unit tests stay **numpy-only** (no JAX).

## Do not route to `start_dev_for_user`

The reporter's PR offer was declined warmly on 2026-07-28 (JAX-traced hot paths).
We implement in-house.

## Provenance

- Epic: PyAutoArray#415 (open — phases 2-4)
- Campaign prompt: `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md`
- Registry: `planned.md` § `rhayes-audit-validation-phases-2-4`
- Sibling issue PyAutoLens#531 (`PointSolver`) already **closed** in phase 1.
