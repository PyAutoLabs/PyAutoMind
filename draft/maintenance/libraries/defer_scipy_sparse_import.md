# Defer the eager scipy.sparse import in derivative_util (~0.10 s of import)

Type: maintenance
Target: libraries
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: safe
Priority: normal
Status: in-flight
Filed: 2026-08-22 (backfilled from git)

## Where this came from

Found 2026-08-22 while measuring the pynufft removal
(`draft/maintenance/libraries/remove_pynufft_legacy_transformer.md`). That task
assumed removing pynufft would take ~0.23 s off `import autoarray`. It takes
~10 ms. The reason is the real target:

`autoarray/operators/derivative_util.py:30` does

```python
from scipy.sparse import csr_matrix
```

at module scope. `scipy.sparse` costs **0.106 s cumulative** and is imported on
every `import autoarray`, whether or not anything touches a derivative
operator. pynufft's apparent 0.19 s was ~95 % this same shared subtree —
removing pynufft did not remove it, because `derivative_util` pulls it in
anyway.

## Evidence (Python 3.13, dev extras, median of 7 runs)

| | `import autoarray` |
|---|---|
| main, pynufft installed | 369.8 ms |
| pynufft removed | 359.9 ms |

`python -X importtime` on the pynufft-removed branch still shows
`scipy.sparse` at 0.106 s cumulative.

## Task

Defer the `csr_matrix` import into the functions that build the sparse
operators (the same pattern `transformer.py` already uses for `nufftax` via
`_load_nufftax()`). Check for other eager `scipy.sparse` importers before
assuming this is the only one — the win only lands if *no* module-scope import
of it survives on the `import autoarray` path.

Note the precedent in `transformer.py`: the deferral must survive unpickling in
multiprocessing workers, so hang it off the call sites rather than `__init__`
alone.

## Acceptance

- `python -X importtime -c "import autoarray" | grep scipy.sparse` is empty.
- Median `import autoarray` drops by ~0.10 s against the same measurement
  method above (record the before/after numbers in the PR).
- Full suite green; sparse-operator behaviour unchanged.

## Correction + result (implemented 2026-08-22, PyAutoArray#477)

**This prompt's own premise was wrong, in exactly the way the pynufft one
was.** Deferring `derivative_util.py:30` changed nothing: `scipy.sparse` was
never imported from there. Traced with a `sys.meta_path` hook:

```
autoarray/__init__.py:80
  -> inversion/mesh/mesh_geometry/delaunay.py:2   import scipy.spatial
    -> scipy/spatial/__init__.py:111              from ._kdtree import *
      -> scipy/spatial/_kdtree.py:4               from ._ckdtree import cKDTree
```

`scipy.spatial` (134 ms) pulls `scipy.sparse` (154 ms) transitively, so the
`csr_matrix` import was riding on a subtree already paid for. Deferring
`scipy.spatial` as well is what removes both — and is required to satisfy this
prompt's own acceptance criterion.

The general lesson, now hit twice: **a module's `importtime` cumulative figure
is not its exclusive cost.** Attributing a saving to a dependency requires
checking who else pulls its subtree in.

Result: `import autoarray` **464.4 ms -> 183.7 ms** (medians of 15 runs,
Python 3.13, dev extras) — a 281 ms saving, ~2.8x this prompt's ~0.10 s
estimate, because `scipy.spatial`'s own cost comes off too. Both greps are
empty. Suites green: autoarray 1179, autogalaxy 1103/1 skipped,
autolens 532/1 skipped.

Note `delaunay.py` already had local `import scipy.spatial` at two of its three
use sites — this deferral had been started and left half-done.
