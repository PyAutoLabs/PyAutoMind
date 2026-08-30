# PyAutoLens test `data_temp/` write paths are not gitignored

Type: maintenance
Target: autolens
Repos:
- @PyAutoLens
Themes:
- hygiene
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-27

Filed 2026-08-27 from the sibling-repo sweep required by
shipped task `untrack-fits-test-artifacts` (PyAutoArray#494, record
`complete/2026/08/untrack-fits-test-artifacts.md`), whose
scope note said: "Leave the sibling repos alone. PyAutoGalaxy/PyAutoLens likely
share the pattern; check, and file separately rather than widening this."

Scope is **PyAutoLens only**. PyAutoArray and PyAutoGalaxy appear below as the
comparison that isolates the defect, not as repos this task touches.

## What the sweep found

The autoarray defect itself — generated FITS committed into **tracked** paths —
does **not** exist in either sibling. Both track zero test-output artifacts:

| Repo | Tracked output artifacts | `data_temp/` ignored? |
|------|--------------------------|------------------------|
| PyAutoGalaxy | 0 | yes — `.gitignore:1` has a global `data_temp/` |
| PyAutoLens | 0 | **partially** — see below |

Neither repo uses the `output_test/` directory name at all, so there is nothing
to untrack.

## The smaller defect that is real

PyAutoLens' `.gitignore` covers only the *integration* copies:

```
test/integration/data_temp/
test_autolens/integration/data_temp/
```

but the tests that actually write FITS put them elsewhere —
`test_autolens/imaging/data_temp/simulate_and_fit/` and
`test_autolens/interferometer/data_temp/simulate_and_fit/`
(`test_simulate_and_fit_imaging.py:35,844`,
`test_simulate_and_fit_interferometer.py:37`). Confirmed against a clean
checkout at `c1bba66`:

```
$ git check-ignore -v test_autolens/imaging/data_temp/simulate_and_fit/image.fits
NOT IGNORED
```

The tests `shutil.rmtree` their `data_temp/` at the end, so on the happy path
this is invisible. On a **failing or interrupted** run the teardown does not
reach, and the artifacts linger as untracked files in a contributor's tree —
exactly when a developer is least well placed to tell noise from signal.

PyAutoGalaxy is unaffected because its global `data_temp/` line catches every
location.

## Suggested scope

Pick one, matching whichever the repo prefers:

1. **`tmp_path`** (consistent with the autoarray fix, PyAutoArray#494) — convert
   the three `simulate_and_fit` writers to pytest's `tmp_path` so no test writes
   into the source tree. Note these tests build real datasets and re-read them,
   so verify the round-trip still passes.
2. **One `.gitignore` line** — replace the two integration-only lines with a
   global `data_temp/`, as PyAutoGalaxy already has. A one-line fix that leaves
   the tests writing into the tree.

Either way, verify the suite passes twice in a row with `git status` clean after
each, and check no `data_temp/` survives a **failed** run.

## Note

Deliberately kept separate from PyAutoArray#494 rather than widening it — the
two repos share a family resemblance, not the same defect. #494 removed 13
tracked binaries; this one removes an untracked-file leak on the failure path.
