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

**Decision (human, 2026-09-17):** add `MassField`, a sibling of `Galaxy` (a
`Galaxy` subclass that accepts only `MassProfile` components), holding
`ExternalShear`, `MassSheet` **and** `ExternalPotential`. It lives in the model's
`galaxies` collection like any other redshifted object, so `Tracer`, `Galaxies`,
the fits, the plotters and the SLaM `lens_`-prefix counting need no change. The
`Galaxy`-attached form stays fully supported, undeprecated and unwarned:
**backwards compatibility is a hard requirement** — a user's existing script
composing `af.Model(al.Galaxy, ..., shear=af.Model(al.mp.ExternalShear))` must
keep working and must keep producing the same PyAutoFit result `unique_identifier`,
so `Galaxy` itself and every prior config it touches are left byte-identical. A
script that adopts `MassField` composes a different model and gets a new
identifier; that is expected. `ExternalPotential` has a `centre`; when it is
composed in a `MassField` its centre prior is tied to the galaxy mass centre
(`mass_field.potential.centre = lens.mass.centre`), which a `model_util` helper
makes the one-line default.

Why not lift the field to the tracer or the model root (lenstronomy-style):
multi-plane tracing needs the field at a redshift, `Analysis.tracer_via_instance_from`
and every pipeline would grow a new slot, and it is a large blast radius for a
naming problem. Recorded so nobody re-derives it.

## Phases

Issue ONE at a time, in order, as the predecessor nears shipping — no bulk
issue queues. Phases 1 and 2 are library work (library-first gate); 3–5 are
workspace sweeps that follow the *released* libraries.

| Phase | Prompt | Repo | What it delivers | Gate |
|---|---|---|---|---|
| 1 | `draft/feature/autogalaxy/mass_field_class.md` | PyAutoGalaxy | `ag.MassField(Galaxy)`: MassProfile-only container, validation, repr/dict round trip, JAX pytree registration, tests, API docs. `Galaxy` untouched. | — |
| 2 | `draft/feature/autolens/mass_field_integration.md` | PyAutoLens | pytree walker registers it; COOLEST maps `al.MassField` ↔ `MassField` 1:1 (legacy peel kept for galaxy-attached sheets); LOS sampler emits `MassField` sheets; `model_util.mass_field_from` helper with the `ExternalPotential` centre tie; tests, docs. | phase 1 merged (CI runs same-named library branches) |
| 3 | `draft/docs/workspaces/mass_field_workspace_sweep.md` | autolens_workspace | `guides/profiles/mass.py` sheets section; `multi_galaxy/` main + features + SLaM: `shear_galaxy` → `mass_field`; LOS-halo feature scripts; `imaging/` stays galaxy-attached (see Decisions). | phases 1–2 released to the installed stack |
| 4 | `draft/docs/workspaces/propagate_shear_galaxy_idiom_to_group_cluster.md` | autolens_workspace | `group/` (four named sites + `features/**`, ~44 code sites, positional-index audit) moves straight to `mass_field`, skipping the `shear_galaxy` interim; `cluster/` surveyed and unchanged. | phase 3 merged |
| 5 | `draft/docs/workspaces/mass_field_sibling_sweep.md` | autolens_workspace_test, HowToLens, autolens_assistant | parity scripts and any tutorial/wiki mention of `shear_galaxy` or "shear on lens_0"; decided by grep after phase 3. | phase 3 merged |

## Decisions

- **BC is a hard invariant.** No change to `Galaxy.__init__`, its validation,
  its `dict()`/`to_dict` output or any `config/priors/*.yaml`; no deprecation
  warning on galaxy-attached sheets. Witness for every library phase: the
  `Galaxy` module and prior configs are absent from the diff.
- **`MassField` is a `Galaxy` subclass, not a duck-typed peer.** `Tracer`
  promises subclasses keep working (`_validate_galaxies` docstring); `Galaxies`
  and the plotters call the aggregate methods; the pytree walker registers by
  class. Subclassing gets all of that for one registration line.
- **It sits in the `galaxies` collection**, named `mass_field` by convention.
  A separate `fields` slot on the model was rejected for now: it would touch the
  analysis and every pipeline for no tracer-side benefit.
- **`ExternalPotential` is a field, centre tied to the galaxy mass.** Its
  τ/δ terms have radial dependence about `centre`, so the centre must be a
  physical point; the convention is the primary lens galaxy's mass centre,
  shared as a prior (`mass_field.potential.centre = lens.mass.centre`). For a
  multi-deflector system "primary" is the model author's choice and the
  helper takes the galaxy explicitly.
- **`imaging/` keeps the galaxy-attached form.** It is the single-galaxy case
  where nothing is misrepresented, it is the form most users' scripts carry,
  and moving it would change every reader's result identifier for no
  physical gain. Its `__External Shear__` prose gains one paragraph pointing
  at `MassField` for multi-deflector systems. Revisit only if the human asks.
- **Naming.** `MassField` follows COOLEST so the interop is 1:1 and the word
  already has a definition users can look up. `mass_field` is the model key.

## Ledger

- 2026-09-17: epic filed from the `/start_dev` plan checkpoint of the group
  shear prompt (Fable session) — the research that led here is on that
  session; summary in the Brief. Phase 4 is the re-scoped original prompt.
