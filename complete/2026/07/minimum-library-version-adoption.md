# minimum-library-version-adoption

- shipped: 2026-07-17 (autolens_workspace `21702119`; siblings adopted the same key)
- follows: PyAutoConf#119 (merged 2026-07-08) — `check_version` prefers `version.minimum_library_version` over the legacy records
- repos:
  - autofit_workspace, autogalaxy_workspace, autolens_workspace
  - HowToFit, HowToGalaxy, HowToLens
  - euclid_strong_lens_modeling_pipeline

## Summary

Every one of the seven repos in scope carries
`version.minimum_library_version: 2026.7.9.1` in `config/general.yaml`, with the
bump-deliberately rule documented inline as a comment on the key itself:

> The compatibility FLOOR: the oldest library release whose API this workspace's
> scripts require. Preferred over workspace_version (autonerves/workspace.py).
> Bump DELIBERATELY — only when a script starts needing new API — never per
> release. Must always name an INSTALLABLE (non-yanked) release.

## Verified 2026-08-08, all three legs of the prompt's scope

1. **The key is adopted in all 7** — confirmed by reading each repo's
   `config/general.yaml` on `main`, not inferred from one.
2. **The dead `workspace_version` key is gone.** The only surviving matches are
   the explanatory comment above and `workspace_version_check`, which is a
   *different* and still-live key (the documented bypass for `main`-branch
   clones, where mismatches are expected because `main` moves faster than
   releases).
3. **`version.txt` is gone** — `HTTP 404` on `main` for autolens_workspace,
   autofit_workspace and HowToLens.

## Bookkeeping note

Reconstructed 2026-08-08. This prompt was sitting in
`draft/feature/workspaces/` — the backlog folder — with `Priority: high`, while
the work had been fully delivered for three weeks. `draft/` is graded by no
check at all, which is how it stayed there; that gap is what
`lifecycle.py issues --drafts` now partially addresses, though only for the
minority of drafts that cite an issue (this one cited none).

## Original prompt

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
