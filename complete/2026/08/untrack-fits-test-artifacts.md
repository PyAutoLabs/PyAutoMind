## untrack-fits-test-artifacts
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/494
- completed: 2026-08-27
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/495 (merged as a5d718e)
- repos:
  - PyAutoArray: feature/untrack-fits-test-artifacts

### What shipped

`test_autoarray` wrote test *output* into tracked paths, so any change to the
autonerves FITS writer rewrote a committed binary and dirtied the tree for every
contributor. PyAutoArray#483 demonstrated it: the PyAutoNerves#155 header-comment
fix (`[""]` -> `""`) silently modified
`structures/arrays/files/array/output_test/array.fits` the moment the autonerves
floor moved to a release carrying it -- identical cards, values, data and byte
size, but a modified tracked file that had to be committed into an unrelated PR.

The durable fix, applied uniformly rather than file-by-file again: the nine tests
that wrote into an `output_test/` directory now take pytest's `tmp_path` and drop
their `rmtree`/`makedirs` preamble; the 13 exposed artifacts are untracked and
deleted; the two file-by-file `.gitignore` lines are replaced by
`test_autoarray/**/output_test/` as a backstop. **After a full run no
`output_test/` directory is created anywhere in the source tree** -- the defect is
closed at the source, not masked by an ignore rule.

20 files, +48 / -106. Suite: 1177 passed, 55 skipped -- identical to the
pre-change baseline -- run twice in a row from a clean checkout with
`git status --porcelain` unchanged after each.

### Traps

