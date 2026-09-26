## mass-field-class
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/620 (closed completed 2026-09-17)
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/621 (merge 33714b80)
- epic: mass-field (phase 1 of 5; ledger complete/archive/epics/mass_field_epic.md)
- summary: Added `ag.MassField(redshift, **mass_profiles)` to PyAutoGalaxy — the standalone, MassProfile-only container for external shear, mass sheets and external potentials (any `MassProfile` accepted; `ExternalShear`/`MassSheet`/`ExternalPotential` intended). Its own class, not a `Galaxy` subclass: `isinstance(field, Galaxy)` is False, per-galaxy surfaces never see it, and a `Galaxies` plane holds it beside galaxies where it adds to every mass quantity and contributes zeros to every image (`image_2d_list_from → []`, `image_2d_from → zeros`, unbinned variants likewise; no `OperateImageList` inheritance). `Galaxy`'s mass sums (`cls_list_from`, memo-routed `deflections_yx_2d_from`, `convergence_2d_from`, `potential_2d_from`, `extract_attribute`) moved verbatim into `autogalaxy/galaxy/mass_aggregate.py: MassProfileAggregate`, inherited LAST by `Galaxy` so its MRO resolves every name as before (`has` still from `af.ModelObject`). Backwards compatibility proven by an identifier pin: the galaxy-attached model `af.Collection(galaxies=af.Collection(lens=af.Model(ag.Galaxy, redshift=0.5, mass=af.Model(ag.mp.Isothermal), shear=af.Model(ag.mp.ExternalShear))))` has identifier `7b251058cdae562470abab6203bacf72` on main (67f6ca6) and after the refactor, asserted as a regression test. No prior-config change, no deprecation warning. Exported as `ag.MassField`; `docs/api/galaxy.rst` and the start-here overview ("External Fields") updated. 24 new tests in `test_autogalaxy/galaxy/test_mass_field.py`; full suite 1236 passed; CI green (3.12, 3.13, nojax, docs). JAX three-way probe (NumPy / xp=jnp / jit with galaxies traced, grid closed over) green with a MassField in the plane; no explicit pytree registration needed — the `jax/registration.py` walker registers it like any member. `af.Model(ag.MassField, redshift=0.5, shear=af.Model(ag.mp.ExternalShear))` composes (5 params), instantiates and renders in `model.info` under a `fields` collection — the shape phase 2's analysis slot consumes.
- traps: (1) `instance_as_dict` puts `af.ModelObject`'s `label` into `arguments`, so `from_dict(field.dict())` calls `MassField(label=None, …)`; `Galaxy` swallows it via its blanket `setattr`, but a strict MassProfile check rejects it — `MassField.__init__` pops `label` and hands it to `ModelObject.__init__(id_=None, label=None)` (commented in the source). (2) The prompt claimed `jax/registration.py` registers `Galaxy` with `no_flatten=("redshift",)`; it does not — the walker calls `register_instance_pytree(cls)` plainly, and `redshift` flattens as an ordinary leaf and round-trips. (3) The literal jit probe with the `Grid2D` as a traced argument fails identically on baseline with no MassField anywhere (`DynamicJaxprTracer has no attribute array` at geometry_profiles.py:419; returning `VectorYX2D` is not a valid JAX type) — pre-existing; the probe of record traces `galaxies` and closes over the grid, as `complete/2026/07/public-register-galaxies-classes.md` did. (4) `register_galaxies_classes` is reached as `from autogalaxy.jax import …`, not `ag.jax.…` (`__getattr__` only lazily exposes `plot` and `interop`). (5) The prompt sat on an unmerged Mind ledger branch (`claude/shear-galaxy-idiom-propagation-bq6yz3`) whose auto-merge failed three times on generated-dashboard conflicts; it landed by merging into this session's branch and regenerating.
- notes: Shipped from a web-github session (no task worktree; PyAutoGalaxy attached with push access and cloned at /home/user/pyautogalaxy; PyAutoFit/PyAutoArray/PyAutoNerves cloned read-only and pip-installed editable; Heart not installed, so the ship gate was the full-suite pytest fallback). Implementation delegated to an Opus subagent from a Fable architect session; the judgment tier reviewed the diff and made two polish edits (list-rejection example names `al.mp.ExternalShear()`, `profile_dict` drops the `Pixelization` clause). Workspace impact: Added-only API, no migration; workspace adoption is the epic's phases 3–5 behind phase 2 (`draft/feature/autolens/mass_field_integration.md`, now unblocked on merge; a release is not required for it since CI runs the same-named library branch). Session shadow row: `Consequence: glance`, not `notify` — no row.

## Original prompt

# MassField: a standalone, MassProfile-only container for external shear, mass sheets and external potentials

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- cluster
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: glance
Witness: `ag.MassField(redshift=0.5, shear=ag.mp.ExternalShear(0.05, 0.05)).deflections_yx_2d_from(grid)` is `np.array_equal` to the same profile on an `ag.Galaxy`; `isinstance(field, ag.Galaxy)` is False; `ag.MassField(redshift=0.5, bulge=ag.lp.Sersic())` raises; identifier pin: `af.Collection(galaxies=af.Collection(lens=af.Model(ag.Galaxy, redshift=0.5, mass=af.Model(ag.mp.Isothermal), shear=af.Model(ag.mp.ExternalShear)))).identifier` equal on `main` and on the branch; `pytest test_autogalaxy -q -n auto` green; `git diff` touches no `autogalaxy/config/priors/` file.
Review-minutes: 5
Unattended: ready
Epic: mass-field
Phase: 1
Filed: 2026-09-17
Issued: 2026-09-17

