# Remove the output-folder `metadata` file; aggregator discovers searches via `files/search.json`

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
- autolens_workspace_developer
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Witness: no search output folder written by `DirectoryPaths.save_all` contains a `metadata` file; `Aggregator.from_directory` on a fresh run (and on a legacy folder that still carries `metadata`) returns the same search outputs as before; `agg.filter(agg.non_linear_search == ...)` still works, sourced from `search.json`; resume of a run whose `metadata` file has been deleted is unaffected; full PyAutoFit test suite green.
Unattended: ready
Filed: 2026-09-08

Original request (verbatim):

> Is the "metadata" file that is output to the output folder of all autofit /
> autolens runs still required? Is there any way we could remove it or would
> this disrupt on going runs
>
> Would using search.json impact run time in a meaningful way? If not then
> that is the solution
>
> lets go, use search.json and remove metadata

Findings (2026-09-08 survey):

- Sole writer: `DirectoryPaths._save_metadata` (`autofit/non_linear/paths/directory.py`),
  called last in `save_all`. Two `key=value` lines: `name=`, `non_linear_search=`.
  Appends, so resumed runs duplicate the block.
- Sole sentinel: `Aggregator.from_directory` (`autofit/aggregator/aggregator.py`)
  treats a directory as a search output iff `"metadata" in filenames`. The
  database scrape and MCP tools inherit this by iterating the aggregator.
- `SearchOutput.__init__` (`autofit/aggregator/search_output.py`) parses it
  into `self.__dict__`; `name` is shadowed by the property reading
  `search.json`, so only `non_linear_search` survives as a filter attribute.
  Absence is already swallowed (`FileNotFoundError` passed).
- Resume keys entirely on `.completed`; nothing on that path reads `metadata`.
- `files/search.json` is written unconditionally by the same `save_all`
  (including the skip-fit-output branch), so switching costs no I/O.
- Trap: `search.json` lives one level down in `files/`; the sentinel must be
  checked from the search root (`"files" in dirs` + exists), not by name match
  in `filenames`, or `os.walk` would hand `SearchOutput` the `files/` dir.
- Mock writers to update: `autofit_workspace_test/scripts/profiling/aggregator/mock_results.py`,
  `autolens_workspace_developer/aggregator_profiling/mock_lens_results.py`.
- Test fixtures under `test_autofit/aggregator/` carry `metadata` files;
  `test_from_directory.py` asserts one survives a zip round-trip.
