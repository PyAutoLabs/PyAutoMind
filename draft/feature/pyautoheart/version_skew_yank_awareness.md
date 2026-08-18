# version_skew: flag a floor that names a PyPI-yanked release

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised

## Why

The `version_skew` Heart leg (reworked under build-chain #155 Phase 4 task 2,
PyAutoHeart#96) enforces "a floor must name an *installable* release" only
against **local git tags**: UNSATISFIABLE fires when
`version.minimum_library_version` exceeds the newest `YYYY.M.D.B` release tag.
It cannot see the other way a floor goes bad — the release it names being
**yanked on PyPI afterwards** (as `2026.7.6.649` was; that yank is what
originally exposed the "floors named a yanked release" bug that this check now
half-guards). The gap is acknowledged in the check itself
(`heart/checks/version_skew.py:33`: "a release that was later *yanked* on PyPI —
that needs the PyPI API, not git tags") and was left unowned when the Phase 4
tracker (`complete/2026/08/release-version-sync-back-to-main.md`) retired.

## Scope

- Extend `version_skew` (or add a sibling non-tick check, if network access
  disqualifies it from the tick path — the current check is deliberately
  local-tags-only, no import/network) to query the PyPI JSON API for the
  floor's version and flag `yanked: true` per package.
- Verdict shape should mirror the existing one: a yanked floor is the same
  class of defect as UNSATISFIABLE (no installable version satisfies "exactly
  this floor"), but the floor semantics (>=) mean a yanked floor with newer
  non-yanked releases still resolves — decide whether that is RED, YELLOW, or
  informational, and record the reasoning.
- Offline/API-failure behaviour must be UNKNOWN/STALE, never a false RED —
  match how the tag-based check treats unresolvable repos.

## Constraints

- Do not slow the readiness tick: if the PyPI call cannot be cached or made
  optional, keep it out of the tick path (nightly / on-demand only).
- Fork (b) of the version model stands (mains authoritative, floors + tags +
  wheels as the live signals — see the retired tracker). This check reads
  state; it must not resurrect any commit-back behaviour.
