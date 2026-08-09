Phase 2 (PyAutoLens half) of the @rhayes777 API audit —
[PyAutoLens#532](https://github.com/PyAutoLabs/PyAutoLens/issues/532).

**Shipped:** PyAutoLens#696, squash-merged `65183d1` 2026-08-09. #532 closed.
Epic PyAutoArray#415 stays open for phase 4.

## Delivered — B4 only, and the issue split across two repos

`Tracer(galaxies="not a list")` constructed happily and failed later with
`AttributeError: 'str' object has no attribute 'redshift'`. It now raises `TypeError`
at construction, naming `galaxies` and the type given.

**Broader than reported:** verified on `main` that `42`, `None` and `{'a': 1}` were all
accepted at construction too, not only the reported string.

**The string is the trap.** A string *is* iterable, so `isinstance(x, Iterable)` does
not catch it — the issue called this out and the guard checks element type, not
iterability. Elements are duck-typed on `redshift` (so mocks and `Galaxy` subclasses
keep working, and `redshift` is precisely the attribute whose absence caused the
original error); `af.ModelInstance` is accepted unexamined, since that is how PyAutoFit
hands the tracer a model's galaxies during a fit.

## The negative-redshift half went to PyAutoGalaxy

The other finding on this issue is guarded in **PyAutoGalaxy#566**, not here.
`al.Galaxy` **is** `ag.Galaxy` — the class and its `redshift` assignment live at
`autogalaxy/galaxy/galaxy.py:52`. A `Tracer`-level redshift check would have missed a
bare `al.Galaxy(redshift=-0.5)`, which is the reported reproduction.

**Lesson:** the repo an issue is *filed on* is where the user hit it, not necessarily
where the attribute is set. Both PRs cross-reference the split so the record is not
confusing later.

## Phase 4 stays held — with a guard-rail

`z_lens > z_source` is **not** implemented. Multi-plane lensing genuinely supports
geometries that look inverted under two-plane naming, and whether it should even *warn*
is still an open question put to @rhayes777 on #532 (no reply as of 2026-08-09).

Rather than leave that implicit, a control test pins today's permissive behaviour: a
`z_lens=1.0` / `z_source=0.5` tracer must still construct and evaluate to a finite
image. Phase 4 cannot quietly turn it into an error without that test failing. A
matching guard-rail sits at `Galaxy` level in PyAutoGalaxy#566.

## Validation

- Full suite **519 passed / 1 skipped**, **+13 new tests**
  (`test_autolens/lens/test_tracer_validation.py`). CI green on 3.12, 3.13 and docs.
- **Zero regressions.**
- Controls cover list, tuple, empty list (degenerate but legal, used in chaining) and
  `af.ModelInstance`.

## Note on the tracer gate

Unlike the other audit guards, this one needs no concreteness gate: it validates the
*container*, and a JAX trace makes a galaxy's parameters traced, never the list of
galaxies itself. Recorded in the docstring so it does not look like an omission.

## Original prompt

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
