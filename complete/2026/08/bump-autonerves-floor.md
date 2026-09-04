- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/482
- completed: 2026-08-23
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/483 (merged 0f75c3d)
- workspace-pr: none — no workspace change needed
- superseded-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/481 (closed unmerged 2026-09-04 — the same floor bump, opened a few hours earlier from the release session recorded in `pyautonerves-release-for-regime-stamp.md`; #483 shipped it)

The floor `autonerves>=2026.8.22.1` predated the SMALLDAT regime stamp
(PyAutoNerves#153/#154), so a PyPI-installed autoarray resolved an autonerves
whose writer emits no card: `should_simulate` read the absent stamp as "unknown"
and fell back to the shape heuristic, which cannot see capped interferometer
datasets — the case the stamp exists for. Bumped to `2026.8.23.1`.

**THE BLOCKER CLEARED ITSELF THE SAME DAY.** The prompt was filed 2026-08-22
blocked on "the PyAutoNerves release". `autonerves 2026.8.23.1` was uploaded
2026-08-23T00:41:41Z, hours before this ran. Worth remembering as a pattern: a
prompt parked on an external release is worth re-checking on sight rather than
trusting its `Status:`.

**Verified by unpacking both wheels, not by reading commit dates.** The prompt
named commits `39014b6` and `0ecefa0` and said "the release that carries them is
the floor to name" — but commit membership is not the same claim as wheel
contents. Unpacked from PyPI: `2026.8.22.1` has neither
`stamp_small_datasets_regime` nor `SMALL_DATASETS_HEADER_KEY` and still writes
the `[""]` header comment; `2026.8.23.1` has both plus the `""` fix. No release
sits between them, so it is provably the first.

**THE PROMPT UNDERSTATED THE DUPLICATION ITEM.** It framed converting
`dataset_util.SMALL_DATASETS_HEADER_KEY` to an import as "optional and low
value... decide deliberately". It is not optional in either direction: the
comment justifying the duplication *names the floor* ("floors autonerves at a
release that predates the stamp, so an import would hard-fail"), so bumping the
floor makes that comment **factually false**. The comment had to change whatever
was decided about the literal.

Decision: **keep the duplication, replace the reason.** A floor constrains
dependency *resolution* only. An editable checkout, `pip install --no-deps`, or a
hand-built virtualenv (the HPC one) can still put a pre-stamp autonerves on the
path. Under the literal that yields "card absent" -> shape fallback, the safe
direction and the same path every pre-stamp dataset on disk already takes. Under
an import it is an `ImportError` at module load. Silent-safe beats hard-fail; the
literal is not debt, it is a deliberate decoupling.

**TRAPS**
- The other floor reason is still load-bearing. PyAutoLens#687/#702 (JAX in
  autonerves' base dependencies) shares this pin; both versions carry
  `jax>=0.7.0` in base `Requires-Dist`, so that condition has been met since
  `2026.8.22.1` and its "bump once it exists" phrasing was stale. Both reasons
  are now stated. Dropping either silently re-opens the other's failure mode.
- Do NOT remove the shape fallback or `_is_capped_at_the_current_cap`. The floor
  governs what a fresh install *writes*; every dataset already on disk is
  unstamped and depends on those paths.
- A `>=` floor does not constrain the upper end, so this bump reaches no new jax
  range — `2026.8.23.1` widens its own cap to `<0.12.0`, but that was already
  resolvable under the old floor. The bump raises the minimum only.

**A TRACKED TEST ARTIFACT CHANGED UNDER US.** Running the suite dirtied
`test_autoarray/structures/arrays/files/array/output_test/array.fits` — the
newly-floored autonerves drops the `/ ['']` comment literal (PyAutoNerves#155),
so the committed copy no longer matched what a compliant install writes:

```
HEAD    : PIXSCAY =                  1.0 / ['']
WORKING : PIXSCAY =                  1.0
```

Verified cosmetic (identical cards, values, data, byte size 5760 -> 5760) and
committed, because the file is test *output* — `test_uniform_2d.py:201-208`
rmtrees the directory and rewrites it — so leaving it stale would dirty the tree
on every run under the new floor. Only 1 of 61 tracked `.fits` was affected,
because only it carries `header_dict` comment cards.

This is a different problem from the one the parent task solved. That one fixed
fixtures that are genuinely *inputs* and became regime-dependent, via an autouse
conftest fixture. This is files that are *outputs* and should not be tracked at
all — and the convention already exists, applied inconsistently: `.gitignore`
names two individual generated files under `dataset/files/array/output_test/`
and misses thirteen others.

**Follow-up filed**
- `draft/maintenance/libraries/untrack_generated_fits_test_artifacts.md` — the
  13 tracked output files across five `output_test/` directories, their writers,
  and the two candidate fixes (`tmp_path` preferred over widening `.gitignore`).
  Notes that `structures/arrays/test_uniform_1d.py:12` *reads* from an
  `output_test` path and must be checked for a real input before untracking.

**Method note.** Filed via `/intake`, which classified it low-confidence to
`triage/` at difficulty large (score 7) off a long description, and again at
medium off a short one. Re-homed by hand to `maintenance/libraries` and the body
written from a real inventory (`git ls-files | grep output_test` plus the
writers). The sizing inflation on prose-dense input is the same effect recorded
in the parent task and in `complete/2026/08/jax-grad-smoke-timeout-budget.md`.

## Original prompt

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
