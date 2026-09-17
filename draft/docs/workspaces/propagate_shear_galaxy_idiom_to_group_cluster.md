# Propagate the separate-shear idiom to group/ and cluster/ — as MassField

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- cluster
- notebooks
Difficulty: medium
Autonomy: safe
Consequence: notify
Witness: `grep -rn "if i == 0 else None" scripts/group/` and `grep -rn 'kwargs\["shear"\]' scripts/group/` both return nothing — every former site holds the field in an `al.MassField` named `mass_field` at the system centre (0.0", 0.0") — the traced grid of `group/modeling.py`'s model at fixed instance values stays `np.allclose` to the pre-change one (presentational, per #378), the positional `tracer.galaxies[k]` sites re-offset or named, the smoke suite green, notebooks and `workspace_index.json` regenerated.
Review-minutes: 5
Unattended: ready
Priority: normal
Epic: mass-field
Phase: 4
Blocked-by: phase 3 (`draft/docs/workspaces/mass_field_workspace_sweep.md`) merged — group/ goes straight to `MassField`, never through the `shear_galaxy` interim
Parent: complete/2026/07/multi-galaxy-imaging-parity.md
Filed: 2026-07-30 (backfilled from git)

## Re-scoped 2026-09-17 (phase 4 of `draft/feature/autogalaxy/mass_field_epic.md`)

The `/start_dev` plan checkpoint for this prompt found the scope is the whole
`scripts/group/` subtree, not four sites, and the discussion it opened became
the MassField epic. What changed:

- **Target idiom is `al.MassField`, not a shear-only `Galaxy`.** Mirror
  `multi_galaxy/` *after* phase 3 (`mass_field = af.Model(al.MassField, redshift=0.5,
  shear=af.Model(al.mp.ExternalShear))` in `af.Collection(**lens_dict,
  mass_field=mass_field, source=source)`; SLaM stages chain
  `mass_field=<result>.model|instance.galaxies.mass_field`).
- **Full survey (autolens_workspace `30104f6`):** 30 loop-idiom sites in 19
  files — the four named plus `features/{linear_light_profiles, no_lens_light,
  multi_gaussian_expansion, pixelization (modeling, slam, adaptive, delaunay,
  cpu_fast_modeling), scaling_relation, advanced/{operated_light_profile,
  subhalo/detect, sky_background, shapelets}}`, nine of them SLaM chaining lines
  (`...lens_0.shear if i == 0 else None`); plus 12 sites in the
  `kwargs["shear"]` spelling in `features/advanced/{mass_stellar_dark,
  double_source_plane_lens}`, whose simulator (`mass_stellar_dark/simulator.py:133`)
  and hand-summed `fit.py:256` walkthrough move to a `MassField` in the tracer
  list the same way (dataset bit-identical); prose in ~25 files says "only
  `lens_0` carries an `ExternalShear`".
- **The one real trap:** `linear_light_profiles/{fit,modeling,slam}.py` and
  `multi_gaussian_expansion/source_science.py` index `tracer.galaxies[k]`
  positionally (`[0..3]`, `[n_main + i]`, `[n_lenses + 1 + n_extra + i]`);
  inserting the field shifts those offsets. Pick one rule (named access where
  the API allows, else re-offset) and run each of those scripts directly —
  most are not on the smoke roster (`group/modeling.py` and
  `group/features/group_halo/modeling.py` are; `group/start_here.py` is
  disabled under `PYAUTO_SMALL_DATASETS=1`).
- **Prose:** `group/modeling.py` gains the `__External Shear__` section phase 3
  writes for `multi_galaxy/modeling.py` (reuse verbatim, "lens pair" → "group"),
  its `__Contents__` line, the header bullet and the `__Main Galaxies and Extra
  Galaxies__` sentence; every "only `lens_0`" line across the subtree.
- **`cluster/` needs nothing** (no `ExternalShear` in any script; only a κ/γ
  magnification formula in `likelihood_function.py`). `group/features/group_halo`
  has no shear. `imaging/` stays galaxy-attached (epic Decisions). Record all
  three in the PR.
- Difficulty re-sized small → medium (declared small, Feature Agent derived
  large; the per-site change is mechanical and the numerics provably
  unchanged, which is what keeps it below large).

The original prompt follows unchanged for its rationale; where it says
`shear_galaxy`, read `mass_field`.

## Original prompt (2026-07-30)

`multi_galaxy/` now holds the system's external shear in its own
`shear_galaxy` at the system centre (0.0", 0.0") instead of attaching it to
`lens_0` (autolens_workspace#378, merged `77d70f48`). Its siblings on the
regime ladder were not changed, so the workspace is now inconsistent:

- `scripts/group/modeling.py:294` and `:422`
- `scripts/group/start_here.py:264`
- `scripts/group/slam.py:289`

all still use `shear=af.Model(al.mp.ExternalShear) if i == 0 else None`, and
their prose says "only the first main lens galaxy (`lens_0`) carries an
`ExternalShear`". `cluster/` should be surveyed too — grep showed no
`ExternalShear` in `scripts/cluster/*.py`, so it may need nothing.

## Why the multi_galaxy form is preferred

`al.mp.ExternalShear(gamma_1, gamma_2)` takes **no `centre` argument** — it is a
uniform field about the coordinate origin. Attaching it to one deflector invites
reading the fitted shear as a property of *that galaxy*, when it describes the
tidal field of everything outside the system. Holding it in its own galaxy makes
`model.info` and the posterior label it as a system property.

Verified in #378: numerically **identical** to attaching it to a deflector
(`np.allclose` on the traced grid), because the tracer sums every deflection
field. A shear-only `al.Galaxy(redshift=z, shear=...)` works in both the tracer
and the `af.Collection` model path. So this is a presentational change with no
result impact — which also means it needs no re-validation of science, only that
the scripts still run.

## Scope

1. Replace the `if i == 0 else None` shear with a `shear_galaxy` entry in the
   `af.Collection`, mirroring `multi_galaxy/{start_here,modeling}.py`.
2. Update the surrounding prose and `__Contents__` (multi_galaxy gained an
   `__External Shear__` section in `modeling.py` — reuse that wording).
3. Survey `cluster/` and the `group/features/*` subpackages for the same idiom.
4. Decide whether `imaging/` (a genuinely single-galaxy lens, where the shear on
   the one lens galaxy is unambiguous) should be left alone — it probably should.

## Acceptance

- Smoke suite green (`group/modeling.py`, `group/start_here.py`,
  `group/features/group_halo/modeling.py` are all smoke-enabled).
- Notebooks + `workspace_index.json` regenerated.
- Trap: run `check_navigator.py --root <checkout> --banners=fail` from the parent
  directory, not `--root .` from inside the workspace — the latter can pass where
  CI fails ([[feedback_worktree_base_drifts_from_main]]).
