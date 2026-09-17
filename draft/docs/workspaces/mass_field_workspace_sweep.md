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
Witness: `grep -rn "shear_galaxy" scripts/` returns nothing; `grep -rn "al.MassField" scripts/multi_galaxy | wc -l` covers every former `shear_galaxy` site; the traced grid of `multi_galaxy/modeling.py`'s model at fixed instance values is `np.allclose` to the pre-change one; smoke suite green; notebooks and `workspace_index.json` regenerated; `check_navigator.py --root <checkout> --banners=fail` run from the parent directory.
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
   `modeling.py`, `slam.py`, `simulator*.py` (`shear_galaxy_simulated` →
   `al.MassField(redshift=..., shear=al.mp.ExternalShear(...))`), and
   `features/**` including every SLaM stage that chains
   `shear_galaxy=<result>.model|instance.galaxies.shear_galaxy`. The model key
   becomes `mass_field`; the `__External Shear__` prose in `modeling.py` is
   rewritten around the class (it is the reference text the group phase reuses,
   so get it right here). `n_main_from` counts the `lens_` prefix and is
   unaffected; say so in the prose where it explains what is not counted.
3. **`scripts/imaging/features/advanced/los_halos/*`** — the
   `hasattr(g, "mass_sheet")` sheet detection becomes `isinstance(g, al.MassField)`
   once the sampler emits fields (phase 2); prose "each plane includes a MassSheet"
   → "each plane carries a `MassField` with a negative-κ sheet".
4. **`scripts/imaging/`** — *not* migrated (epic Decisions). Add one paragraph
   to its `__External Shear__` prose pointing at `MassField` for multi-deflector
   systems.
5. **Positional-index audit** — grep `tracer.galaxies[` under `multi_galaxy/`;
   renaming the key does not move the entry, but confirm nothing indexes by the
   old name.

## Acceptance

Witness above. Regenerate notebooks with PyAutoHands; run `scripts/check_sizes.sh`
before committing (bulk edit across many files). Run the navigator check from
the parent directory, never `--root .` from inside the workspace.
