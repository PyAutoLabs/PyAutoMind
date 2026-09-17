# autolens_workspace: adopt MassField — guides, multi_galaxy (main + features + SLaM), LOS halos

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- cluster
- notebooks
Difficulty: medium
Autonomy: safe
Priority: normal
Consequence: notify
Witness: `grep -rn "shear_galaxy" scripts/` returns nothing; every former `shear_galaxy` site is a `fields=af.Collection(field=af.Model(al.MassField, ...))` slot beside `galaxies=`, and no `MassField` appears inside a `galaxies` collection; the traced grid of `multi_galaxy/modeling.py`'s model at fixed instance values is `np.allclose` to the pre-change one; smoke suite green; notebooks and `workspace_index.json` regenerated; `check_navigator.py --root <checkout> --banners=fail` run from the parent directory.
Review-minutes: 5
Unattended: ready
Epic: mass-field
Phase: 3
Blocked-by: PyAutoGalaxy and PyAutoLens releases carrying phases 1–2 reaching the installed stack (the workspace follows the released library, not main)
Filed: 2026-09-17

Third phase of `draft/feature/autogalaxy/mass_field_epic.md` (read it first):
move the workspace's *existing* separate-shear idiom from the shear-only
`Galaxy` named `shear_galaxy` (autolens_workspace#378) to `al.MassField`, and
document the class where the sheet profiles are taught.

## Scope

1. **`scripts/guides/profiles/mass.py`** — the "Mass Sheets" section: introduce
   `al.MassField` as the container for `ExternalShear`, `MassSheet`,
   `ExternalPotential`, show `al.model_util.mass_field_from(lens=..., potential=True)`
   and the centre tie, and state plainly that a sheet on a `Galaxy` remains
   supported and is the right form for a single-galaxy lens.
2. **`scripts/multi_galaxy/`** — every `shear_galaxy` site: `start_here.py`,
   `modeling.py`, `slam.py`, `simulator*.py` (`shear_galaxy_simulated` becomes
   `al.MassField(redshift=..., shear=al.mp.ExternalShear(...))` passed as
   `al.Tracer(galaxies=[...], fields=[field])`), and `features/**` including
   every SLaM stage that chains `shear_galaxy=<result>.model|instance.galaxies.shear_galaxy`.
   The model idiom is the field in its own slot —
   `af.Collection(galaxies=af.Collection(**lens_dict, source=source),
   fields=af.Collection(field=af.Model(al.MassField, redshift=0.5,
   shear=af.Model(al.mp.ExternalShear))))` — and SLaM stages chain
   `fields=<result>.model|instance.fields`. The `__External Shear__` prose in
   `modeling.py` is rewritten around the class and the slot (it is the reference
   text the group phase reuses, so get it right here): a field is a container
   like a galaxy (shear + sheet + potential in one), several fields means
   several planes, and `tracer.galaxies` never holds one. `n_main_from` counts
   the `lens_` prefix over `galaxies` and is unaffected; its docstring's "not
   counted" list drops `shear_galaxy`.
3. **`scripts/imaging/features/advanced/los_halos/*`** — the sampler now
   returns the sheets as fields (phase 2): the tracer is built as
   `al.Tracer(galaxies=[lens, source] + halos, fields=sheets)`, the
   `hasattr(g, "mass_sheet")` detection becomes a loop over `tracer.fields`,
   and the prose "each plane includes a MassSheet" becomes "each plane carries
   a `MassField` with a negative-κ sheet".
4. **`scripts/imaging/`** — *not* migrated (epic Decisions). Add one paragraph
   to its `__External Shear__` prose pointing at `MassField` for multi-deflector
   systems.
5. **Positional-index check** — grep `tracer.galaxies[` under `multi_galaxy/`;
   removing `shear_galaxy` from `galaxies` *shifts* every index that came after
   it (typically `source`), so each hit is re-checked and preferably made
   named access. Fields never appear in `tracer.galaxies`, so this is the last
   time these offsets move.

## Acceptance

Witness above. Regenerate notebooks with PyAutoHands; run `scripts/check_sizes.sh`
before committing (bulk edit across many files). Run the navigator check from
the parent directory, never `--root .` from inside the workspace.
