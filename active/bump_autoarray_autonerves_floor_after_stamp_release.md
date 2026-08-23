# Bump autoarray's autonerves floor once the regime stamp is released

Type: maintenance
Target: libraries
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised

Filed 2026-08-22 as the step that makes PyAutoNerves#153/#154 actually take
effect. Blocked on the PyAutoNerves release, not on any code.

`autoarray/pyproject.toml:30` floors `autonerves>=2026.8.22.1`. That version is
currently the **newest release on PyPI** and it **predates the SMALLDAT regime
stamp**. So an autoarray installed from PyPI resolves an autonerves whose writer
emits no card at all: `should_simulate` sees an absent stamp, reads it as
"unknown", and falls back to the shape heuristic — which provably cannot see
capped interferometer datasets, the case the whole change exists for.

Nothing is broken by that; it is the designed degradation. But until the floor
names a stamped release, the fix is inert for anyone who installs rather than
runs from a checkout.

## Do this after PyAutoNerves is released

1. Bump `"autonerves>=2026.8.22.1"` to the first release containing the stamp
   (the commits are `39014b6` and `0ecefa0` on nerves main; the release that
   carries them is the floor to name).
2. Keep the comment block above the pin current — it currently explains a
   *different* historical reason for the floor (PyAutoLens#687/#702, JAX moving
   into autonerves' base dependencies). Add the stamp reason rather than
   replacing that one; both are now load-bearing.
3. **Do not remove the shape fallback in `should_simulate`.** The floor governs
   what a fresh install *writes* going forward; it says nothing about datasets
   already on disk, every one of which is unstamped. The fallback protects those
   and must stay. Same for `_is_capped_at_the_current_cap` on the capped branch.

## Note on the duplicated header key

`autoarray.util.dataset_util.SMALL_DATASETS_HEADER_KEY` duplicates the `"SMALLDAT"`
literal rather than importing it from autonerves, *because* of this floor — an
import would hard-fail against a legitimately-resolved older autonerves. Once the
floor names a stamped release that objection disappears and the import becomes
safe. Converting it is optional and low value: the duplication is documented, and
a stale reader degrades to the fallback, which is the safe direction. Decide
deliberately rather than by reflex.
