# Mirror drifted library config keys into the workspace configs

Type: maintenance
Target: autogalaxy_workspace
Repos:
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Filed 2026-07-12 from a `/hygiene config` audit (recursive key-path diff of
each library `config/*.yaml` against its workspace counterpart).

## Why

Workspace configs override library defaults, so when a library gains a config
key the workspace config should usually gain it too (see the standing
"mirror new library config keys downstream" chore). 17 library keys are
currently absent from the matching workspace config. ~14 are worth mirroring;
a few are test/logging-namespace keys that may be intentional omissions —
review each rather than blanket-copying.

## Keys (grouped)

**autogalaxy_workspace / notation.yaml (12 — plot label + format entries for
newer mass-profile params, worth mirroring so plots label correctly):**
`label.label.c_2`, `label.label.concentration`,
`label.label.scaled_multipole_comps_0`, `label.label.scaled_multipole_comps_1`,
`label.label.virial_mass`, `label.label.virial_overdens`,
`label.label.zeroth_coefficient`, `label.label.zeroth_signal_scale`,
`label_format.format.input_multipole_comps_0`,
`label_format.format.input_multipole_comps_1`,
`label_format.format.virial_mass`, `label_format.format.virial_overdens`.

**Output toggles (worth mirroring — workspace overrides library output.yaml):**
- `autofit_workspace/config/general.yaml`: `output.search_internal`
- `autolens_workspace/config/general.yaml`: `output.fit_dill`

**Review — test/logging namespace, likely intentional omissions:**
- `autofit_workspace/config/general.yaml`: `test.check_likelihood_function`
- `autofit_workspace/config/logging.yaml`: `total_files_open`
- `autogalaxy_workspace/config/general.yaml`: `test.exception_override`

## Scope

- Add the worth-mirroring keys to the three workspace `config/*.yaml` files,
  matching the library value/default (keep keys snake_case-lowercase — autoconf
  lowercases yaml keys).
- For each test/logging key, confirm whether the workspace should carry it
  before adding; leave out any that are deliberately library-only.

## Verify

- Load each workspace with `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1` and confirm
  no config-key errors; a plot that uses a mirrored notation label renders it.
