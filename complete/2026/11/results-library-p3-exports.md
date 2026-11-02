- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1755
- epic: results-library (phase 3; ledger draft/feature/autofit/results_library_epic.md)
- summary: AggregateCSV.save(cache=, shard=, expected=, sort_by=, on_error=, columns_json=): row cache
  `<csv>.rows.jsonl` (row_fingerprint over zip / every file under files/ + .identifier; spec digest incl. closures,
  defaults, helper functions, hash-seed stable; rows stored as CSV text so cached == fresh); header from the column
  specs (same in every shard); on_error="row" error rows + expected= reason rows with dataset/search;
  `<name>.columns.json`; add_variable(unit=, prior_edge=) (log space for log priors); merge_csv / af.merge_csv /
  `python -m autofit.results merge` (header agreement, key dedup, deterministic sort); SearchOutput.plain + plain();
  AggregateFITS.output_to_folder atomic + skip_errors. Stacked on #1753, retargeted to main before merge.
- witness: W1c — 113 DR1 vis_pix zips read in place: first export 76 s, refresh 11 s all cached, edited column →
  recompute, kill -9 leaves CSV + cache byte-identical, cached == fresh, 4 parallel shards merge == serial;
  Workspace/Science/scratch/results_library_p3_w1c/.
- tests: test_exports.py 21 (10 review regressions); full suite serial 4,226 passed; independent review 6 bugs + 3
  minor fixed (header-from-rows broke shard merges; unresolved-path sharding duplicated expected rows behind symlinks;
  in-place rewrites + captured values missed by the cache; cached ≠ fresh text; compound_dict plain()).
- decisions flagged: CSV-only caching (not FITS); merge == serial needs the same sort_by; dict-returning computed
  columns with shard-varying keys still refuse to merge; on_error default stays "raise".
- follow-up: the "15k fixture" witness is 150 synthetic + 113 real; phase 4 (package + parity) next.

## Original prompt

Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1754
Epic: results-library
Phase: 3
Blocked-by: phase 1 (COMPLETE); stacked on phase 2 branch (PyAutoFit#1753) for shard.py + CompletenessReport
Concurrent-with: results-library phase 2 (ruling F11 — two PyAutoFit worktrees; this task owns `aggregator/summary/aggregate_csv/`, `aggregate_fits.py`, `SearchOutput.plain`, `merge` CLI subcommand; reuses phase-2 `results/shard.py`, `results/completeness.py` read-only)
Consequence: judge
Witness: W1c — DR1 laptop mirror re-export (incremental timing, killed-export safety, 4-shard merge = serial) → Workspace/Science/scratch/results_library_p3_w1c/

# Results library phase 3 — incremental, honest exports and chunk/merge

## Original request (verbatim)

"start phase 3 in parallel too" — plan approved 2026-11-02 ("I approve").

## Scope (ledger draft/feature/autofit/results_library_epic.md §Phase 3)

- AggregateCSV incremental refresh: row cache `<path>.rows.jsonl` keyed by output path + stat fingerprint + column-spec hash (computed columns hash qualname + code bytes); labels recomputed.
- Every result a row or a reason: per-row error capture → `status_reason`; `expected=` CompletenessReport adds rows for non-done expected results; optional prior-edge flag columns.
- `<name>.columns.json`: source path, kind, unit, bound type, n_blank.
- `SearchOutput.plain(name)`: plain-JSON view of autonerves-typed JSON.
- Chunk/merge: `save(shard="i/N")`, `merge_csv(parts, out, key="id")` + `python -m autofit.results merge`; header agreement, key dedup, deterministic sort; 4-shard merge byte-identical to serial with same sort_by.
- AggregateFITS: atomic writes + per-result error capture (no caching).

Done: 15k fixture refresh after 50 new results rewrites only those rows; killed export leaves previous CSV intact; 4-shard merge byte-identical to serial.
