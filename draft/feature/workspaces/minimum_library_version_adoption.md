# Adopt version.minimum_library_version in workspace configs

Type: feature
Target: workspaces
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

## Context

Follow-up to PyAutoConf#119 (merged 2026-07-08): `check_version` now enforces
a compatibility floor, preferring `version.minimum_library_version` in
`config/general.yaml` over the legacy `workspace_version`/`version.txt`
records (which releases no longer write since PyAutoBuild#121).

## Scope

- Add `version.minimum_library_version` to `config/general.yaml` in
  autofit_workspace, autogalaxy_workspace, autolens_workspace, HowToFit,
  HowToGalaxy, HowToLens, euclid_strong_lens_modeling_pipeline — set to the
  oldest release whose API the workspace's scripts actually require (at
  adoption time: the first real release after 2026-07-08, since workspace
  mains depend on post-2026.7.6.649 API).
- Remove the now-dead `workspace_version` key and `version.txt` once the new
  key is in place (they are only read as fallbacks).
- Document the bump-deliberately rule in each workspace README/AGENTS: the
  floor moves only when scripts start needing new API, never per release.
- Coordinate claims: autofit_workspace (ep-examples-tests) and
  autolens_workspace (kxs-core) are claimed as of filing — serialise or wait.
- Best sequenced AFTER the first real release (Q1 on PyAutoBuild#118), so the
  floor value is an installable version.
