- Library: PyAutoFit
- Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1584 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoFit/pull/1592 (MERGED, merge commit `c03fa3f30`, head `57d838c38`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1592
- heart-ack: 2026-09-09 RED acknowledged in-session, single organism-scope reason "release validation FAILED (stage integrate)" (Release Integrate run of 2026-09-09T07:23Z) — nothing in this branch is in the release chain; no freeze window open
- Consequence: glance — no tier-`notify` shadow row

## What shipped

**Aggregating a tree of zipped results no longer has to double it.** `Aggregator.from_directory`
extracts every `.zip` it walks into a sibling directory beside the zip and leaves it there. For a
results tree that holds only zips — an HPC run, or any run with `output: remove_files` — that
permanently doubles the disk and the file count, with no opt-out and no automatic cleanup
(`remove_unzipped()` is opt-in and removes the *parent* of each search directory). Measured on a
three-result zip-only tree: the scan grew it **1.85x in bytes and 10x in files**.

`unzip_temporary=True` extracts into a temporary directory instead, and the scanned tree comes out
byte-identical.

- `autofit/aggregator/aggregator.py`: `from_directory` and `add_directory` take
  `unzip_temporary=False`. The inner `scan` gained `extract_temporary` (where to put the
  extraction) and `owner` (which extraction the outputs found there belong to); a new `scan_all`
  scans a directory and then each temporary extraction it produced, and is used for both the main
  call and the test-mode retry. `Aggregator` gained `close()`, `__enter__` and `__exit__`.
- `autofit/aggregator/search_output.py`: new `TemporaryExtraction`; the search-output constructors
  take `temporary_directory=None`.

**Layout is mirrored, not flattened.** Extraction goes to
`<tmp>/<path relative to the scan root>/<zip stem>`, so two zips of the same name in different
directories cannot collide, and — this is the part that matters — a grid search still pairs with
its children, because `grid_searches()` pairs on `is_relative_to` over their directories.

**Lifetime rides on the outputs, not the aggregator.** Every search output read out of an
extraction holds a reference to it, so the files live exactly as long as something can still read
them, and go when the last one is collected. That survives slicing, querying and grouping without
threading state through those constructors, and a search output kept after its aggregator is
dropped still loads.

## Traps worth keeping

- **Both classes turn a missing attribute into something else.** `Aggregator.__getattr__` returns
  an `AttributePredicate` and `AbstractSearchOutput.__getattr__` tries to load a pickle of that
  name from disk. A new attribute that is not set in `__init__` therefore does not raise — it
  silently becomes a query predicate or a disk read. Both new attributes are initialised in
  `__init__` for exactly this reason.
- **`tempfile.TemporaryDirectory` warns on implicit cleanup** (`ResourceWarning`), and implicit
  cleanup is the normal path here. `TemporaryExtraction` uses
  `weakref.finalize(self, rmtree, path, True)` instead; the callback must not close over `self`,
  or the object never becomes unreachable and the directory never goes.
- **A test that binds the owning object prevents the collection it asserts.** The first cleanup
  test held the `TemporaryExtraction` in a local and failed; it keeps only the path now.
- **Two pytest runs over the same fixture tree collide.** A background full-suite run overlapping
  a directory run produced five unrelated failures (an aggregate-images test, a reference test,
  two nautilus tests, an atomic-write test). All passed serially on both trees. Control-run before
  bisecting.

## Not taken

- **Reading members straight from the zip.** ~20 path-based loader and enumeration call sites
  across `file_output.py`, `search_output.py` and `aggregator.py`, plus lazy per-query re-reads
  that would re-open the archive repeatedly and regress the 2026-07 aggregator speed-up (#1375
  arc). Assessed and rejected before the plan was written.
- **Flipping the default** to temporary extraction — a one-line follow-up, left to the human.

## Cost

The new mode re-extracts on every call rather than once: 0.33s against 0.04s on a repeat call over
a 200-result tree, versus ~45 ms per result to parse samples. Extraction is not where aggregation
time goes.

## Verification

- Full PyAutoFit suite: **2553 passed, 2 skipped** (serial, clean run).
- Eight new tests in `test_autofit/aggregator/test_from_directory.py`: no sibling written, outputs
  identical to the default mode, removal on release and on `close()`, existing sibling still wins,
  mirrored layout for same-named zips, an output outliving its aggregator, and grid searches under
  temporary extraction. The aggregator tests carried no `.is_grid_search` fixture before this.
- CI on `57d838c38`: `unittest (3.12)`, `unittest (3.13)`, `unittest-nojax`, `docs-build` — every
  leg green, both runs completed, `mergeStateStatus` CLEAN at merge.

## Original prompt

# Aggregator: temporary-directory unzip mode so scraping `.zip` results does not permanently double disk usage

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Witness: `Aggregator.from_directory(<dir>, unzip_temporary=True)` on a directory holding only `<name>.zip` search outputs loads every search (`len(agg)`, `agg.values("samples")`, filters) identically to the default mode, writes nothing next to the zips (no `<name>/` sibling appears), and the extracted files are gone from the temp location once the aggregator and its search outputs are released; the default call is byte-for-byte unchanged in behaviour (extracts alongside, skips when the sibling exists); full PyAutoFit aggregator test suite green.
Consequence: glance
Review-minutes: 10
Unattended: ready
Filed: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1584
Issued: 2026-09-09

Original request (verbatim):

> The aggregator scrapes directories and enables things like .fits, .csv
> generation, and a while back we did profiling to speed it up. My
> understanding is that when it runs, it automatically unzips the .zip files
> results are stored in, which then doubles the amount of files and hard disk
> space in use, but I could be wrong on that. Is it possible for it to not
> unzip .zip files and still do all catalogue operations? Would this lead to
> slower performance?
>
> Ok lets go with the cheaper middle ground

Findings (2026-09-08 survey):

- `AbstractSearch.post_fit_output` always calls `paths.zip_remove()`
  (`autofit/non_linear/search/abstract_search.py`): the zip is always
  written; the unzipped folder is deleted only when `general.yaml`
  `output: remove_files` is true (forced true in HPC mode). Default laptop
  runs therefore already leave folder + zip before aggregation.
- `Aggregator.from_directory` → inner `scan()`
  (`autofit/aggregator/aggregator.py`) extracts every `.zip` it meets
  **permanently** to a sibling `<name>/` next to the zip, appends it to the
  `os.walk` `dirs` list, and skips extraction when the sibling already
  exists (perf commit `afa67edb6`, 2026-07-16). No `tempfile`, no cleanup,
  no opt-out kwarg (`from_directory(directory, completed_only, reference)`).
- `Aggregator.remove_unzipped()` is the only cleanup: opt-in, never called
  internally, and it `rmtree`s the *parent* of each search directory.
- Reading straight from the zip (no extraction) was assessed and rejected
  for now: ~20 path-based loader / enumeration call sites across
  `file_output.py`, `search_output.py`, `aggregator.py`, plus lazy per-query
  re-reads that would re-open the archive many times and regress the
  2026-07 speed-up. The "cheaper middle ground" chosen by the user is a
  temp-directory extraction mode with automatic cleanup.

Scope:

- Add an opt-in mode on `Aggregator.from_directory` (default = today's
  behaviour) that extracts zips into a `tempfile` tree mirroring the scanned
  layout, scans that tree for search outputs, and removes it automatically
  when the aggregator / its search outputs are garbage-collected, plus an
  explicit context-manager / `close()` path. An existing extracted sibling
  still wins (no re-extraction). `add_directory` threads the mode through.
- Tests in `test_autofit/aggregator/test_from_directory.py` for: no sibling
  written, identical outputs, cleanup on release, sibling-exists short-cut.
- Docstring + one-line mention in the aggregator cookbook if the workspace
  documents `from_directory` kwargs (workspace follow-up only if needed).

Trap noted from the survey: `aggregator-search-json-sentinel` (PyAutoFit#1582,
active 2026-09-08) is editing the same `scan()` loop (metadata → `search.json`
sentinel). Land after it, or stack on its branch.
