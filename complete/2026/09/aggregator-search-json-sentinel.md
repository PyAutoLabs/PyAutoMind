- Library: PyAutoFit
- Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1582 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoFit/pull/1585 (MERGED, merge commit `1dc9250c`, head `7f344bf`)
- Workspace PR: https://github.com/PyAutoLabs/autofit_workspace_test/pull/101 (MERGED, merge commit `48f56c33`, head `4781213`)
- Workspace PR: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/133 (MERGED, merge commit `d585e3d5`, head `e4874fe`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1585
- heart-ack: 2026-09-08 YELLOW acknowledged in-session, two organism-scope reasons (multi_dataset workspace validation failures; no release rehearsal) — none of the failing scripts touched by this diff
- parallel-claim: PyAutoFit and autofit_workspace_test were also claimed by traced-assertions-on-jax-path (#1581); file sets disjoint; own worktree

## What shipped

**The `metadata` output file is gone.** Every `DirectoryPaths.save_all` used to append a
two-line `metadata` file (`name=…`, `non_linear_search=…`) into each search output folder.
A survey found exactly one load-bearing consumer: `Aggregator.from_directory` treated any
walked directory containing a file named `metadata` as a search output. `files/search.json`
is written unconditionally by the same `save_all` (including the skip-fit-output branch), so
discovery now keys on that at zero extra run-time or aggregation cost.

- `autofit/aggregator/aggregator.py`: `_is_search_output(root, dirs, filenames)` returns true
  when `<root>/files/search.json` exists (the `"files" in dirs` guard keeps `os.walk` from
  returning the `files/` directory itself) or, for legacy output, when `metadata` is present.
- `autofit/aggregator/search_output.py`: the `metadata` parse into `__dict__` / `.text` is
  removed; `non_linear_search` is a property reading the `class_path` leaf of `search.json`
  (lower-cased, matching what the old file wrote) with a legacy fallback to the `metadata`
  line; `__str__`/`__repr__` report the directory.
- `autofit/non_linear/paths/directory.py`: `_save_metadata` and its call deleted.
- `abstract_search.py`: the skip-fit-output comment names `files/search.json` as what the
  aggregator needs.
- Tests: four `metadata` fixtures removed; `fit_1`/`fit_2` summary fixtures gained the
  `files/search.json` they lacked; zip round-trip assertion moved to `search.json`; new
  tests cover the sentinel, the `files/`-without-`search.json` case, legacy discovery and
  the `non_linear_search` filter. Full suite 2477 passed, 2 skipped; a real `af.LBFGS` fit
  wrote no `metadata` and aggregated with `non_linear_search == "lbfgs"`.

**Workspace side.** The aggregator profiling mocks in `autofit_workspace_test`
(`scripts/profiling/aggregator/`) and `autolens_workspace_developer`
(`aggregator_profiling/`) stamped a `dataset_name=` line into each copy's `metadata` and the
harness queried `agg.dataset_name`. Both now rely on the `unique_tag` they already write into
`search.json`; the harness queries and names outputs by `unique_tag` (timing key
`query_dataset_name` → `query_unique_tag`, no consumer of the old key). Both profiling
scripts pass in quick mode.

## Why resume was safe

Resume keys entirely on `.completed`; nothing on the `is_complete` /
`result_via_completed_fit` path read `metadata`, and `SearchOutput` already swallowed its
absence. The only risk was aggregator discovery, which is why legacy folders stay accepted.

## Follow-ups

- `draft/bug/workspaces/profile_lens_aggregator_needs_config_dir.md`: pre-existing,
  `profile_lens_aggregator.py` cannot run from the `autolens_workspace_developer` root
  because the repo has no `config/` tree (its smoke here ran from a scratch dir symlinking
  `autolens_workspace/config`).

## Original prompt

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
Issued: 2026-09-08

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
