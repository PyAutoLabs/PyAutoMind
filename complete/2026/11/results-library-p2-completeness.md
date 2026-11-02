- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1753
- epic: results-library (phase 2; ledger draft/feature/autofit/results_library_epic.md)
- summary: `autofit/results/library.py` ResultsLibrary (grid / library.yaml / from_campaign — campaign expectations
  match the zip at success.zip_complete exactly, as collector.check_success); `completeness.py` check() →
  CompletenessReport (done/missing/incomplete/failed/duplicate + reasons, per-product gaps, unexpected results,
  atomic `<name>.missing.csv`); `enrich.py` + Aggregator.enrich (atomic add of files/<name> to zip AND folder copies,
  skip existing, per-result errors); `shard.py` (stable i/N); tools/util.write_zip_member; CLI `check` / `enrich`;
  `af.ResultsLibrary`. autofit_workspace#180: scripts/features/results_library.py guide (+ notebook, navigator).
- witness: W1b — DR1 laptop mirror: consensus-100 manifest 0/200 (wrong tree surfaced as 226 unexpected); 113 mirror
  objects 226/226 done incl. files/coolest.json; `_v5` naming drift surfaced as 13 missing ↔ 13 unexpected pairs;
  Workspace/Science/scratch/results_library_p2_w1b/.
- tests: test_autofit/results 58 (22 new); full suite serial 4,204 passed; independent review 8 findings fixed
  (from_index enrich skipped the folder copy — a rerun's re-zip would drop the product; campaign matching looser than
  check_success; short manifest line crash; superseded at exact location; CLI exit codes; string products; shard skew).
- decisions flagged: guide at scripts/features/; multi-root libraries need index_dir at declaration; concurrent
  enrich passes on the same results unsupported (documented); force_pickle_overwrite deprecated in docstring only.
- traps: `pytest -n 8` collides on shared /tmp paths (serial only); `autohands generate autofit` needs
  ipynb-py-convert (~/venv/PyAuto/bin) and deletes notebooks/ when it fails.

## Original prompt

Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1752
Epic: results-library
Phase: 2
Blocked-by: phase 1 (COMPLETE 2026-10-30; released in 2026.11.1.1)
Concurrent-with: results-library phase 3 (ruling F11 — two PyAutoFit worktrees; this task owns `autofit/results/{library,completeness,enrich,shard}.py`, `Aggregator.enrich`, the shared zip add-or-replace helper; phase 3 owns `aggregator/summary/aggregate_csv/`, `aggregate_fits`, `search_output.plain`, chunk/merge and reuses `shard.py`; both add subcommands to `results/__main__.py` — second to merge rebases)
Consequence: judge
Witness: W1b — read-only completeness check on the DR1 laptop mirror → Workspace/Science/scratch/results_library_p2_w1b/

# Results library phase 2 — completeness over a declared grid, and enrich

## Original request (verbatim)

"Continbue the HPC kit and results epic where we are making it so PyAutoFit can do auto run campaign things" — human approved the phase-2 plan 2026-11-02 ("I approve").

## Scope (ledger draft/feature/autofit/results_library_epic.md §Phase 2)

- Declare the expected library: datasets × searches × per-product requirements in `library.yaml`, by API
  (`af.ResultsLibrary(expected=...)`), or `from_campaign: campaign.yaml` (grid from the hpc-campaign manifest,
  stage `success.zip_complete` → location, `success.members` → required products; never a second manifest).
- Completeness report: done / missing / incomplete / failed per (dataset, search, product) with a reason;
  `<name>.missing.csv` written atomically. Path products checked via `zip_names()` (no index schema bump).
- `Aggregator.enrich(fn, name=..., overwrite=False, shard=(i, N))`: atomic add-or-replace of a zip member,
  other members byte-identical; stable shard by record key. CLI `python -m autofit.results {check,enrich}`.
- autofit_workspace guide `scripts/features/results_library.py` (declare → index → check → enrich).
- `force_pickle_overwrite` deprecated in docstring only (removal later).

Done: fixture library with deliberate holes lists every gap with its reason; enrich adds a member to 100 zips
with sha256 of all other members unchanged; killed enrich leaves the zip intact; workspace smoke green.
