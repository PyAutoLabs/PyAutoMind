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
