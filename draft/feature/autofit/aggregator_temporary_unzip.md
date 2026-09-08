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
