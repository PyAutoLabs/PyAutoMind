# Delete PYAUTO_SMALL_DATASETS / PYAUTO_FAST_PLOTS from the autofit-only build profiles

Type: maintenance
Target: workspaces
Repos:
- autofit_workspace
- autofit_workspace_test
- HowToFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to autolens_workspace#321 (env_vars key-order sweep), which made the
profiles diffable and exposed this.

## Why

`PYAUTO_SMALL_DATASETS` and `PYAUTO_FAST_PLOTS` are **dead config** in every
autofit-only workspace — nothing that reads them is ever imported there.

- `PYAUTO_SMALL_DATASETS` is read only in PyAutoArray (`util/dataset_util.py`,
  `structures/grids/uniform_2d.py`, `mask/mask_2d.py`,
  `operators/over_sampling/over_sample_util.py`, `operators/convolver.py`),
  PyAutoGalaxy (`analysis/model_util.py`) and PyAutoLens. **Zero** occurrences
  in PyAutoFit or PyAutoNerves — not even a docstring.
- `PYAUTO_FAST_PLOTS` is read in `autoarray/plot/utils.py` and
  `autogalaxy/util/plot_utils.py`. In PyAutoFit it appears twice, both in prose
  (`autofit/non_linear/quick_update.py:71` and a test docstring) — never in an
  `os.environ` lookup.
- PyAutoFit does not import autoarray, and no script in `autofit_workspace`,
  `autofit_workspace_test` or `HowToFit` imports autoarray / autogalaxy /
  autolens. The reading code is never loaded.
- PyAutoFit's single `tight_layout()` is in `autofit/non_linear/live_viewer.py:102`,
  inside the interactive `plt.ion()` desktop viewer, which never runs headless in
  CI — so honouring `PYAUTO_FAST_PLOTS` there would buy nothing. Deleting the
  keys is the right call, not wiring them up.

The comments betray the copy-paste origin: an autofit config currently claims to
"reduce MGE gaussians" and skip "critical curve/caustic overlays", both lensing
concepts. Same bidirectional copy-paste pattern as the `no_run` dead-entry purge.

This does **not** violate the release-profile doctrine ("every var this profile
cares about gets an EXPLICIT value, not left absent") — autofit cares about
neither var. `autofit_workspace_test/config/build/env_vars_release.yaml` already
omits both and is the profile that had it right.

## Scope

Delete the two `defaults:` entries (8 lines total) from 4 files:

- `autofit_workspace/config/build/env_vars.yaml`
- `autofit_workspace/config/build/env_vars_release.yaml`
- `autofit_workspace_test/config/build/env_vars.yaml`
- `HowToFit/config/build/env_vars.yaml`

No `overrides:` block in any of these repos references either key, so the
deletion is contained to `defaults:`. Leave
`autofit_workspace_test/config/build/env_vars_release.yaml` alone (already
correct). Do not touch the galaxy/lens/cti workspaces, where both keys are live.

## Verify

- Resolved-env diff before/after via `resolve_clean()` in
  `PyAutoHands/autohands/validate_env_profiles.py` (empty base, every script x
  every profile). Unlike #321 this diff will **not** be empty, and that is the
  point: assert the delta is **exactly** the two keys disappearing from every
  script's env, with no other key added, removed or changed.
- `validate_env_profiles.py` verdicts unchanged from `main` per repo.
- `git diff --stat` shows nothing but `config/build/env_vars*.yaml`.
- Re-grep to confirm no autofit-only script reads either var.
