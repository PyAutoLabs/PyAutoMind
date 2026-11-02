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
