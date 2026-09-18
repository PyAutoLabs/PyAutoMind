# Accept a bare `MassField` in `fields=` so the flat model form works

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
Difficulty: small
Autonomy: human-required
Priority: normal
Consequence: judge
Epic: mass-field
Filed: 2026-09-18
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/743
Witness: with the branch installed, `af.Collection(galaxies=..., fields=af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear)))` yields prior paths `fields.shear.gamma_1/gamma_2` (not `fields.field.shear.…`), `AnalysisImaging`'s tracer construction succeeds on its instance, and `tracer.fields == [MassField(redshift=0.5, shear)]`. On `main` the same model raises `TypeError: 'MassField' object is not iterable`. The collection form `fields=af.Collection(field=field)` is unchanged in paths, prior count and result identifier.

## Original request

> The following API: field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear)) and model = af.Collection(
>     galaxies=af.Collection(lens=lens, source=source),
>     fields=af.Collection(field=field),
> ) produces model.fields.field.shear, is there a way to avoid the double API of field.shear?

and, after the options were reported back:

> do this If you want the flat form to work, it's a small library change in PyAutoLens, in two places:
> 1. PyAutoLens/autolens/analysis/analysis/lens.py:138 — wrap a bare MassField in a list rather than calling list() on it.
> 2. PyAutoLens/autolens/lens/tracer.py:240 (_validate_fields) plus the self.fields = list(fields) line in Tracer.__init__ — accept a single MassField.
>
> Adding __iter__ to MassField in PyAutoGalaxy would also satisfy list(), but it would yield the field's profiles, not the field — wrong for Tracer(fields=...). So the lens-side change is the right one.

## Why

The shipped composition is `fields=af.Collection(field=field)`, giving parameter
paths `fields.field.shear.gamma_1`. The middle level is a name the user must
invent for a collection that, in every workspace example today, holds exactly
one entry — so it reads as a stutter (`fields.field`) rather than as
information. The galaxy-attached form it replaced was one level shallower
(`galaxies.lens.shear.gamma_1`).

Measured against the installed stack 2026-09-18:

| Form | Paths | Result |
|---|---|---|
| `fields=af.Collection(field=field)` | `fields.field.shear.gamma_1` | works (current convention) |
| `fields=af.Collection(los=field)` | `fields.los.shear.gamma_1` | works — rename only |
| `fields=af.Collection([field])` | `fields.0.shear.gamma_1` | works — index middle level |
| `fields=field` | `fields.shear.gamma_1` | **builds, then dies at tracer construction** |

`prior_count` is 14 in all four. Only the flat form removes the level, and it is
the one that breaks: `MassField` and its base `MassProfileAggregate` define
neither `__iter__` nor `__getitem__`, so `list(instance.fields)` raises, and
`_validate_fields` independently rejects a non-list/tuple non-`ModelInstance`.

## Scope

Three edits, all in PyAutoLens:

1. `autolens/analysis/analysis/lens.py` (~line 138, `_tracer_via_instance_from`)
   — the `fields = list(instance.fields) if getattr(instance, "fields", None) is
   not None else None` block wraps a bare `MassField` in a list instead of
   calling `list()` on it.
2. `autolens/lens/tracer.py` `_validate_fields` (line 240) — accept a single
   `MassField` alongside the list/tuple/`ModelInstance` forms, keeping the
   string trap and the `Galaxy`-in-`fields` message intact.
3. `autolens/lens/tracer.py` `Tracer.__init__` (~line 352) — `self.fields =
   list(fields)` normalises a single `MassField` to `[field]`, preserving the
   "plain list, never None" invariant the members-walking properties rely on.

Explicitly **not** in scope: adding `__iter__`/`__getitem__` to `MassField` in
PyAutoGalaxy. It would satisfy `list()` but yield the field's *profiles*, not
the field, which is wrong for `Tracer(fields=...)` and would silently produce a
tracer holding `ExternalShear` objects with no redshift.

## Open questions for the plan

- **Epic decision conflict.** The mass-field epic's Decisions section reads
  "Model slot `fields=`, a collection; tracer argument `fields=`, a list. The
  analysis folds `list(instance.fields)` into `Tracer(fields=...)` exactly as it
  folds `extra_galaxies` / `scaling_galaxies` into `galaxies`." Accepting a bare
  field relaxes that and breaks symmetry with `extra_galaxies` /
  `scaling_galaxies`, which stay collection-only. Decide whether the relaxation
  is accepted as a second supported form (both work) and record it in the epic
  ledger.
- **Which form the workspaces teach.** Phase 3 (`autolens_workspace` +
  `autolens_workspace_test`, 217 + 87 files) has shipped as draft PRs using the
  collection form, and phase 5 (HowToLens, autolens_assistant) is unstarted. If
  the flat form becomes the taught idiom, that is a follow-up sweep, not this
  task. This task adds the capability only.
- **Multi-field systems.** The collection form stays mandatory for more than one
  field (per-plane LOS sheets, foreground/background tidal planes); the flat
  form is a single-field convenience. Error messages should say so.
- Whether `Tracer(fields=<bare MassField>)` should also be accepted directly, or
  only the model slot. Scope above assumes both, since `_validate_fields` is the
  shared door.

## Notes

- Backwards compatibility is the epic's hard invariant: the collection form's
  paths, prior count and PyAutoFit result identifier must be untouched, and the
  galaxy-attached form stays unwarned.
- Diagnostic script behind the table:
  `/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/65d55a6f-8729-4857-be92-b098eeb4031d/scratchpad/field_variants.py`
  (scratch, not committed).


## Approved implementation plan (2026-09-18)

The handoff's expanded five-site plan and Codex read-only review supersede the
initial three-edit scope and open questions above. User approved with `proceed`.
Canonical detailed plan: https://github.com/PyAutoLabs/PyAutoLens/issues/743.

- Library capability only, collection and flat forms supported; collection examples remain primary.
- Internal fields_list_from helper plus Tracer constructor/slicing, analysis, aggregator and Result folds.
- Preserve validation messages; bare Galaxy gets the existing generic container error,
  while [Galaxy] gets the targeted galaxies-argument message.
- Normalize before the geometry warning. Update public annotations and the four specified docs surfaces.
- Add aggregator coverage, list ownership, empty slots, generator non-consumption and MassSheet convergence
  to the handoff test plan. Existing test_autolens/analysis/test_result.py is extended, not replaced.
- Baseline reproduced on 719738067: collection c5cf98ea7733689dc8c0ede6939c1d83,
  flat 36a0be37c9667958bafca2f01e487f80, both prior_count 14. Red witness captured
  before source edits: TypeError at analysis/analysis/lens.py:139.