- **The prompt's inventory described the symptom, not the state.** Of the 13
  tracked files only **one** was a live output (the `array.fits` #483 flipped).
  The other 12 were orphans: no test referenced their paths, and a repo-wide grep
  for their basenames returned nothing. They were residue from tests deleted long
  ago -- as were the two `.gitignore` lines, gravestones for one such test.
  Re-derive which inventory entries are still load-bearing before acting.
- **A fixture that looks dead may not be.** The plan called
  `dataset/imaging/test_dataset.py::make_test_data_path` never-requested and
  proposed deleting it; three tests do request it, and a truncated `grep | head`
  hid them. Deleting it broke those three -- caught by the first verification run,
  one step earlier than the prompt's "run the suite twice" guard was aimed at.
  They now take `tmp_path`, which was the plan's real intent.
- **The repo has three inconsistent ignore conventions**, not two: root
  file-by-file lines, root directory lines, and **nested `.gitignore` files
  containing `*`** (`test_autoarray/structures/files/`,
  `test_autoarray/util/files/array/`). The third is why
  `structures/files/output_test/data.fits` looked exposed in the plan but was in
  fact already covered. Not consolidated here; worth knowing before the next
  gitignore judgement in this repo.
- **`test_uniform_1d` and `test_uniform_2d` both `rmtree`'d the same shared
  output directory** -- a cross-module ordering hazard nobody had filed.
  `tmp_path` removes it incidentally.

### Notes

- Shipped from a web session: no local worktree, no `gh`; issue, PR and merge all
  driven through the GitHub MCP surface. PyAutoHeart was not reachable, so the
  readiness gate ran through the documented fallback (per-repo suite, any failure
  treated as RED). PyAutoArray was attached to the session mid-run via `add_repo`.
- Mind state for this task was pushed to `claude/untrack-fits-test-artifacts-r1eard`
  rather than `main`, per the session's branch instruction -- so
  `dashboard_refresh.yml` does not heal the render until that branch merges.
- Sibling sweep (the prompt's scope item 4) done and deliberately **not** widened
  into #495. PyAutoGalaxy is clean -- no `output_test/`, zero tracked artifacts,
  global `data_temp/` ignore. PyAutoLens has no tracked artifacts either, so this
  defect was autoarray-only, but its `.gitignore` covers only the `integration/`
  copies of `data_temp/` while its tests write to
  `test_autolens/{imaging,interferometer}/data_temp/`; the teardown `rmtree` hides
  the leak unless a run fails. Filed as
  `draft/maintenance/libraries/autolens_data_temp_not_ignored.md`.

## Original prompt

# Untrack the generated FITS test artifacts in autoarray

Type: maintenance
Target: libraries
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-22 (backfilled from git)
Issued: 2026-08-27

Filed 2026-08-23 from the PyAutoArray#482/#483 floor bump, which tripped over
this. Not a bug — a git-hygiene defect that converts unrelated upstream changes
into binary diffs.

## The defect

`test_autoarray` writes test *output* into **tracked** paths. The tests rmtree
the directory, recreate it, write a FITS, and read it back — the file is never an
input expectation, yet it is committed. So any change to the autonerves FITS
writer rewrites a tracked binary and dirties the tree for every contributor.

Demonstrated on #483: the PyAutoNerves#155 header-comment fix (`[""]` -> `""`)
silently changed `test_autoarray/structures/arrays/files/array/output_test/array.fits`
the moment the autonerves floor moved to a release carrying it —

```
HEAD    : PIXSCAY =                  1.0 / ['']
WORKING : PIXSCAY =                  1.0
```

— identical cards, values, data and byte size, but a modified tracked file that
had to be either committed into an unrelated PR or left dirtying the tree. It
was committed there; that was the least-bad option, not a good one.

## Why this is worth fixing rather than absorbing

The convention **already exists and is applied inconsistently**. `.gitignore`
lines 9-10 name two individual generated files:

```
test_autoarray/dataset/files/array/output_test/uv_wavelengths.fits
test_autoarray/dataset/files/array/output_test/visibilities.fits
```

so someone already hit this and patched the two files in front of them rather
than the pattern. **13 tracked files** across five `output_test/` directories are
still exposed:

```
test_autoarray/dataset/files/array/output_test/noise_map.fits
test_autoarray/dataset/files/arrays/output_test/{background_noise_map,background_sky_map,
  exposure_time_map,image,noise_map,poisson_noise_map,psf}.fits
test_autoarray/structures/arrays/files/array/output_test/array.fits
test_autoarray/structures/arrays/files/output_test/{array,masked_array}.fits
test_autoarray/structures/arrays/files/output_test/values_test.dat
test_autoarray/structures/arrays/files/values/output_test/values_test.dat
```

Writers: `structures/arrays/test_uniform_2d.py:201-211`,
`structures/test_visibilities.py:96-107`, `mask/test_mask_2d.py:417`,
`dataset/interferometer/test_dataset.py:140`, `dataset/imaging/test_dataset.py:18`,
`structures/arrays/test_uniform_1d.py:12`.

## Suggested scope

1. Pick one of the two fixes and apply it uniformly — do **not** patch
   file-by-file again:
   - **`tmp_path`** (preferred): the tests already rmtree/recreate their output
     dir, so pytest's `tmp_path` fixture is a near-drop-in and removes the
     tracked path entirely. This is the durable fix.
   - **`.gitignore` the directories** (`test_autoarray/**/output_test/`) plus
     `git rm --cached` the 13 files, if converting the tests is judged too wide.
     Cheaper, but leaves the tests writing into the source tree.
2. Confirm each candidate file is genuinely output before untracking it. The
   inventory above was read off the writers, but
   `structures/arrays/test_uniform_1d.py:12` *reads* from an `output_test` path —
   check whether it consumes a file another test produced (ordering dependency)
   or a committed one. If any file is a real input, it is not in scope and should
   be moved out of `output_test/` instead.
3. Verify the suite passes from a clean checkout **and** twice in a row (a test
   that silently depended on a committed artifact will fail on the first run
   after untracking, not the second).
4. Leave the sibling repos alone. PyAutoGalaxy/PyAutoLens likely share the
   pattern; check, and file separately rather than widening this.

## Note

The equivalent problem in the workspaces was solved differently — an autouse
conftest fixture per repo (see `complete/2026/08/small-datasets-regime-stamp.md`,
"Committed FITS fixtures became regime-DEPENDENT"). That solved *regime*
dependence of fixtures that are genuinely inputs. This is the different case:
files that are outputs and should not be tracked at all.
