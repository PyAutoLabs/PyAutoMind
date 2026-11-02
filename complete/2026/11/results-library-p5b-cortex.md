- epic: results-library (phase 5b; ledger draft/feature/autofit/results_library_epic.md)
- summary: `cortex.py library <project> <index_dir> [--name] [--dry-run]` appends a fact-only `library` ledger entry
  (decision 65): `<name>: index <hash12> — N results (<state counts>)`, hash = autofit.export.index_hash (sha256 of
  output_path|state|completed_at per record, path order) computed from the index JSON with no autofit import.
  Written only by the verb (`log --kind` excludes it), one dated line per call, never result/lesson/## Now/## Runs.
- tests: 14 new (hash parity with autofit on a real ResultsIndex); suite 105 passed; cortex check OK.
- decisions flagged (merged as defaults): default --name; projects.yaml key check; counts from records; unknown
  states alphabetical; bad record files skipped.
- built by a delegated Opus agent, reviewed in-session before ship.

## Original prompt

Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/84
Epic: results-library
Phase: 5b
Consequence: judge

# Results library 5b — Cortex `library` ledger entry (index hash + counts)

Human: "start phase 5" → "5a + 5b now" (2026-11-02). Scope in the issue; new entry kind is decide-and-flag (schema decision).
