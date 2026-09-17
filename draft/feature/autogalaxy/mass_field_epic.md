# MassField — external shear, mass sheets and external potentials as their own model object

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- cluster
Difficulty: too-large
Autonomy: human-required
Priority: normal
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 20
Unattended: needs-slicing
Epic: mass-field
Filed: 2026-09-17

## Brief

A `Galaxy` in PyAutoGalaxy is a redshift plus a named bag of profiles; the
tracer only ever asks it for its redshift and its summed fields. `ExternalShear`,
`MassSheet` and `ExternalPotential` describe the tidal field of everything
*outside* the modelled system, so they are not properties of any galaxy, yet the
only redshift-bearing container the stack has is `Galaxy`, and so they ride on
one. In `imaging/` that is harmless (one galaxy, nothing misrepresented). With
several deflectors it is a lie the model tells: `model.info` prints `lens_0`'s
shear, users read γ as something about that galaxy, and `multi_galaxy/`
(autolens_workspace#378) had to invent a shear-only `Galaxy` named
`shear_galaxy` to say what the physics means.

The stack already half-admits the mismatch: the line-of-sight sampler builds a
`Galaxy(redshift=z, mass_sheet=MassSheet(...))` per plane
(`@PyAutoLens/autolens/lens/los.py`), the analysis carries a TODO asking
whether a subhalo should be its own class, and the COOLEST exporter
(`@PyAutoLens/autolens/interop/coolest.py`) peels `ExternalShear` / `MassSheet`
off every galaxy into a separate `MassField` entity on export and folds it back
into a `Galaxy` on import, because the standard treats external fields as a
peer of galaxies, both with a redshift. lenstronomy goes further and has no
galaxy concept at all (a flat `lens_model_list` with a per-component
redshift). COOLEST's middle ground is the right one for PyAutoLens.

**Decision (human, 2026-09-17):** `MassField` is **its own thing** — a
standalone class, *not* a `Galaxy` subclass — holding `ExternalShear`,
`MassSheet` **and** `ExternalPotential` (any `MassProfile` is accepted). It has
its own slot in the model, `fields=`, a collection like `extra_galaxies`, and
its own argument on the tracer, `Tracer(galaxies=..., fields=...)`. Only the
tracer's *planes* merge galaxies and fields at each redshift; `tracer.galaxies`
is unchanged, so nothing that indexes galaxies positionally moves. One field
carries every component at one redshift (shear + sheet + potential is one
`MassField`, as bulge + disk is one `Galaxy`); several fields means several
planes (the LOS sampler's per-plane sheets; line-of-sight shear formalisms with
foreground and background tidal planes), which is why the slot is a collection
and not a single `field=`.

**Backwards compatibility is a hard requirement.** The `Galaxy`-attached form
stays fully supported, undeprecated and unwarned: a user's existing script
composing `af.Model(al.Galaxy, ..., shear=af.Model(al.mp.ExternalShear))` must
keep working and must keep producing the same PyAutoFit result
`unique_identifier`. The identifier hashes the model's class paths and
parameter structure, not source files, so `Galaxy` may be refactored
(behaviour-preserving mixin extraction) provided its import path, constructor,
`dict()` output and prior configs are unchanged; the witness is an
**identifier pin** (same representative model, same identifier on `main` and
on the branch), not "file untouched". A shear-only `Galaxy` in a tracer list
keeps working too. A script that adopts `MassField` composes a different model
and gets a new identifier; that is expected.

`ExternalPotential` has a `centre` (its τ/δ terms have radial dependence about
it); composed in a `MassField` its centre prior is tied to the galaxy mass
centre (`field.potential.centre = lens.mass.centre`), which a `model_util`
helper makes the one-line default.

Rejected, recorded so nobody re-derives them: (a) a `Galaxy` subclass in the
`galaxies` collection — cheapest, but it keeps the false is-a relation, leaves
fields visible to every per-galaxy surface (image dicts, plotters, tables) and
keeps the positional-index hazard in every list-based workspace script; (b)
lifting the field to the model root as a bare profile — needs a redshift for
multi-plane tracing; (c) a single `field=` slot — a second spelling would be
needed the day someone models line-of-sight shear on two planes.

## Phases

Issue ONE at a time, in order, as the predecessor nears shipping — no bulk
issue queues. Phases 1 and 2 are library work (library-first gate); 3–5 are
workspace sweeps that follow the *released* libraries.

| Phase | Prompt | Repo | What it delivers | Gate |
|---|---|---|---|---|
| 1 | `draft/feature/autogalaxy/mass_field_class.md` | PyAutoGalaxy | standalone `ag.MassField(redshift, **mass_profiles)`; the mass sums shared with `Galaxy` through a mixin extracted behaviour-preservingly; zero-light interface so a plane can hold it; dict round trip; JAX pytree registration; identifier pin test; API docs. | — |
| 2 | `draft/feature/autolens/mass_field_integration.md` | PyAutoLens | `Tracer(galaxies, fields=None)`, planes merge, `tracer.fields`, `sliced_tracer_from`, `to_dict`, pytree flatten; analysis folds `instance.fields`; LOS sampler emits fields; COOLEST 1:1 both ways (legacy peel kept); `model_util.mass_field_from` with the `ExternalPotential` centre tie; tests, docs. | phase 1 merged (CI runs same-named library branches) |
| 3 | `draft/docs/workspaces/mass_field_workspace_sweep.md` | autolens_workspace | `guides/profiles/mass.py` sheets section; `multi_galaxy/` main + features + SLaM: `shear_galaxy` → `fields=af.Collection(field=...)`; LOS-halo feature scripts; `imaging/` stays galaxy-attached (see Decisions). | phases 1–2 released to the installed stack |
| 4 | `draft/docs/workspaces/propagate_shear_galaxy_idiom_to_group_cluster.md` | autolens_workspace | `group/` (four named sites + `features/**`, ~44 code sites) moves straight to `fields=`, skipping the `shear_galaxy` interim; `cluster/` surveyed and unchanged. | phase 3 merged |
| 5 | `draft/docs/workspaces/mass_field_sibling_sweep.md` | autolens_workspace_test, HowToLens, autolens_assistant | parity scripts and any tutorial/wiki mention of `shear_galaxy` or "shear on lens_0"; decided by grep after phase 3. | phase 3 merged |

## Decisions

- **BC is a hard invariant** (Brief). No change to `Galaxy`'s import path,
  constructor signature, `dict()`/`to_dict` output or any `config/priors/*.yaml`;
  no deprecation warning on galaxy-attached sheets. Witness for every library
  phase: the identifier pin (a representative galaxy-attached model's
  `unique_identifier` computed on `main` and on the branch, equal).
- **`MassField` is standalone.** It shares the mass-sum implementation with
  `Galaxy` through a mixin (`has`, `cls_list_from`, deflections / convergence /
  potential sums) so nothing is duplicated, and implements the minimal
  zero-light interface a plane needs (`image_2d_list_from` → empty,
  `has(LightProfile)` → False). `isinstance(field, Galaxy)` is False, so
  per-galaxy surfaces never see it.
- **Model slot `fields=`, a collection; tracer argument `fields=`, a list.**
  The analysis folds `list(instance.fields)` into `Tracer(fields=...)` exactly
  as it folds `extra_galaxies` / `scaling_galaxies` into `galaxies`. Planes
  merge galaxies and fields at each redshift; `tracer.galaxies` never contains
  a field. The multi-galaxy `n_main` counting (`lens_` prefix over
  `instance.galaxies`) is untouched.
- **`ExternalPotential` is a field, centre tied to the galaxy mass** via
  `model_util.mass_field_from(lens, potential=True)`; for a multi-deflector
  system the caller names the primary galaxy explicitly.
- **`imaging/` keeps the galaxy-attached form.** Single-galaxy, nothing
  misrepresented, the form most users' scripts carry; moving it would change
  every reader's result identifier for no physical gain. Its `__External
  Shear__` prose gains one paragraph pointing at `MassField` for
  multi-deflector systems. Revisit only if the human asks.
- **Naming.** `MassField` follows COOLEST so the interop is 1:1; `fields` is the
  model slot and tracer argument; `field` the conventional single entry.

## Ledger

- 2026-09-17: epic filed from the `/start_dev` plan checkpoint of the group
  shear prompt (Fable session); first draft had `MassField` as a `Galaxy`
  subclass in the `galaxies` collection.
- 2026-09-17 (same day, human ruling): redesigned to a standalone class with
  its own `fields=` model slot and tracer argument — the human's "MassField is
  its own thing"; `fields` is a collection because shear + sheet at one
  redshift is one field, while several fields means several planes. Phase 2
  re-sized medium → large; phase 4 loses its positional-index trap.
