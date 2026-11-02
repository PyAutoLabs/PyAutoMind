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
