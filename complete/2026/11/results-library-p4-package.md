- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1757
- epic: results-library (phase 4; ledger draft/feature/autofit/results_library_epic.md)
- summary: new `autofit/export/` (`af.export`): package() — size-capped / exactly-N part zips with objects whole,
  tables.zip, parts_manifest.csv, package.json, SHA256SUMS, README + KNOWN_ISSUES with provenance (git revs,
  results-index hash); deterministic atomic zips (UTC times, STORED media); delta rebuilds keep assignments and leave
  unchanged parts byte-identical; stale parts removed; include_dataset; force. verify() — checksums, CRC, members,
  empty members, CSV parse/ragged/row counts, coverage from the real zips, unlisted zips. compare() — identity incl.
  column sets, exact (big-int ids, one-sided blanks), tolerance-by-sigma with floors, values informational unless
  gated, markdown. scatter_between() — run-to-run z per path. CLI `python -m autofit.export {package,verify,compare}`.
- witness: W1d — 113 DR1 vis_pix zips → 3 parts, verify OK; one-object rebuild rewrote only part_002 (others
  byte-identical); emptied member caught. FINDING: the laptop mirror's 13 vis_lp output/ vs output_sed/ pairs are
  copies (z=0) — real run-to-run scatter (P19) needs genuine reruns (phase 5). Workspace/Science/scratch/results_library_p4_w1d/.
- tests: test_autofit/export 37 (15 review regressions); full suite serial 4,262 passed + 1 unrelated flake
  (test_fit_status sigusr1/sigterm timing under load; passes alone); independent review 16 findings fixed.
- decisions flagged: af.export (not af.agg) for scatter_between; packaging unit = folder of object folders;
  values gate only when named; change detection by name/size/mtime (force=True escape); package deletes foreign
  part_*.zip in dist.

## Original prompt

Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1756
Epic: results-library
Phase: 4
Blocked-by: phase 3 (COMPLETE 2026-11-02, PyAutoFit#1755)
Consequence: judge
Witness: W1d — DR1 laptop mirror: package 113 vis_pix + CSV into 3 parts, verify, delta rebuild (2 parts byte-identical), injected empty member caught, scatter_between on the 13 real vis_lp reruns → Workspace/Science/scratch/results_library_p4_w1d/

# Results library phase 4 — packaging, distribution and parity

## Original request (verbatim)

"start phase 4" — plan approved 2026-11-02 ("I approve").

## Scope (ledger draft/feature/autofit/results_library_epic.md §Phase 4)

- `af.export.package(source, dist, cap_gb=/n_parts=, include_dataset=, provenance)`: size-capped part zips (objects kept whole), tables.zip, parts_manifest.csv, SHA256SUMS, package.json, STORED media / DEFLATED text, atomic zips, README/KNOWN_ISSUES with provenance (git revs, index hash, counts); delta rebuild keeps assignments, rewrites only changed parts.
- `af.export.verify(dist)`: SHA256SUMS, CRC, non-empty members, CSVs parse + row counts match, manifest coverage.
- `af.export.compare(a, b, key=)`: identity / exact / tolerance-by-sigma (combined 1σ z, error floor), duplicate-key detection; values informational unless gated; markdown report.
- `af.export.scatter_between(agg_a, agg_b, paths)`: run-to-run z distribution (report P19).
- CLI `python -m autofit.export {package,verify,compare}`.

Done: 3-part fixture package; one-part rebuild leaves two byte-identical; verify catches an injected empty member; parity on two reruns reports scatter, not FAIL.