Add `MassField` to PyAutoGalaxy: the redshift-bearing container for the mass
components that describe the tidal field of everything *outside* the modelled
system — `ExternalShear`, `MassSheet`, `ExternalPotential` — so a model can say
"this is a property of the system" instead of pinning the field to one galaxy.
It is **its own thing, not a `Galaxy` subclass**. The design, prior art and the
backwards-compatibility invariant are in the epic ledger
`complete/archive/epics/mass_field_epic.md`; read it first.

## What to build

1. **Share the mass sums, do not copy them.** `@PyAutoGalaxy/autogalaxy/galaxy/galaxy.py`
   implements `has`, `cls_list_from`, `deflections_yx_2d_from`,
   `convergence_2d_from`, `potential_2d_from` and the `deflections_memo`
   routing. Extract them, behaviour-preservingly, into a mixin
   (e.g. `autogalaxy/galaxy/mass_aggregate.py: MassProfileAggregate`) that
   `Galaxy` keeps using and `MassField` also uses. `Galaxy`'s import path,
   constructor, `dict()`/`to_dict` output and `__eq__`/`__hash__` are unchanged
   — the identifier pin in the Witness is the proof, run it before and after.
2. **`@PyAutoGalaxy/autogalaxy/galaxy/mass_field.py`** — `class MassField(af.ModelObject, MassProfileAggregate)`.
   - `__init__(self, redshift, **kwargs)`: validate the redshift the way
     `Galaxy` does (`validate.validate_redshift`), reject lists with the same
     message, then require every component to be a `MassProfile`
     (`autogalaxy.profiles.mass.abstract.abstract.MassProfile`); a
     `LightProfile`, `Pixelization`, `Regularization` or anything else raises
     `exc.GalaxyException` naming the offending key and what a `MassField` is
     for. Any `MassProfile` is accepted (a user may want an NFW "environment"
     halo as a field); the docstring names the three intended ones.
   - **Zero-light interface**, so a tracer plane can hold it beside galaxies:
     `has(cls)` is False for any non-mass class; `image_2d_list_from` returns
     `[]`; `image_2d_from` returns zeros of the grid's shape; whatever else
     `Galaxies` / `OperateImageGalaxies` call on a member (read
     `autogalaxy/galaxy/galaxies.py` and `autogalaxy/operate/image.py` and list
     them in the PR) gets the no-op that makes a field contribute nothing to
     light and everything to mass. Do not inherit `OperateImageList`.
   - `__repr__`: `MassField(redshift=..., <component names>)`; `__eq__`/`__hash__`
     following `Galaxy`'s pattern (it is used as a dict key nowhere today, but
     keep it hashable).
   - `dict()`/`to_dict` round trip via `autonerves.dictable` rebuilds a
     `MassField` (test it).
3. **Export** `ag.MassField` from `@PyAutoGalaxy/autogalaxy/__init__.py` beside
   `Galaxy` / `Galaxies`.
4. **JAX pytree registration** — `@PyAutoGalaxy/autogalaxy/jax/registration.py`
   registers `Galaxy` with `no_flatten=("redshift",)`; register `MassField` the
   same way in the same walker. Measure with the three-way probe from
   `complete/2026/07/public-register-galaxies-classes.md` using a `MassField`
   in the `Galaxies` list.
5. **Tests** — `@PyAutoGalaxy/test_autogalaxy/galaxy/test_mass_field.py`:
   construction with each of the three sheets and all three; rejection of
   light profiles / pixelizations with the named key in the message;
   `isinstance(field, Galaxy)` False; field equality of deflections /
   convergence / potential against the same profiles on a `Galaxy`;
   `image_2d_from` zeros; `Galaxies([galaxy, field])` aggregate sums (a plane
   can hold it); `to_dict`/`from_dict` round trip type; `__repr__`; the
   identifier pin as a regression test against a hard-coded value captured on
   `main` **and** a comment saying which model produced it.
6. **Docs** — `@PyAutoGalaxy/docs/api/galaxy.rst` gains `MassField`; a short
   "External fields" paragraph in the galaxy overview page explaining when to
   use it and that the galaxy-attached form remains supported.

## Hard constraints

- `Galaxy`'s public behaviour is unchanged (import path, constructor, dict
  output, hash/eq); the mixin extraction is the only edit to `galaxy.py` and
  the identifier pin proves it moved nothing that PyAutoFit hashes.
- No deprecation warning anywhere for sheets on a `Galaxy`.
- No prior config changes (`autogalaxy/config/priors/`).

## Out of scope (later phases)

The tracer's `fields=` argument, the analysis slot, COOLEST, the LOS sampler
and the `model_util` helper are phase 2; workspaces are phases 3–5.
