# Propagate the shear_galaxy-at-(0,0) idiom to group/ and cluster/

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- cluster
- notebooks
Difficulty: small
Autonomy: safe
Consequence: judge
Review-minutes: 20
Unattended: ready
Priority: normal
Parent: complete/2026/07/multi-galaxy-imaging-parity.md
Filed: 2026-07-30 (backfilled from git)

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
